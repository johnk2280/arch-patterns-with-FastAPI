from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from demo.database import Base


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
