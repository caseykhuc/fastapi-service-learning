import datetime
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError

from main import config
from main.commons.exceptions import ErrorCode, ErrorMessage, Forbidden, Unauthorized


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


def get_id_from_access_token(token: str) -> int | None:
    try:
        return jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms="HS256",
        ).get("sub")
    except DecodeError:
        return None


async def require_authentication(
    token: Annotated[
        HTTPAuthorizationCredentials,
        Depends(HTTPBearer(auto_error=False)),
    ],
) -> int | None:
    if not token:
        raise Unauthorized()

    user_id = get_id_from_access_token(token.credentials)
    if not user_id:
        raise Unauthorized()

    return user_id


async def require_creator(
    required_id: int,
    id: Annotated[int, Depends(require_authentication)],
):
    if required_id != id:
        raise Forbidden(
            error_message=ErrorMessage.NOT_CREATOR,
            error_code=ErrorCode.NOT_CREATOR,
        )
