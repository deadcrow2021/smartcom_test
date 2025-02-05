import paramiko
from sqlalchemy.orm import Session
from datetime import datetime

from src.core.worker import celery_app
from src.db.models import Server, File
from src.tasks.download_file import download_file
from src.db.session import get_session


@celery_app.task
def check_server_for_new_files(server_id):
    """
    Проверка одного SFTP-сервера на наличие новых файлов.
    """
    session: Session = get_session()

    server = session.query(Server).filter_by(id=server_id, is_active=True).first()
    if not server:
        return

    try:
        # Подключение к SFTP
        transport = paramiko.Transport((server.host))
        transport.connect(username=server.username, password=server.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        remote_dir = '/uploads/'
        files = sftp.listdir(remote_dir)

        for file in files:
            stat = sftp.stat(remote_dir)
            file_fullname = f'{file}_{stat.st_size}_{stat.st_mtime}'

            # Проверяем, был ли файл уже обработан
            if not session.query(File).filter_by(server_id=server.id, file_name=file_fullname).first():
                file_record = File(
                    server_id=server.id,
                    file_name=file_fullname,
                    status="ready"
                )
                session.add(file_record)
                session.commit()
                download_file.delay(server_id, file, file_fullname)
        sftp.close()
        transport.close()

    except Exception as e:
        print(f"Error checking server {server.host}: {e}")

    finally:
        session.close()