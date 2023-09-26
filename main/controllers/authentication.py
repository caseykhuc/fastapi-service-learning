from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from main.commons import exceptions
from main.commons.exceptions import ErrorCode, ErrorMessage, Unauthorized
from main.engines.users import add_user, get_user_by_email, verify_password
from main.schemas.authentication import AccessTokenSchema, LoginSchema, SignUpSchema
from main.utils import auth

router: APIRouter = APIRouter()


@router.post("/register", response_model=AccessTokenSchema)
async def _add_user(user: SignUpSchema):
    try:
        user = await add_user(email=user.email, password=user.password)
        return AccessTokenSchema(access_token=auth.create_access_token_from_id(user.id))
    except IntegrityError:
        raise exceptions.BadRequest(
            error_message=ErrorMessage.ACCOUNT_ALREADY_REGISTERED,
            error_code=ErrorCode.ACCOUNT_ALREADY_REGISTERED,
        )


@router.post("/login", response_model=AccessTokenSchema)
async def _authenticate_user(user_data: LoginSchema):
    user = await get_user_by_email(user_data.email)

    if user and verify_password(user_data.password, user.hashed_password):
        return AccessTokenSchema(
            access_token=auth.create_access_token_from_id(user.id),
        )

    raise Unauthorized(error_message=ErrorMessage.INVALID_LOGIN_CREDENTIALS)
