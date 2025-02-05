from sqlalchemy.orm import Session

from src.schemas.server import ServerCreate
from src.db.models import Server

def add_server(session: Session, server_scheme: ServerCreate) -> Server:
    server = Server(**server_scheme.model_dump())

    try:
        session.add(server)
    except:
        session.rollback()
    else:
        session.commit()
    
    return server