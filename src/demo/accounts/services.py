import shutil
from typing import Never

from dynaconf import Dynaconf
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import UploadFile
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from demo.accounts.models import Account
from demo.accounts.schemas import AccountCreate
from demo.accounts.schemas import AccountUpdate
from demo.config import BASE_DIR
from demo.config import get_settings
from demo.database import get_session
from demo.database import Session


class AccountService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Dynaconf = Depends(get_settings),
    ) -> None:
        self.session = session
        self.settings = settings

    def create_account(self, account: AccountCreate) -> Account | Never:
        new_account = Account(
            email=account.email,
            username=account.username,
            password=pbkdf2_sha256.hash(account.password),
        )
        self.session.add(new_account)
        try:
            self.session.commit()
            return new_account
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    def get_accounts(self) -> list[Account]:
        return self.session.query(Account).all()

    def _get_account(self, id_: int) -> Account | Never:
        account: Account | None = self.session.query(Account).filter_by(id=id_).first()
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return account

    def get_account(self, id_: int) -> Account:
        return self._get_account(id_)

    def update_account(
        self,
        id_: int,
        account_update: AccountUpdate
    ) -> Account | Never:
        account = self._get_account(id_)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if (
                not account_update.first_name
                and not account_update.last_name
                and not account_update.avatar
        ):
            return account

        account.first_name = account_update.first_name or account.first_name
        account.last_name = account_update.last_name or account.last_name
        self.session.commit()
        return account

    def update_account_avatar(self, id_: int, avatar: UploadFile) -> Account:
        account = self._get_account(id_)
        filepath = BASE_DIR.joinpath(self.settings.STATIC_DIR, avatar.filename)
        with filepath.open('wb') as file:
            shutil.copyfileobj(avatar.file, file)

        account.avatar = f'{self.settings.STATIC_URL}/{avatar.filename}'
        self.session.commit()
        return account
