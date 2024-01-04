"""Database Models Description."""

import enum
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class AbstractBase(DeclarativeBase):
    """Declaration of AbstractBase class.

    Args:
        DeclarativeBase (class): SQLAlchemy DeclarativeBase class.
    """

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class AccessLevel(enum.Enum):
    """Declaration of Enum-like AccessLevel data type.

    Args:
        enum (class): Basic Python Enum class.
    """

    client = 1
    moderator = 2
    superuser = 3


class Role(AbstractBase):
    """Declaration of ORM representation of Role table.

    Args:
        Base (class): AbstractBase class.
    """

    __tablename__ = 'role'

    description: Mapped[Optional[str]]
    access: Mapped[AccessLevel]
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user_service: Mapped[List['UserService']] = relationship(
        back_populates='role',
    )


class UserService(AbstractBase):
    """Declaration of ORM representation of UserService table.

    Args:
        Base (class): AbstractBase class.
    """

    __tablename__ = 'user_service'

    is_active: Mapped[bool]
    data_joined: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    role: Mapped['Role'] = relationship(
        back_populates='role',
    )
    user: Mapped['User'] = relationship(back_populates='user_service')


class LoginHistory(AbstractBase):
    """Declaration of ORM representation of LoginHistory table.

    Args:
        Base (class): AbstractBase class.
    """

    __tablename__ = 'login_history'

    user_agent: Mapped[str]
    login_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped['User'] = relationship(back_populates='login_history')


class User(AbstractBase):
    """Declaration of ORM representation of User table.

    Args:
        Base (class): AbstractBase class.
    """

    __tablename__ = 'user'

    # The common max e-mail length is 254 characters. WPS432 (Magic Number).
    email: Mapped[str] = mapped_column(
        String(254), unique=True,  # noqa: WPS432
    )
    login: Mapped[str] = mapped_column(String(60), unique=True)
    password: Mapped[str]
    avatar: Mapped[Optional[str]]
    bio: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]] = mapped_column(String(60))
    last_name: Mapped[Optional[str]] = mapped_column(String(60))
    phone_number: Mapped[Optional[str]] = mapped_column(String(24))
    birthday: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
    )

    login_history: Mapped[List['LoginHistory']] = relationship(
        back_populates='user',
    )
    user_service: Mapped['UserService'] = relationship(
        back_populates='user',
        )
