from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    ENVIRONMENT: Literal['dev', 'prod', 'test']

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str

    @property
    def database_url(self) -> PostgresDsn:
        if self.ENVIRONMENT == 'test':
            return (f'postgresql+asyncpg://'
                    f'{self.TEST_DB_USER}:{self.TEST_DB_PASS}@'
                    f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/'
                    f'{self.TEST_DB_NAME}')

        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@'
                f'{self.DB_HOST}:{self.DB_PORT}/'
                f'{self.DB_NAME}')

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(db_name={self.DB_NAME})>'


def get_settings() -> Settings:
    return Settings()

