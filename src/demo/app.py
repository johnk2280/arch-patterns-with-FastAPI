import shutil
from pathlib import Path

from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi import UploadFile
from fastapi.staticfiles import StaticFiles
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from demo.config import BASE_DIR
from demo.config import settings
from demo.database import Account
from demo.database import Session
from demo.schemas import AccountSerializer

app = FastAPI()
app.mount(
    settings.STATIC_URL,
    StaticFiles(directory=settings.STATIC_DIR),
    name='static'
)


@app.post('/account')
def create_account(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(),
):
    with Session() as session:
        account = Account(
            email=email,
            username=username,
            password=pbkdf2_sha256.hash(password),
        )
        session.add(account)

        try:
            session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return Response('CREATED', status_code=status.HTTP_201_CREATED)


@app.get('/accounts', response_model=list[AccountSerializer])
def get_accounts():
    with Session() as session:
        accounts = session.query(Account).all()

    return accounts


@app.get('/accounts/{account_id}', response_model=AccountSerializer)
def get_accounts(account_id: int):
    with Session() as session:
        accounts = session.query(Account).filter_by(id=account_id).first()

    if not accounts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return accounts


@app.patch('/accounts/{account_id}', response_model=AccountSerializer)
def edit_account(
    account_id: int,
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    avatar: UploadFile | None = File(None),
):
    with Session() as session:
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
