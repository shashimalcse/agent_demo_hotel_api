from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
import jwt
from jwt.exceptions import InvalidTokenError

from pydantic import BaseModel

security = HTTPBearer()

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

async def validate_token(
    security_scopes: SecurityScopes,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    """
    Decode JWT without verifying its signature, and then validate the scopes.
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            options={"verify_signature": False},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not decode token",
        )

    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Missing 'sub' in token",
        )

    token_scopes = payload.get("scope", "").split()
    # Check that the token has ALL the required scopes
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=401,
                detail="Not enough permissions",
            )

    return TokenData(username=username, scopes=token_scopes)
