from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean

from src.db.session import Base


class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'), nullable=False)
    file_name = Column(String, nullable=False)
    status = Column(String, default="pending")
    uploaded_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)
