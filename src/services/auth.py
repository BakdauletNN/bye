

class AuthService:

    def __init__(self, session):
        self.session = session

    async def create_acces_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=stgs.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encode_jwt = jwt.encode(to_encode, stgs.SECRET_KEY, algorithm=stgs.HASH__ALG0)
        return encode_jwt


    async def verify_pass(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

