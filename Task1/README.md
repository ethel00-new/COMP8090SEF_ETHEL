# Task 1 Password Management System

## System Overview
This project is a password and credential management system designed to simplify how users store, generate, manage, and track credentials securely.
It combines a clean Object-Oriented Programming (OOP) architecture with a set of CRUD-based REST APIs, allowing structured password handling with strong maintainability and extensibility.
The system solves several common problems: password reuse, weak password creation, manual expiration tracking, forgot password and unorganized credential file storage.

### Key Features:
- Secure password & credential storage
Store login passwords or credential files such as .pem or .cer to keep all service-related authentication materials in one place.
- Support for uploading credential/key files
Users can upload files tied to a password entry, allowing non-password authentication materials to be stored together.
- Customizable strong password generator
The system provides a flexible password generator supporting:
    - Custom length
    - Optional special characters
    - Numeric-only patterns
    - Optional alphabet-first requirement
    - Password expiration tracking
- Password expiration tracking
Tracks expiry dates and highlights entries that have expired or may require renewal (e.g., near the 90‑day security rotation cycle).
- Password strength checking
Checks for at least 10 characters and 3 out of 4 categories:
uppercase, lowercase, digits, special characters.
- Duplicate password detection
Warns if the same password is reused across different sites.
- Full CRUD REST API
Provides endpoints to:
    - Create password/credential entries
    - Read all saved credentials
    - Update an existing entry
    - Delete entries
    This enables integration with external tools, GUIs, or automation scripts.

## OOP Design 

### Abstraction / ADT
- Abstract Base Class: BaseEntry defines the abstract interface for entries with to_dict() and from_dict() to concrete models implement these methods. 
This hides serialization details behind a stable abstraction.
```python
class BaseEntry(ABC):
    @abstractmethod
    def to_dict(self) -> dict: ...
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict): ...
```
- Generator Strategy Interface: PasswordGenerator is an interface with a single generate() method; StandardPasswordGenerator implements it.
Consumers depend on the abstraction, not the implementation.
```python
class PasswordGenerator:
    def generate(self, rule: PasswordRule) -> str:
        raise NotImplementedError
```

### Encapsulation
- Private State & Getters/Setters: PasswordRule and PasswordEntry store data in “private” attributes (e.g., _max_length, _site) and expose accessors/mutators.
This allows validation/logging and keeps invariants centralized.
```python
class PasswordRule:
    def __init__(self, max_length, require_special, numbers_only):
        self._max_length = max_length
        self._require_special = require_special
        self._numbers_only = numbers_only
    def get_max_length(self) -> int: ...
    def set_max_length(self, value: int): ...
```
- Change Auditing via __setattr__: PasswordEntry overrides __setattr__ to log attribute changes after initialization, encapsulating audit concerns within the entity.
```python
def __setattr__(self, name: str, value) -> None:
```

### Inheritance
- PasswordEntry inherits from BaseEntry and implements its abstract methods, providing concrete serialization (to_dict/from_dict). This demonstrates classical inheritance for shared contracts. 
- StandardPasswordGenerator inherits from PasswordGenerator, enabling different concrete generators under a common type.

### Polymorphism
The service accepts a PasswordGenerator polymorphically: you can swap in any generator that implements generate(rule). By default, it uses StandardPasswordGenerator, but you can inject alternatives for testing or new policies without changing callers.
```python
class PasswordService:
    def __init__(self, storage_file='passwords.json', generator: PasswordGenerator = None):
        self._generator = generator or StandardPasswordGenerator()
```

### Modular Programming
- Service and Models: PasswordService composes PasswordEntry objects and persists them. It also composes a PasswordGenerator. Composition over inheritance allows flexible graph-like collaboration between objects.


## Key Classes 

**PasswordRule**
Encapsulates password generation constraints: max_length, require_special, and numbers_only, with getters/setters for encapsulation and future validation. Used by generators and the UI to drive generation behavior

**PasswordEntry (inherits BaseEntry)**
Represents a password record with site, username, password, expiry_date, and optional file_path.
Notable OOP features:

Change logging via custom __setattr__ (post-init)
Clean __repr__ / __str__ for debug vs. user-friendly text
Serialization to/from dict for persistence boundaries


**PasswordGenerator & StandardPasswordGenerator**
Defines a generator interface and a default implementation. The default implementation respects rules (length, digits, special characters) and shuffles characters for randomness. You can add new generators (e.g., PwDicewareGenerator) without modifying callers.


**PasswordService**
Coordinates application use-cases:

CRUD over PasswordEntry with validation and JSON persistence
Delegates password creation to the injected PasswordGenerator
Utility: is_strong_password, is_repeated_password, is_expired, and file upload collision-safe saving


## How to Run
Follow these steps to set up and launch the app.
```
cd Task1
pip install -r requirements.txt
python main.py
```
Access at http://127.0.0.1:5001
