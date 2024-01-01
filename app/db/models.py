from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ToDo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(BigInteger,
                                    primary_key=True,
                                    autoincrement=True,
                                    index=True)
    title: Mapped[str]