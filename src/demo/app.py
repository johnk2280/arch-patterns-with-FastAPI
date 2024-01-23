from fastapi import FastAPI
from fastapi import Form
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from demo.database import Account
from demo.database import Session

app = FastAPI()


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


@app.get('/accounts')
def get_accounts():
    with Session() as session:
        accounts = session.query(Account).all()

    return accounts
