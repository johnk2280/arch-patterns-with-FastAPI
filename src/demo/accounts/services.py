from dynaconf import Dynaconf
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from demo.accounts.models import Account
from demo.accounts.schemas import AccountDeserializer
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

    def create_account(self, account: AccountDeserializer) -> None:
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