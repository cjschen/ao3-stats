from typing import List
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy import create_engine
from constants import RATINGS, TAG_TYPES
class Base(DeclarativeBase):
    pass 

class Works(Base):
    __tablename__ = 'works'
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    heading: Mapped[str] = mapped_column(String(255))
    rating: Mapped[int] = mapped_column(ForeignKey('ratings.id'))
    completed: Mapped[bool]
    last_updated = mapped_column(DateTime)
    summary: Mapped[str] = mapped_column(String(1250))
    kudos: Mapped[int]
    words: Mapped[int]
    chapters: Mapped[int]
    comments: Mapped[int]
    hits: Mapped[int]
    bookmarks: Mapped[int]
    total_chapters: Mapped[int] = mapped_column(Integer, nullable=True)

    tags: Mapped[List["Tags"]] = relationship(back_populates='work')
    fandoms: Mapped[List["Fandoms"]] = relationship(back_populates='work')

class Ratings(Base):
    __tablename__='ratings'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(31), unique=True)

class Authors(Base):
    __tablename__='authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    
class TagTypes(Base):
    __tablename__='tag_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

class Tags(Base):
    __tablename__='tags'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    work_id = mapped_column(ForeignKey("works.id"))
    type = mapped_column(ForeignKey("tag_types.id"))
    # user: Mapped["User"] = relationship(back_populates="addresses")
    work: Mapped["Works"] = relationship(back_populates='tags')

class Fandoms(Base):
    __tablename__='fandoms'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    work_id = mapped_column(ForeignKey("works.id"))

    work: Mapped["Works"] = relationship(back_populates='fandoms')

class Downloads(Base):
    __tablename__='downloads'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fandom: Mapped[int] = mapped_column(ForeignKey("fandoms.id"))
    date = mapped_column(DateTime)


engine = create_engine("sqlite:///aooo.db", echo=True)

def recreate_db():

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine) 

    with Session(engine) as session:
        for tag_type in TAG_TYPES.keys():
            session.add(TagTypes(name=tag_type))
        for rating in RATINGS.keys():
            session.add(Ratings(name=rating))
        session.commit()