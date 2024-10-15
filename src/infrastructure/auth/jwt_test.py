import jwt

payload = {
    'iss': 'https://auth.example.com',
    'sub': 'bcdef178-58bb-411f-b285-c05fc776c3ce',
    'aud': 'https://127.0.0.1:8000/products',
    'iat': 1728950932,
    'exp': 1726531807,
    'azp': 'fc88d225-1321-41d4-a5c2-1424ea9e8210',
    'scope': 'openid',
}

if __name__ == '__main__':

    result = jwt.encode(payload=payload, key='secret', algorithm='HS256')
    print(result)
