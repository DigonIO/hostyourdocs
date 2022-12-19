class HydError(Exception):
    """Generic i2d server exception."""


class UsernameError(HydError):
    ...


class VerificationError(HydError):
    "JTW Verification Error"


class UnknownEntryError(HydError):
    pass
