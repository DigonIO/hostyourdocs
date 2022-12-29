from fastapi import HTTPException, status

from hyd.backend.util.const import HEADERS

####################################################################################################
#### Internal Exceptions
####################################################################################################


class HydError(Exception):
    """Generic i2d server exception."""


class UsernameError(HydError):
    ...


class VerificationError(HydError):
    "JTW Verification Error"


class UnknownEntryError(HydError):
    pass


####################################################################################################
#### HTTP Exceptions
####################################################################################################

HTTPException_USER_DISABLED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is disabled!",
    headers=HEADERS,
)

HTTPException_NO_PERMISSION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not enough permissions!",
    headers=HEADERS,
)

HTTPException_UNKNOWN_PROJECT = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unknown project ID!",
    headers=HEADERS,
)
