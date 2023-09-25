import bcrypt

from main import db
from main.models.user import UserModel


async def create_user(email: str, password: str):
    user = UserModel(
        email=email,
        hashed_password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
    )

    db.session.add(user)
    await db.session.commit()

    return user
