from bs4 import BeautifulSoup 

class Work: 
    def __init__(self, work: BeautifulSoup) -> None:
        self.work = work

        self.id = self.work['id'].split("_")[1]
        self.author = self.find_single_attr("a[rel=author]")
        self.last_updated = self.find_single_attr('.datetime')

        # Required Tags
        self.rating = self.find_single_attr(".rating > span")
        self.catagories = self.find_single_attr(".category > span").split(", ")
        self.completed = self.find_single_attr('.iswip > span')
        self.warnings = self.find_single_attr('.warnings > span').split(", ")

        # Other tags
        self.relationships = self.find_all(".relationships > .tag")
        self.characters = self.find_all(".characters > .tag")
        self.freeforms = self.find_all(".freeforms > .tag")

        # Summary
        self.summary = "\n".join([ p.string for p in self.work.select('.summary > p') ])

        # Stats 
        self.language = self.find_single_attr("dd.language")
        self.kudos = self.get_number("dd.kudos > a")
        self.words = self.get_number("dd.words")
        self.chapters = self.get_number("dd.chapters > a")
        self.comments = self.get_number("dd.comments > a")
        self.hits = self.get_number("dd.hits")
        self.bookmarks = self.get_number("dd.bookmarks > a")

        total_chapters_str = self.work.select("dd.chapters")[0].contents[1].replace('/', '')
        self.total_chapters = None if total_chapters_str == "?" else int(total_chapters_str)
        
    def find_single_attr(self, search: str, allow_empty = False) -> str:
        all = self.work.select(search)
        if len(all) != 1:
            if allow_empty and len(all) == 0:
                return None
            raise ValueError(f"Expected one match for {search} on {self.id}. Found {len(all)}")
        return all[0].string

    def find_all(self, search: str): 
        all = self.work.select(search)
        return [ x.string for x in all ] 

    def get_number(self, search: str) -> int:
        val =  self.find_single_attr(search, True)
        if val:
            return int(val.replace(',',''))
        return 0

    def __str__(self) -> str:
        return f"""ID: {self.id}
Author: {self.author}
Rating: {self.rating}
Category: {self.catagories}
Completed: {self.completed}
Warnings: {self.warnings}
Last Updated: {self.last_updated}
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