class I2DServerError(Exception):
    """Generic i2d server exception."""


class UnknownUsernameError(I2DServerError):
    ...


class InvalidPasswordError(I2DServerError):
    ...


class VerificationError(I2DServerError):
    "JTW Verification Error"


class UnkownEntryIdError(I2DServerError):
    pass
