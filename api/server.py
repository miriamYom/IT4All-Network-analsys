from typing import Dict

import uvicorn
from fastapi import FastAPI, Response, Depends, File, UploadFile, Form, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Json

from models.entities import Network
from DB.DB_manager import fake_db
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
    fake_db[network_model.id] = network_model
    # TODO: read file
    await open_pcap_file(pcap_file)
    # TODO: analyze file

    # TODO: return network id
    return network_model.id


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
