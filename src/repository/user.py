from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user from the database based on the provided email.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user corresponding to the provided email.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user in the database with the provided user data.

    :param body: The user data to create the user with.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def confirmed_email(email: str, db: Session) -> None:
    """
    Marks the user with the provided email as confirmed in the database.

    :param email: The email address of the user to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh token for the specified user in the database.

    :param user: The user whose token needs to be updated.
    :type user: User
    :param token: The new refresh token. If None, the existing token will be removed.
    :type token: str or None
    :param db: The database session.
    :type db: Session
    """
    user.refresh_token = token
    db.commit()
