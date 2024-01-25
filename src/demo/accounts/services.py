import shutil

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

    def create_account(self, account: AccountCreate) -> None:
        self.session.add(
            Account(
                email=account.email,
                username=account.username,
                password=pbkdf2_sha256.hash(account.password),
            )
        )
        try:
            self.session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    def get_accounts(self) -> list[Account]:
        return self.session.query(Account).all()

    def _get_account(self, id_: int) -> Account:
        account: Account | None = self.session.query(Account).filter_by(
            id=id_,
        ).first()
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return account

    def get_account(self, id_: int) -> Account:
        return self._get_account(id_)

    def update_account(self, id_: int, account_update: AccountUpdate) -> None:
        account = self._get_account(id_)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if (
                not account_update.first_name
                and not account_update.last_name
                and not account_update.avatar
        ):
            return

        account.first_name = account_update.first_name or account.first_name
        account.last_name = account_update.last_name or account.last_name

        if account_update.avatar:
            filepath = BASE_DIR.joinpath(
                self.settings.STATIC_DIR,
                account_update.avatar.filename,
            )
            with filepath.open('wb') as file:
                shutil.copyfileobj(account_update.avatar.file, file)

            file_url = (f'{self.settings.STATIC_URL}/'
                        f'{account_update.avatar.filename}')
            account.avatar = file_url

        self.session.commit()

    def update_account_avatar(self, id_: int, avatar_url: UploadFile) -> None:
        pass