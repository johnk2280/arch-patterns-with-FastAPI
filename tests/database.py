from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy import event
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
    settings.TEST_DATABASE_URL,
    future=True,  # только для SQLite
    connect_args={'check_same_thread': False},  # только для SQLite
)

Session = sessionmaker(engine, future=True)


def get_session() -> Session:
    with Session() as session:
        yield session
