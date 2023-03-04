from bs4 import BeautifulSoup
from models import Works, Tags, Fandoms, Authors, engine
from sqlalchemy import inspect, select
from sqlalchemy.orm import Session
from datetime import datetime
from constants import RATINGS, TAG_TYPES


class Work:
    def __init__(self, work: BeautifulSoup) -> None:
        self.work = work

        self.id = self.work['id'].split("_")[1]
        self.heading = self.find_all('h4.heading > a')[0]
        self.author = self.find_single_attr("a[rel=author]")
        self.last_updated = datetime.strptime(
            self.find_single_attr('.datetime'), "%d %b %Y")
        self.fandoms = self.find_all(".fandoms .tag")

        # Required Tags
        self.rating = self.find_single_attr(".rating > span")
        self.categories = self.find_single_attr(".category > span").split(", ")
        self.completed = (self.find_single_attr(
            '.iswip > span') == 'Complete Work')
        self.warnings = self.find_single_attr('.warnings > span').split(", ")

        # Other tags
        self.relationships = self.find_all(".relationships > .tag")
        self.characters = self.find_all(".characters > .tag")
        self.freeforms = self.find_all(".freeforms > .tag")

        # Summary
        self.summary = "\n".join(
            [p.text or "" for p in self.work.select('.summary > p')])

        # Stats
        self.language = self.find_single_attr("dd.language")
        self.kudos = self.get_number("dd.kudos > a")
        self.words = self.get_number("dd.words")
        self.chapters = self.get_number("dd.chapters > a")
        self.comments = self.get_number("dd.comments > a")
        self.hits = self.get_number("dd.hits")
        self.bookmarks = self.get_number("dd.bookmarks > a")

        total_chapters_str = self.work.select(
            "dd.chapters")[0].contents[1].replace('/', '')
        self.total_chapters = None if total_chapters_str == "?" else int(
            total_chapters_str)

        self.commit()

    def find_single_attr(self, search: str, allow_empty=False) -> str:
        all = self.work.select(search)
        if len(all) != 1:
            if allow_empty and len(all) == 0:
                return None
            raise ValueError(
                f"Expected one match for {search} on {self.id}. "
                "Found {len(all)}")
        return all[0].string

    def find_all(self, search: str):
        all = self.work.select(search)
        return [x.string for x in all]

    def get_number(self, search: str) -> int:
        val = self.find_single_attr(search, True)
        if val:
            return int(val.replace(',', ''))
        return 0

    def add_tag(self, session, tag, type):
        existing = session.scalars(select(Tags).where(
            Tags.title == tag and Tags.work == self.work)).first()
        session.add(existing or Tags(title=tag, work_id=self.id,
                                     type=type))

    def commit(self):
        # with Session(engine) as session:
        #     work = select(Works).where(Works.id == self.id)
        #     if session.scalar(work):
        #         return

        # does not already exists
        with Session(engine) as session:
            author = session.scalars(select(Authors).where(
                Authors.name == self.author)).first() or Authors(name=self.author)
            session.add(author)
            session.commit()

            work = session.scalars(select(Works).where(
                Works.id == self.id)).first() or Works()
            
            for key in inspect(Works).c:
                setattr(work, key.name, self.__dict__[key.name])

            work.author = author.id

            if type(work.rating) != int:
                work.rating = RATINGS[work.rating]

            session.add(work)

            for tag in self.freeforms:
                self.add_tag(session, tag, TAG_TYPES["freeform"])
            for tag in self.warnings:
                self.add_tag(session, tag, TAG_TYPES["warning"])
            for tag in self.characters:
                self.add_tag(session, tag, TAG_TYPES["character"])
            for tag in self.relationships:
                self.add_tag(session, tag, TAG_TYPES["relationship"])
            for tag in self.categories:
                self.add_tag(session, tag, TAG_TYPES["category"])
            for fandom in self.fandoms:
                existing = session.scalars(select(Fandoms).where(
                    Fandoms.title == fandom and Fandoms.work == self.work)).first()
                session.add(existing or Fandoms(title=fandom, work_id=self.id))
            session.commit()

    def __str__(self) -> str:
        return f"""ID: {self.id}
Author: {self.author}
Heading: {self.heading}
Rating: {self.rating}
Category: {self.categories}
Completed: {self.completed}
Warnings: {self.warnings}
Last Updated: {self.last_updated}
---
Fandoms: {self.fandoms}
---
Summary: {self.summary}
---
Characters: {self.characters}
Relationships: {self.relationships}
Freeform: {self.freeforms}
---
Kudos: {self.kudos}
Words: {self.words}
Chapters: {self.chapters}
Comments: {self.comments}
Hits: {self.hits}
Bookmarks: {self.bookmarks}
Total Chapters: {self.total_chapters}
        """
