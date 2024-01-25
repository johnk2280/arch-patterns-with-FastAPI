from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import Response
from fastapi import status
from fastapi import UploadFile

from demo.accounts.models import Account
from demo.accounts.schemas import AccountCreate
from demo.accounts.schemas import AccountSerializer
from demo.accounts.schemas import AccountUpdate
from demo.accounts.services import AccountService

router = APIRouter(prefix='/accounts')


def initialize_app(app: FastAPI) -> None:
    app.include_router(router)


@router.post('', response_model=AccountSerializer, status_code=status.HTTP_201_CREATED)
def create_account(
    account_create: AccountCreate,
    service: AccountService = Depends()
) -> Account:
    return service.create_account(account_create)


@router.get('', response_model=list[AccountSerializer])
def get_accounts(service: AccountService = Depends()) -> list[Account]:
    return service.get_accounts()


@router.get('/{account_id}', response_model=AccountSerializer)
def get_account(account_id: int, service: AccountService = Depends()) -> Account:
    return service.get_account(account_id)


@router.patch('/{account_id}', response_model=AccountSerializer)
def edit_account(
    account_id: int,
    account_update: AccountUpdate,
    service: AccountService = Depends(),
) -> Account:
    return service.update_account(account_id, account_update)


@router.put('/{account_id}/avatar', response_model=AccountSerializer, status_code=status.HTTP_202_ACCEPTED)
def update_account_avatar(
    account_id: int,
    avatar: UploadFile = File(),
    service: AccountService = Depends()
):
    return service.update_account_avatar(account_id, avatar)
