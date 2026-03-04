import json
from datetime import datetime, timedelta
import random
import string
import os
from models import PasswordRule, PasswordEntry, logger

ALLOWED_SPECIAL = "@#$%&"


class PasswordGenerator:
    def generate(self, rule: PasswordRule) -> str:
        raise NotImplementedError


class StandardPasswordGenerator(PasswordGenerator):
    def generate(self, rule: PasswordRule) -> str:
        length = max(5, rule.get_max_length())
        if rule.get_numbers_only():
            chars = string.digits
            min_digits = length
        else:
            chars = string.ascii_letters + string.digits
            if rule.get_require_special():
                chars += ALLOWED_SPECIAL
            min_digits = 3

        digits_part = ''.join(random.choice(string.digits) for _ in range(min_digits))
        remaining_length = length - min_digits
        if remaining_length > 0:
            rest = ''.join(random.choice(chars) for _ in range(remaining_length))
            password = digits_part + rest
            password = ''.join(random.sample(password, len(password)))
        else:
            password = digits_part
        return password


class PasswordService:
    def __init__(self, storage_file='passwords.json', generator: PasswordGenerator = None):
        self._storage_file = storage_file
        self._passwords = self._load_passwords()
        self._generator = generator or StandardPasswordGenerator()

    def _load_passwords(self):
        try:
            with open(self._storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                entries = [PasswordEntry.from_dict(entry) for entry in data]
                for entry in entries:
                    entry._log_changes = True
                return entries
        except FileNotFoundError:
            return []
        except Exception as e:
            logger.error(f"Error loading passwords: {e}")
            return []

    def _save_passwords(self):
        try:
            with open(self._storage_file, 'w', encoding='utf-8') as f:
                json.dump(
                    [entry.to_dict() for entry in self._passwords],
                    f,
                    indent=4,
                    ensure_ascii=False
                )
        except Exception as e:
            logger.error(f"Error saving passwords: {e}")

    def add_password(self, entry: PasswordEntry, rule: PasswordRule):
        if not entry.get_site() or not entry.get_username():
            raise ValueError("Site and username are required.")
        if not entry.get_password() and not entry.get_file_path():
            raise ValueError("Must provide at least a password or a file.")
        entry._log_changes = True
        self._passwords.append(entry)
        self._save_passwords()

    def update_password(self, index: int, entry: PasswordEntry, rule: PasswordRule):
        if index < 0 or index >= len(self._passwords):
            raise IndexError("Invalid password entry index")
        if not entry.get_site() or not entry.get_username():
            raise ValueError("Site and username are required.")
        if not entry.get_password() and not entry.get_file_path():
            raise ValueError("Must provide at least a password or a file.")
        entry._log_changes = True
        self._passwords[index] = entry
        self._save_passwords()

    def delete_password(self, index: int):
        if index < 0 or index >= len(self._passwords):
            raise IndexError("Invalid password entry index")
        entry = self._passwords[index]
        logger.info("DELETED  %-22s | %s", entry.get_site(), entry)
        del self._passwords[index]
        self._save_passwords()

    def get_all_passwords(self):
        return self._passwords

    def is_expired(self, entry: PasswordEntry) -> bool:
        return datetime.now() > entry.get_expiry_date()

    def generate_password(self, rule: PasswordRule) -> str:
        return self._generator.generate(rule)

    def upload_file(self, file_storage) -> str | None:
        if not file_storage or not file_storage.filename:
            return None
        filename = file_storage.filename.replace('/', '_').replace('\\', '_')
        os.makedirs("files", exist_ok=True)
        dest_path = os.path.join("files", filename)
        base, ext = os.path.splitext(dest_path)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = f"{base} ({counter}){ext}"
            counter += 1
        file_storage.save(dest_path)
        return dest_path

    def is_strong_password(self, password: str) -> bool:
        if not password or len(password) < 10:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in ALLOWED_SPECIAL for c in password)
        category_count = sum([has_upper, has_lower, has_digit, has_special])
        return len(password) >= 10 and category_count >= 3

    def is_repeated_password(self, password: str, exclude_index: int = -1) -> bool:
        if not password:
            return False
        for i, entry in enumerate(self._passwords):
            if i == exclude_index:
                continue
            if entry.get_password() == password:
                return True
        return False