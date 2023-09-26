from pydantic import EmailStr, field_validator

from .base import BaseValidationSchema, NonEmptyStr


class AccessTokenSchema(BaseValidationSchema):
    access_token: NonEmptyStr


class LoginSchema(BaseValidationSchema):
    email: EmailStr
    password: NonEmptyStr


class SignUpSchema(BaseValidationSchema):
    email: EmailStr
    password: NonEmptyStr

    @field_validator("password")
    @classmethod
    def password_validator(cls, password):
        min_length = 6

        if len(password) < min_length:
            raise ValueError(f"Password must be at least {min_length} characters long.")
        if not any(character.islower() for character in password):
            raise ValueError("Password should contain at least one lowercase letter.")
        if not any(character.isupper() for character in password):
            raise ValueError("Password should contain at least one uppercase letter.")
        if not any(character.isdigit() for character in password):
            raise ValueError("Password should contain at least one digit.")

        return password
