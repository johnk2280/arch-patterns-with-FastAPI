from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DB_HOST: str = Field('localhost', env='DB_HOST')
    DB_PORT: int = Field(5432, env='DB_PORT')
    DB_NAME: str = Field('arch_patterns', env='DB_NAME')
    DB_USER: str = Field('postgres', env='DB_USER')
    DB_PASS: str = Field('postgres', env='DB_PASS')

    @property
    def url(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@'
                f'{self.DB_HOST}:{self.DB_PORT}/'
                f'{self.DB_NAME}')

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(db_name={self.DB_NAME})>'


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    database: DatabaseSettings = DatabaseSettings()


settings = Settings()

