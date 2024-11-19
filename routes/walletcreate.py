# routes/walletcreate.py
from fastapi import APIRouter, Request, Cookie, HTTPException, status
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes
from fastapi.responses import JSONResponse
import httpx
from config import NodeConfig 
import json
import jwt

from auth import get_current_user, decode_jwt_token
import os
from dotenv import load_dotenv
from iota_sdk import (ClientOptions, CoinType, StrongholdSecretManager, Utils,
                      Wallet)
from iota_sdk import Client, NodeIndexerAPI
from config import AppConfig 

from fastapi.responses import FileResponse
from fastapi import HTTPException


load_dotenv()

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed


# Define the /walletcreate route
@router.get("/walletcreate", response_class=HTMLResponse)
async def read_createwallet(request: Request):
    return templates.TemplateResponse("walletcreate.html", {"request": request, "active_page": "walletcreate"})



# Endpoint to serve the Stronghold vault for download
@router.get("/download_vault/{wallet_name}")
async def download_vault(wallet_name: str):
    # Construct the path to the Stronghold vault
    vault_path = f"./{wallet_name}/vault.stronghold"

    # Check if the file exists
    if not os.path.exists(vault_path):
        raise HTTPException(status_code=404, detail="Vault file not found.")

    # Serve the file as a downloadable response
    return FileResponse(vault_path, media_type='application/octet-stream', filename=f"{wallet_name}_vault.stronghold")



# @router.post("/walletcreate")
# async def create_wallet(request: Request):
#     try:
#         # Parse incoming JSON data
#         data = await request.json()
#         wallet_name = data.get("wallet_name")
#         stronghold_password = data.get("stronghold_password")

#         if not wallet_name or not stronghold_password:
#             raise HTTPException(status_code=400, detail="Wallet name and password are required.")

#         # Logic to create a wallet (replace this with your actual implementation)
#         wallet_id = "unique-wallet-id"
#         mnemonic = "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"

#         # Return the wallet ID and mnemonic as JSON
#         return JSONResponse(content={"wallet_id": wallet_id, "mnemonic": mnemonic})

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

 


# @router.post("/wallet")
# async def register_user(
#     request: Request, access_token: str = Cookie(None)):

@router.post("/walletcreate")
async def read_wallet(request: Request, access_token: str = Cookie(None)):
    try:
        # Parse incoming JSON data
        data = await request.json()
        wallet_name = data.get("wallet_name")
        stronghold_password = data.get("stronghold_password")

        if not wallet_name or not stronghold_password:
            raise HTTPException(status_code=400, detail="Wallet name and password are required.")
    

        # #node_url = NodeConfig.NODE_URL
        client_options = ClientOptions(nodes=[NodeConfig.NODE_URL])
        STRONGHOLD_PASSWORD = NodeConfig.STRONGHOLD_PASSWORD
        STRONGHOLD_SNAPSHOT_PATH = NodeConfig.STRONGHOLD_SNAPSHOT_PATH
        WALLET_DB_PATH = NodeConfig.WALLET_DB_PATH
    
        if(wallet_name):
            path="./"+ wallet_name+"/vault.stronghold"

        NodeConfig.STRONGHOLD_SNAPSHOT_PATH = path

        print("STRONGHOLD_SNAPSHOT_PATH:", NodeConfig.STRONGHOLD_SNAPSHOT_PATH)

        #need to be removed later
        if os.path.exists(NodeConfig.STRONGHOLD_SNAPSHOT_PATH):
            os.remove(NodeConfig.STRONGHOLD_SNAPSHOT_PATH)
            print("Existing Stronghold vault and accounts deleted.")
        else:
            print("No existing Stronghold vault found.")




        secret_manager = StrongholdSecretManager(
        path, STRONGHOLD_PASSWORD)
        

        # Set up and store the wallet.
        client_options = ClientOptions(nodes=[NodeConfig.NODE_URL])

        wallet = Wallet(
            client_options=client_options,
            coin_type=CoinType.SHIMMER,
            secret_manager=secret_manager
        )

        #account = wallet.get_account('Tester')
        wallet.remove_latest_account()

        print({'after wallet'})


        # Store the mnemonic in the Stronghold snapshot, this only needs to be
        # done once.
        mnemonic = Utils.generate_mnemonic()
        print(f'Mnemonic: {mnemonic}')
        wallet.store_mnemonic(mnemonic)


        print({'after mnemonic'})

        account = wallet.create_account('Alice')
        print("Account created:", account.get_metadata())

        address = account.addresses()[0]
        print({address.address})
        print({address.address})
        #print(os.environ['WALLET_DB_PATH'])

        

        # user_info = decode_jwt_token(access_token)
        # user_id = user_info["userid"]
        # user_email = user_info["email"]
        # print(user_id)
        # print(user_email)

        #new_user = User(displayname=displayname, password=password, name=name, email=email, phone=phone)

        # if address != "":
        #      wallet_command(user_id,tblWallet)
        #      print("You are eligible to vote!")
        #      user_id


        return JSONResponse(content={
            "wallet_id": str(address.address),
            "mnemonic": mnemonic,
            "vault_download_link": f"/download_vault/{wallet_name}"
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))