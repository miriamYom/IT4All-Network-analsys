from typing import Dict

import pymysql
import uvicorn
from fastapi import FastAPI, Response, Depends, File, UploadFile, Form, Body,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Json

from models.entities import Network
from DB.DB_manager import fake_db
from DB.crud import add_network, ClientNotFoundError, add_network2
from services.file_handler import open_pcap_file

app = FastAPI()


@app.get("/")
async def root():
    return "welcome to IT4all😀"


@app.post("/upload_pcap_file")
async def upload_pcap_file(pcap_file: UploadFile = File(...), network: Json = Body(...)):
    # print(network)
    # print(type(network))

    # TODO: users authorization
    # TODO: add network to DB
    network_model = Network(**network)
    try:
        id=add_network2(network_model)
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


@app.get("/filtered_devices/{network_id}")
async def get_filtered_devices(network_id: int, mac_address: str, vendor: str):
    # TODO: users authorization
    # TODO: get networks devices by filter
    pass


@app.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: implement login
    pass


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="info")
