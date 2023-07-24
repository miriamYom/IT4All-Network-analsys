import uvicorn
from fastapi import FastAPI, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.network import Network

app = FastAPI()


@app.get("/")
async def root():
    return "welcome to IT4all😀"


@app.post("/upload_pcap_file")
async def upload_pcap_file(network: Network, pcap_file=None):
    # TODO: users authorization
    # TODO: add network to DB
    # TODO: read file
    # TODO: analyze file
    # TODO: return network id
    pass


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
