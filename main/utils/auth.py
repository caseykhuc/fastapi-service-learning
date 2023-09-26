import datetime

import jwt

from main import config


def create_access_token_from_id(
    account_id: int,
) -> str:
    iat = datetime.datetime.utcnow()

    return jwt.encode(
        {
            "sub": account_id,
            "iat": iat,
            "exp": iat + datetime.timedelta(seconds=config.JWT_LIFETIME),
        },
        config.JWT_SECRET,
    )
