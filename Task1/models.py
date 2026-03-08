from datetime import datetime
from abc import ABC, abstractmethod
import logging

# add log in password_changes.log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-7s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("password_changes.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PasswordManager")

# set password rule
class PasswordRule:
    def __init__(self, max_length: int, require_special: bool, numbers_only: bool):
        self._max_length = max_length
        self._require_special = require_special
        self._numbers_only = numbers_only

    def get_max_length(self) -> int:
        return self._max_length

    def get_require_special(self) -> bool:
        return self._require_special

    def get_numbers_only(self) -> bool:
        return self._numbers_only

    def set_max_length(self, value: int):
        self._max_length = value

    def set_require_special(self, value: bool):
        self._require_special = value

    def set_numbers_only(self, value: bool):
        self._numbers_only = value


# common function
class BaseEntry(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        pass


class PasswordEntry(BaseEntry):
    def __init__(
        self,
        site: str,
        username: str,
        password: str,
        expiry_date: datetime,
        file_path: str = None
    ):
        self._log_changes = False
        self._site = site.strip() if site else ""
        self._username = username.strip() if username else ""
        self._password = password
        self._expiry_date = expiry_date
        self._file_path = file_path

        logger.info("CREATED  %-22s | %s", self._site, self)

        self._log_changes = True

    def __repr__(self) -> str:
        """Developer-friendly representation (used in logs, debugger, repr())"""
        pw_hidden = f"***{len(self._password)} chars***" if self._password else "—"
        file_part = f", file={self._file_path!r}" if self._file_path else ""
        return (
            f"PasswordEntry(site={self._site!r}, "
            f"username={self._file_path!r}, "
            f"password={pw_hidden}, "
            f"expiry={self._expiry_date.strftime('%Y-%m-%d')}{file_part})"
        )

    def __str__(self) -> str:
        return f"{self._site} ({self._username}) – expires {self._expiry_date.strftime('%Y-%m-%d')}"

    def __setattr__(self, name: str, value) -> None:
        """
        Log every attribute change after initialization
        """
        if name == '_log_changes':
            object.__setattr__(self, name, value)
            return

        old_value = getattr(self, name, None) if hasattr(self, name) else None

        object.__setattr__(self, name, value)

        if getattr(self, '_log_changes', False):
            short_name = name.lstrip('_')
            logger.info(
                "CHANGE   %-22s | %-12s : %r → %r",
                self._site or "(no site)",
                short_name,
                old_value,
                value
            )

    def get_site(self) -> str:
        return self._site

    def get_username(self) -> str:
        return self._username

    def get_password(self) -> str:
        return self._password

    def get_expiry_date(self) -> datetime:
        return self._expiry_date

    def get_file_path(self) -> str | None:
        return self._file_path

    def set_site(self, value: str):
        self._site = value.strip() if value else ""

    def set_username(self, value: str):
        self._username = value.strip() if value else ""

    def set_password(self, value: str):
        self._password = value

    def set_expiry_date(self, value: datetime):
        self._expiry_date = value

    def set_file_path(self, value: str | None):
        self._file_path = value

    def to_dict(self) -> dict:
        """
        format data
        """
        return {
            'site': self._site,
            'username': self._username,
            'password': self._password,
            'expiry_date': self._expiry_date.strftime("%Y-%m-%d"),
            'file_path': self._file_path
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        format data
        """
        expiry = datetime.strptime(data['expiry_date'], "%Y-%m-%d")
        return cls(
            site=data['site'],
            username=data['username'],
            password=data['password'],
            expiry_date=expiry,
            file_path=data.get('file_path')
        )