import shutil

from dynaconf import Dynaconf
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi import UploadFile

from demo.accounts.models import Account
from demo.accounts.schemas import AccountDeserializer
from demo.accounts.schemas import AccountSerializer
from demo.accounts.services import AccountService
from demo.config import BASE_DIR
from demo.config import get_settings
from demo.database import get_session
from demo.database import Session

router = APIRouter()


def initialize_app(app: FastAPI) -> None:
    app.include_router(router)


@router.post('/account')
def create_account(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(),
    service: AccountService = Depends()
):
    service.create_account(
        AccountDeserializer(
            email=email,
            username=username,
            password=password,
        )
    )
    return Response('CREATED', status_code=status.HTTP_201_CREATED)


@router.get('/accounts', response_model=list[AccountSerializer])
def get_accounts(service: AccountService = Depends()):
    return service.get_accounts()


@router.get('/accounts/{account_id}', response_model=AccountSerializer)
def get_account(
    account_id: int,
    service: AccountService = Depends(),
):
    return service.get_account(account_id)


@router.patch('/accounts/{account_id}', response_model=AccountSerializer)
def edit_account(
    account_id: int,
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    avatar: UploadFile | None = File(None),
    service: AccountService = Depends(),
):
    account = session.query(Account).filter_by(id=account_id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not first_name and not last_name and not avatar:
        return account

    account.first_name = first_name or account.first_name
    account.last_name = last_name or account.last_name

    if avatar:
        filepath = BASE_DIR / settings.STATIC_DIR / avatar.filename
        with filepath.open('wb') as file:
            shutil.copyfileobj(avatar.file, file)

        file_url = f'{settings.STATIC_URL}/{avatar.filename}'
        account.avatar = file_url

    session.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)
