import jwt


def create_token(data: dict):
    token : str = jwt.encode(payload=data, key='misecret', algorithm='HS256')
    return token

def validate_token(token: str) -> dict:
    data : dict = jwt.decode(token, key='misecret', algorithms=['HS256'])
    return data