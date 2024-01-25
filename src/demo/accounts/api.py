from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import Response
from fastapi import status
from fastapi import UploadFile

from demo.accounts.schemas import AccountCreate
from demo.accounts.schemas import AccountSerializer
from demo.accounts.schemas import AccountUpdate
from demo.accounts.services import AccountService

router = APIRouter(prefix='/accounts')


def initialize_app(app: FastAPI) -> None:
    app.include_router(router)


@router.post('')
def create_account(
    account_create: AccountCreate,
    service: AccountService = Depends()
):
    service.create_account(account_create)
    return Response('CREATED', status_code=status.HTTP_201_CREATED)


@router.get('', response_model=list[AccountSerializer])
def get_accounts(service: AccountService = Depends()):
    return service.get_accounts()


@router.get('/{account_id}', response_model=AccountSerializer)
def get_account(account_id: int, service: AccountService = Depends()):
    return service.get_account(account_id)


# TODO: разобраться и доработать
@router.patch('/{account_id}', response_model=AccountSerializer)
def edit_account(
    account_id: int,
    # account_update: AccountUpdate,
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    avatar: UploadFile | None = File(None),
    service: AccountService = Depends(),
):
    service.update_account(
        id_=account_id,
        account_update=AccountUpdate(
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
        )
    )
    # service.update_account(account_id, account_update)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.put('/{account_id}/avatar')
def update_account_avatar(
    account_id: int,
    avatar: UploadFile = File(),
    service: AccountService = Depends()
):
    service.update_account_avatar(account_id, avatar)
    return Response(status_code=status.HTTP_202_ACCEPTED)
