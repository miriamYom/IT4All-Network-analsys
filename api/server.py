from typing import Dict

import pymysql
import aiomysql
import uvicorn
from fastapi import FastAPI, Response, Depends, File, UploadFile, Form, Body,HTTPException, status, encoders
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pydantic import Json

from auth.auth_handler import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
from auth.auth_models import Token
from models.entities import Network
from DB.DB_manager import fake_db
from DB.crud import add_network, ClientNotFoundError, get_networks_devices
from services.file_handler import open_pcap_file

app = FastAPI()


@app.get("/")
async def root():
    return "welcome to IT4all😀"


@app.post("/upload_pcap_file")
async def upload_pcap_file(pcap_file: UploadFile = File(...), network: Json = Body(...)):
    print(network)
    print(type(network))

    # TODO: users authorization
    # TODO: add network to DB
    network_model = Network(**network)
    try:
        id = add_network(network_model)
    except pymysql.Error as e:
        raise e
        # raise HTTPException(status_code=404,detail="bgbj")
    # TODO: read file
    await open_pcap_file(pcap_file)
    # TODO: analyze file

    # TODO: return network id
    return f"network created with id:{id}"


@app.get("/view_network/{network_id}")
async def view_network(network_id: int):
    # TODO: users authorization
    # TODO: get devices and connections
    pass


@app.get("/devices/{network_id}")
async def get_filtered_devices(network_id: int, mac_address: str = None, vendor: str = None):
    # TODO: users authorization
    # TODO: get networks devices by filter
    try:
        devices = await get_networks_devices(network_id, mac_address, vendor)
        if not devices:
            raise HTTPException(status_code=404, detail="network not found")
        return devices
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/login", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="info")
