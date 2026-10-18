"""Person: the parent (base) class. User inherits from it."""


class Person:
    """A basic person with a name and an email."""

    def __init__(self, name, email=""):
        """Create a person. The setters below check the values."""
        self.name = name
        self.email = email

    @property
    def name(self):
        """Return the person's name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name. It cannot be empty."""
        value = str(value).strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self):
        """Return the person's email."""
        return self._email

    @email.setter
    def email(self, value):
        """Set the email. It can be empty, but if given it must look like an email."""
        value = str(value).strip()
        if value and ("@" not in value or "." not in value.split("@")[-1]):
            raise ValueError(f"'{value}' is not a valid email address.")
        self._email = value

    def __str__(self):
        """Readable text for printing."""
        return f"{self.name} <{self.email or 'no email'}>"
    