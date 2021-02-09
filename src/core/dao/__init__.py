from sqlalchemy import create_engine
from os import getenv

engin = create_engine(
    getenv("DATABASE_URL").split(', ')[1],
    echo=True,
    connect_args={'connect_timeout': 3},
    pool_pre_ping=True
)
