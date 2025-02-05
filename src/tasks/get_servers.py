from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.worker import celery_app
from src.db.models import Server
from src.tasks.check_servers import check_server_for_new_files
from src.db.session import get_session


@celery_app.task
def get_active_servers():
    """
    Проверка одного SFTP-сервера на наличие новых файлов.
    """
    session: Session = get_session()

    try:
        query = select(Server).filter_by(is_active=True)
        result = session.execute(query)
        active_servers = result.scalars().all()
    
        for server in list(active_servers):
            check_server_for_new_files.delay(server.id)
    finally:
        session.close()
