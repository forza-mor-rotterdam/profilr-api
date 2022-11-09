from typing import Union
import os
from fastapi import FastAPI, Header, status,HTTPException
from data import meldingen
from fastapi.responses import JSONResponse
app = FastAPI()


def authenticate_user(authorization_header: str):
    auth_parts = authorization_header.split(" ") if authorization_header else []
    if len(auth_parts) == 2 and auth_parts[0] == "Bearer" and auth_parts[1] == os.getenv('MSB_USER_TOKEN'):
        return True
    return False


@app.post("/sbmob/api/msb/openmeldingen")
async def root(authorization: Union[str, None] = Header(default=None)):
    user = authenticate_user(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    melding_list = [m.get("list") for m in meldingen() if m.get("detail")]
    return {
        "success": True,
        "result": melding_list,
    }


@app.get("/sbmob/api/msb/melding/{item_id}")
async def detail(item_id, authorization: Union[str, None] = Header(default=None)):
    user = authenticate_user(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    melding_dict = {m.get("detail").get("result").get("id"): m.get("detail") for m in meldingen() if m.get("detail")}
    melding = melding_dict.get(int(item_id))
    if not melding:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return melding


@app.get("/sbmob/api/msb/melding/{item_id}/mutatieregels")
async def mutatieregels(item_id, authorization: Union[str, None] = Header(default=None)):
    user = authenticate_user(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    melding_dict = {m.get("detail").get("result").get("id"): m.get("mutatieregels") for m in meldingen() if m.get("mutatieregels")}
    melding = melding_dict.get(int(item_id))
    if not melding:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return {
        "success": True,
        "result": melding,
    }


@app.get("/sbmob/api/gebruikerinfo")
async def gebruikerinfo(authorization: Union[str, None] = Header(default=None)):
    user = authenticate_user(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return {
        "success": True,
        "result": {
            "user": "G313000",
            "naam": "Duck D. (Donald)",
            "rollen": [
                "msb.verantwoordlijken",
            ],
            "gebruikersinstellingen": [],
        },
    }


@app.post("/sbmob/api/login")
async def login():
    return {
        "success": True,
        "result":os.getenv('MSB_USER_TOKEN'),
    }

@app.get("/sbmob/api/logout")
async def logout():
    return {
        "success": True,
        "result":"",
    }
