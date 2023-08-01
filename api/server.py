import pymysql
import uvicorn
from fastapi import FastAPI, Response, Depends, File, UploadFile, Form, Body, HTTPException, status, encoders
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import Json

from DB.network_crud import add_network, get_networks_devices
from DB.user_crud import add_user, technician_authorization
from auth.auth_handler import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, \
    get_password_hash
from auth.auth_models import Token
from models.entities import Network, User, UserInDB
from services.file_handler import open_pcap_file, analyze_pcap_file

app = FastAPI()


@app.get("/")
async def root():
    return "welcome to IT4all😀"


@app.post("/upload_pcap_file")
async def upload_pcap_file(pcap_file: UploadFile = File(...), network: Json = Body(...),
                           current_user: User = Depends(get_current_user)):
    network_model = Network(**network)

    is_authorized = await technician_authorization(current_user.ID, network_model.client_id)
    if not is_authorized:
        raise HTTPException(status_code=403, detail="You are not authorized to access this client.")

    try:
        network_id = await add_network(network_model)
        packets = await open_pcap_file(pcap_file)
        await analyze_pcap_file(packets, network_id)
    except Exception as e:
        raise e
        # raise HTTPException(status_code=404,detail="bgbj")

    return f"network created with id:{network_id}"


@app.get("/view_network/{network_id}")
async def view_network(network_id: int, current_user: User = Depends(get_current_user)):
    # TODO: users authorization
    # TODO: get devices and connections
    pass


@app.get("/devices/{network_id}")
async def get_filtered_devices(network_id: int, mac_address: str = None, vendor: str = None,
                               current_user: User = Depends(get_current_user)):
    # TODO: users authorization
    # TODO: get networks devices by filter
    try:
        devices = await get_networks_devices(network_id, mac_address, vendor)
        if not devices:
            raise HTTPException(status_code=404, detail="network not found")
        return devices
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/sign_up")
async def sign_up(pcap_file: UploadFile = None, user: Json = Body(...), password: str = Body(...)):
    hashed_password = get_password_hash(password)
    user_in_db = UserInDB(**user, HashedPassword=hashed_password)
    try:
        user_id = await add_user(user_in_db)
    except Exception as e:
        # TODO: error logging
        raise HTTPException(status_code=500, detail="Internal server error")
    return f"user added with id:{user_id}"


@app.post("/login", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # TODO: add username in data
    access_token = create_access_token(
        data={"email": user.Email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="info")
