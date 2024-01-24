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
from demo.accounts.services import AccountService

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
        AccountCreate(
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
def get_account( account_id: int, service: AccountService = Depends()):
    return service.get_account(account_id)


@router.patch('/accounts/{account_id}', response_model=AccountSerializer)
def edit_account(
    account_id: int,
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    avatar: UploadFile | None = File(None),
    service: AccountService = Depends(),
):
    from demo.accounts.schemas import AccountUpdate
    service.update_account(
        id_=account_id,
        account_update=AccountUpdate(
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
        )
    )
    return Response(status_code=status.HTTP_202_ACCEPTED)
