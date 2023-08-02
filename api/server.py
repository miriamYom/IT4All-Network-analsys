from typing import Union

import pymysql
import uvicorn
from fastapi import FastAPI, Response, Depends, File, UploadFile, Form, Body, HTTPException, status, encoders, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.responses import JSONResponse
from DB.client_crud import ClientNotFoundError, is_exist_client_by_id, is_exist_client_by_network
from DB.user_crud import technician_authorization, UnAuthorizedError
from auth_api import router as auto_api_router
from pydantic import Json

from DB.network_crud import add_network, get_networks_devices, DeviceDoesntExistError, get_network_details

from auth.auth_handler import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, \
    get_password_hash
from auth.auth_models import Token
from models.entities import Network, User, UserInDB
from services.file_handler import open_pcap_file
from services.packet_analyzer import analyze_pcap_file

app = FastAPI()


@app.get("/")
async def root(current_user: User = Depends(get_current_user)):
    await is_exist_client_by_id(1)
    await technician_authorization(current_user.ID, 1)
    return "welcome to IT4all😀"


@app.post("/upload_pcap_file")
async def upload_pcap_file(pcap_file: UploadFile = File(...), network: Json = Body(...),
                           current_user: User = Depends(get_current_user)):
    try:
        network_model = Network(**network)
        await is_exist_client_by_id(network_model.client_id)
        await technician_authorization(current_user.ID, network_model.client_id)
        network_id = await add_network(network_model)
        packets = await open_pcap_file(pcap_file)
        await analyze_pcap_file(packets, network_id)
        return f"network created with id:{network_id}"
    except ClientNotFoundError as e:
        raise HTTPException(status_code=404, detail=e)
    except UnAuthorizedError as e:
        raise HTTPException(status_code=403, detail=e)
    except Exception as e:
        raise HTTPException(status_code=403, detail=e)


@app.get("/view_network/{network_id}")
async def view_network(network_id: int, current_user: User = Depends(get_current_user)):
    try:
        client_id = await is_exist_client_by_network(network_id)
        await technician_authorization(current_user.ID, client_id)
        network_details = await get_network_details(network_id)
        return network_details
    except ClientNotFoundError as e:
        raise HTTPException(status_code=404, detail=e)
    except UnAuthorizedError as e:
        raise HTTPException(status_code=403, detail=e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@app.get("/devices")
async def get_filtered_devices(network_id: int = None, mac_address: str = None, vendor: str = None,
                               client_id: int = None, current_user: User = Depends(get_current_user)):
    try:
        client_id_for_query: Union[int, None] = client_id
        if client_id:
            await is_exist_client_by_id(client_id)
        else:
            client_id = await is_exist_client_by_network(network_id)
        await technician_authorization(current_user.ID, client_id)
        devices = await get_networks_devices(network_id, mac_address, vendor, client_id_for_query)
        if not devices:
            raise HTTPException(status_code=404, detail="network not found")
        return devices
    except ClientNotFoundError as e:
        raise HTTPException(status_code=404, detail=e)
    except UnAuthorizedError as e:
        raise HTTPException(status_code=403, detail=e)
    except DeviceDoesntExistError as e:
        raise HTTPException(status_code=404, detail=e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


app.include_router(auto_api_router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="info")
