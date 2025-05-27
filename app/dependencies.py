from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
import jwt
from jwt.exceptions import InvalidTokenError

from pydantic import BaseModel

security = HTTPBearer()

class Actor(BaseModel):
    sub: str | None = None

class TokenData(BaseModel):
    sub: str | None = None
    act: Actor = None
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

    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(
            status_code=401,
            detail="Missing 'sub' in token",
        )
    
    # Extract actor information if available
    act_claim = payload.get("act")
    if act_claim is None:
        act = Actor(sub=None)
    elif isinstance(act_claim, dict):
        try:
            sub = act_claim.get("sub", sub)  # Use sub from act if available
            act = Actor(sub=sub)
            print(f"Actor sub: {act.sub}")  # Debugging output
        except Exception as e:
            # Log the error and default to no actor
            print(f"Warning: Could not parse act claim {act_claim}: {e}")
            act = Actor(sub=None)
    else:
        # Handle case where act is not a dict
        print(f"Warning: act claim is not a dict: {act_claim}")
        act = Actor(sub=None)

    token_scopes = payload.get("scope", "").split()
    # Check that the token has ALL the required scopes
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=401,
                detail="Not enough permissions",
            )

    return TokenData(sub=sub, act=act, scopes=token_scopes)
