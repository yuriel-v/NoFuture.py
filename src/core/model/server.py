from sqlalchemy import Column, String, Integer, BigInteger
from core.model import Base


class Server(Base):
    __tablename__ = "server"

    id = Column(Integer, primary_key=True, autoincrement=True)
    server_name = Column(String)
    server_id = Column(BigInteger, unique=True, nullable=False)
    cogs_enabled = Column(BigInteger, nullable=False)

    def import_server(self, srv):
        if not isinstance(srv, Server):
            return
        for attr in list(filter(lambda x: '__' not in x, dir(self))):
            if srv.__getattribute__(attr) is None:
                continue
            self.__setattr__(attr, srv.__getattribute__(attr))
