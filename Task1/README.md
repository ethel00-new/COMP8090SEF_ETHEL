# 🔐 Password Management System

Password Management System is a **password & credential management system** designed to simplify how users store, generate, manage, and track credentials.

It combines a clean **Object-Oriented Programming (OOP)** architecture with **CRUD-based REST APIs**, solving common problems like password reuse, weak password creation, manual expiration tracking, and unorganized credential storage.

## 📹 Introduction Video
https://youtu.be/996RB4VpN2s
---

## ✨ Key Features

- **Secure password & credential storage**  
    Store login passwords or credential files (.pem, .cer) in one place.
    
- **Credential/key file uploads**  
    Attach authentication files directly to password entries.
    
- **Customizable strong password generator**
    
    - Custom length
    - Optional special characters
    - Numeric-only patterns
    - Alphabet-first requirement
    - Expiration tracking
- **Password expiration tracking**  
    Highlight expired or soon-to-expire entries (e.g., 90‑day rotation cycle).
    
- **Password strength checking**  
    Enforces:
    
    - ≥ 10 characters
    - At least 3 of 4 categories (uppercase, lowercase, digits, special characters).
- **Duplicate password detection**  
    Warns if the same password is reused across different sites.
    
- **Full CRUD REST API**
    
    - Create password/credential entries
    - Read all saved credentials
    - Update existing entries
    - Delete entries

---

## 🧩 OOP Design

### Class & Object
A **class** is the blueprint that defines attributes and methods. An **object** is a concrete instance created from that class. Every object has its own methods that define its behavior.
#### class

```python
class PasswordRule:
class PasswordEntry(BaseEntry):
class PasswordGenerator:
class StandardPasswordGenerator(PasswordGenerator):
class PasswordService:
```
#### Object

```python
# Method calls on objects
entries = service.get_all_passwords()
pw = service.generate_password(rule)
service.add_password(entry, rule)
expired = service.is_expired(e)
strong = service.is_strong_password(pw)
```

### Abstraction / ADT

- **BaseEntry (Abstract Class)**  
BaseEntry is an Abstract Base Class that defines the serialization interface (ADT) `to_dict`, `from_dict`.

```python
class BaseEntry(ABC):
    @abstractmethod
    def to_dict(self) -> dict: ...
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict): ...
```

- **PasswordGenerator (Interface)**  
    Strategy pattern for password generation.

```python
class PasswordGenerator:
    def generate(self, rule: PasswordRule) -> str:
        raise NotImplementedError
```

### Encapsulation

- Private attributes with getters/setters for validation.
- Change auditing via `__setattr__`.

```python
class PasswordRule:
    def __init__(self, max_length, require_special, numbers_only):
        self._max_length = max_length
        self._require_special = require_special
        self._numbers_only = numbers_only

    def get_max_length(self) -> int:
    def set_max_length(self, value: int):
```

### Inheritance

- `PasswordEntry` inherits from `BaseEntry`.
- `StandardPasswordGenerator` inherits from `PasswordGenerator`.

### Polymorphism

- `PasswordService` accepts any `PasswordGenerator`.

```python
class PasswordService:
    def __init__(self, storage_file='passwords.json', generator: PasswordGenerator = None):
        self._generator = generator or StandardPasswordGenerator()
```

### Modular Programming
Service and Main (It can call the controller, it is actually an MVC model.)
Able to call other classes from different files
```python
from models import PasswordRule, PasswordEntry, logger
from services import PasswordService
```

### Magic Methods
Python magic methods are special methods with double underscores that customize object behavior.
```python
    def __repr__(self) -> str:
    def __str__(self) -> str:
    def __setattr__(self, name: str, value) -> None:
```
---

## 🚀 How to Run

```bash
cd Task1
pip install -r requirements.txt
python main.py
```

Access at: http://127.0.0.1:5001