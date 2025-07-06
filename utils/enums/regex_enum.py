from enum import Enum


class RegEx(Enum):
    PASSWORD = (
        r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])([^\s]){5,16}$',
        [
            'password must contain 1 number(0-9)',
            'password must contain 1 uppercase letter',
            'password must contain 1 lowercase letter',
            'password must contain 1 non-alpha numeric number',
            'password is 5-16 characters with no space',
        ]
    )
    FIRST_NAME = (
        r"^[a-zA-Zа-яА-ЯҐґІіЇїЄє'-]{3,20}$",
        'only letters min 2 max 20 ch'
    )
    LAST_NAME = (
        r"^[a-zA-Zа-яА-ЯҐґІіЇїЄє'-]{3,20}$",
        'only letters min 2 max 20 ch'
    )
    PHONE = (
        r'^0\d{9}$',
        'invalid phone number Ex. 097 999 99 99 '
    )
    PROJECT_NAME = (
        r'^[a-zA-Z]{2,20}$',
        'min 2 max 20ch'
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg