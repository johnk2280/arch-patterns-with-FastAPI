from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy import event
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from demo.config import settings


# Функция обработчик для автоматического создания внешних ключей в БД SQLite.
# Только для SQLite
@event.listens_for(Engine, 'connect')
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


engine = create_engine(
    settings.DATABASE_URL,
    future=True,  # только для SQLite
    connect_args={'check_same_thread': False},  # только для SQLite
)

Session = sessionmaker(engine, future=True)
Base = declarative_base()


def get_session() -> Session:
    with Session() as session:
        yield session


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String)

    def __repr__(self) -> str:
        return (f'<Account '
                f'id={self.id}, '
                f'email={self.email}, '
                f'username={self.username}>')
