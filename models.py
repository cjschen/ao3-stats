from typing import List
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass 

class Works(Base):
    __tablename__ = 'works'
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    rating: Mapped[int]
    completed: Mapped[bool]
    last_updated = mapped_column(DateTime)
    summary: Mapped[str] = mapped_column(String(1250))
    kudos: Mapped[int]
    words: Mapped[int]
    chapters: Mapped[int]
    comments: Mapped[int]
    hits: Mapped[int]
    bookmarks: Mapped[int]
    total_chapters: Mapped[int]

    tags: Mapped[List["Tags"]] = relationship(back_populates='works')
    

class TagTypes(Base):
    __tablename__='tag_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(15))

class Tags(Base):
    __tablename__='tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    work_id = mapped_column(ForeignKey("works.id"))
    tag_type = mapped_column(ForeignKey("tag_types.type"))
    # user: Mapped["User"] = relationship(back_populates="addresses")
    work: Mapped["Works"] = relationship(back_populates='tags')

engine = create_engine("sqlite:///aooo.db", echo=True)
Base.metadata.create_all(engine)
