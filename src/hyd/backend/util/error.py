from fastapi import HTTPException, status

from hyd.backend.util.const import HEADERS

####################################################################################################
#### Internal Exceptions
####################################################################################################


class HydError(Exception):
    """Generic HostYourDocs exception."""


class NameError(HydError):
    """Raised if a name is not available."""


class PrimaryTagError(HydError):
    """Raised if a second primary tag would be created for a project."""


class VerificationError(HydError):
    """Raised if an error occurs while JTW verification."""


class UnknownEntryError(HydError):
    """Raised if a db table could not be found."""


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
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Unknown project ID!",
    headers=HEADERS,
)
