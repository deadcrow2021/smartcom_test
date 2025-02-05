from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from src.db.session import get_session
from src.schemas.server import Server, ServerCreate
from src.services.add_server import add_server


servers_router = APIRouter(prefix='/server', tags=['Server'])

@servers_router.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    response_model=Server)
def add_server_view(
    server: ServerCreate,
    session: Session = Depends(get_session) 
):
    return add_server(session, server)
