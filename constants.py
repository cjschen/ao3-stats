from re import L
from strenum import StrEnum
# Current Fandom

FANDOM = "少女☆歌劇 レヴュー・スタァライト | Shoujo Kageki Revue Starlight (Anime)"
BASE_URL = f"https://archiveofourown.org/tags/{FANDOM}/works"
START = 135
END = 136

# Constants

CATEGORIES = {
    "F/M" : 1,
    "F/F" : 2,
    "M/M" : 3,
    "Gen" : 4,
    "Multi" : 5,
    "Other" : 6
    }


TAG_TYPES = {
    "character" : 1,
    "warning" : 2,
    "relationship" : 3,
    "freeform": 4,
    "category": 5
}

RATINGS = {
    "General Audiences": 1,
    "Teen And Up Audiences": 2,
    "Mature": 3,
    "Explicit": 4,
    "Not Rated": 5
}


class Warnings(StrEnum):
    NONE = "No Archive Warnings Apply",
    VIOLENCE = "Graphic Depictions Of Violence",
    NONCON = "Rape/Non-Con",
    DEATH = "Major Character Death",
    UNDERAGE = "Underage",
    OPTOUT = "Creator Chose Not To Use Archive Warnings"
class Catagories(StrEnum):
    FM = "F/M",
    FF = "F/F",
    MM = "M/M",
    GEN = "Gen",
    MULTI = "Multi",
    OTHER = "Other"

class Rating(StrEnum):
    G = "General Audiences",
    T = "Teen And Up Audiences",
    M = "Mature",
    E = "Explicit",
    NR = "Not Rated"

class TagTypes(StrEnum):
    CHARACTER = "Characters"
    WARNING = "Warnings"
    RELATIONSHIP  = "Relationship"
    FREEFORM  = "Freeform"
