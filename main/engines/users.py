import bcrypt
from sqlalchemy import select

from main import db
from main.models.user import UserModel


async def add_user(email: str, password: str) -> UserModel:
    user = UserModel(
        email=email,
        hashed_password=bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt(),
        ),
    )

    db.session.add(user)
    await db.session.commit()

    return user


async def get_user_by_email(email: str) -> UserModel:
    statement = select(UserModel).filter(UserModel.email == email)
    result = await db.session.execute(statement)

    return result.scalar()


def verify_user(user: UserModel, password: str):
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=user.hashed_password.encode(),
    )
