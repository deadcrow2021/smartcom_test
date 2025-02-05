import paramiko
from minio import Minio
from minio.error import S3Error
from sqlalchemy.orm import Session
from datetime import datetime

from src.core.worker import celery_app
from src.core.settings import sftp_settings, minio_settings
from src.db.session import get_session
from src.tasks.notify_external import notify_external_service
from src.db.models import File, Server


@celery_app.task
def download_file(server_id, file, file_fullname):
    session: Session = get_session()

    try:
        server = session.query(Server).filter_by(id=server_id).first()
        if not server:
            return

        # Подключение к SFTP
        transport = paramiko.Transport((server.host))
        transport.connect(username=sftp_settings.sftpuser, password=sftp_settings.sftppassword)
        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_file_path = f"/uploads/{file}"

        minio_client = Minio(
            f'{minio_settings.minio_host}:{minio_settings.minio_port}',
            access_key=minio_settings.minio_access_key,
            secret_key=minio_settings.minio_secret_key,
            secure=False
        )

        with sftp.open(remote_file_path, "rb") as sftp_file:
            stat = sftp.stat(remote_file_path)
            file_size = stat.st_size
            file_fullname = f'{file}_{file_size}_{stat.st_mtime}'
            minio_client.put_object(minio_settings.minio_bucket, file, sftp_file, file_size)

        file_record = File(
            server_id=server.id,
            file_name=file_fullname,
            status="uploaded",
            uploaded_at=datetime.now()
        )
        session.add(file_record)
        session.commit()

        # Уведомление внешнего сервиса через RabbitMQ
        notify_external_service.delay(file)

    except S3Error as e:
        print(f"MinIO error for file {file}: {e}")
        file_record = session.query(File).filter_by(file_name=file_fullname).first()
        if file_record:
            file_record.status = "error"
            file_record.error_message = str(e)
            session.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        session.close()
        sftp.close()
        transport.close()
