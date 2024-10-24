from datetime import date
from string import ascii_letters

from src.enums import Sex


def data_validated(args: list[str]) -> bool:
    lname, fname, p, bday, s = args
    if s not in Sex.values():
        return False
    try:
        bday = date.fromisoformat(bday)
    except ValueError:
        return False
    
    names = [lname, fname, p]
    for name in names:
        if len(name) < 3 or len(name) > 50:
            return False

    for name in [lname, fname, p]:
        for char in name:
            if char not in ascii_letters:
                return False
    
    return True
