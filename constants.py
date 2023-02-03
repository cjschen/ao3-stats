from re import L
from strenum import StrEnum

# Current Fandom

FANDOM = "少女☆歌劇 レヴュー・スタァライト | Shoujo Kageki Revue Starlight (Anime)"
BASE_URL = f"https://archiveofourown.org/tags/{FANDOM}/works"
START = 135
END = 136
TEST_CONST = "test"

# Constants

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