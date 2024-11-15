# routes/wallet.py
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

from config import AppConfig 
load_dotenv()

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed


# def decode_jwt_token(access_token: str):
#     try:
#         payload = jwt.decode(access_token, AppConfig.SECRET_KEY, algorithms=[AppConfig.ALGORITHM])
#         user_info = {"userid": payload.get("sub"), "email": payload.get("email")}
#         return user_info
#     except jwt.ExpiredSignatureError:
#         raise Exception("Token has expired")
#     except jwt.JWTError as e:
#         raise Exception(f"Invalid token: {str(e)}")


# Define the /wallet route
@router.get("/wallet", response_class=HTMLResponse)
async def read_wallet(request: Request, access_token: str = Cookie(None)):

    if not access_token:
        return templates.TemplateResponse("error.html", {"request": request, "active_page": "error", "exception": "No token provided"})

    try:
        user_info = decode_jwt_token(access_token)
        user_id = user_info["userid"]
        user_email = user_info["email"]
        print(user_id)
        print(user_email)

    except Exception as e:
        error_message = str(e)  
        return templates.TemplateResponse("error.html", {"request": request, "active_page": "error", "exception": error_message})
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token error: {error_message}")
    
    if (user_email):
        path="./"+user_email+"/vault.stronghold"

    print("print################# :"+ user_email)

    client_options = ClientOptions(nodes=[NodeConfig.NODE_URL])
    STRONGHOLD_PASSWORD = NodeConfig.STRONGHOLD_PASSWORD
    STRONGHOLD_SNAPSHOT_PATH = path #NodeConfig.STRONGHOLD_SNAPSHOT_PATH

    # Setup Stronghold secret manager
    secret_manager = StrongholdSecretManager(
        STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)

    
    wallet = Wallet(
        client_options=client_options,
        coin_type=CoinType.SHIMMER,
        secret_manager=secret_manager
    )
    account = wallet.get_account('Alice')

# Sync account with the node
    _balance = account.sync()

    # Just calculate the balance with the known state
    balance = account.get_balance()
    print(f'Balance {json.dumps(balance.as_dict(), indent=4)}')










    # wallet = Wallet(NodeConfig.STRONGHOLD_SNAPSHOT_PATH)

    # if 'STRONGHOLD_PASSWORD' not in os.environ:
    #     raise Exception(".env STRONGHOLD_PASSWORD is undefined, see .env.example")

    # wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])
    # account = wallet.get_account('Alice')

    # address = account.generate_ed25519_addresses(1)
    # print('Generated address:', address[0].address)

    return templates.TemplateResponse("wallet.html", {"request": request, "active_page": "wallet"})


@router.post("/wallet")
async def register_user(
    request: Request, access_token: str = Cookie(None)):
    
    #node_url = os.environ.get('NODE_URL', 'https://api.testnet.shimmer.network')
    #print(str(node_url))

    # #node_url = NodeConfig.NODE_URL
    client_options = ClientOptions(nodes=[NodeConfig.NODE_URL])
    STRONGHOLD_PASSWORD = NodeConfig.STRONGHOLD_PASSWORD
    STRONGHOLD_SNAPSHOT_PATH = NodeConfig.STRONGHOLD_SNAPSHOT_PATH
    WALLET_DB_PATH = NodeConfig.WALLET_DB_PATH
 
    user_info = get_current_user(request, access_token) 
    if(user_info.email):
        path="./"+user_info.email+"/vault.stronghold"

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
    
    
    # secret_manager = StrongholdSecretManager(
    # NodeConfig.STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)


    
    # Setup Stronghold secret manager
    # secret_manager = StrongholdSecretManager(
    #     STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)
    


    # if os.path.exists(WALLET_DB_PATH):
    #     os.remove(WALLET_DB_PATH)
    #     print("Existing Stronghold vault and accounts deleted.")
    # else:
    #     print("No existing Stronghold vault found.")


    # # Setup Stronghold secret manager
    # secret_manager = StrongholdSecretManager(
    #     WALLET_DB_PATH, STRONGHOLD_PASSWORD)

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


    return JSONResponse(content={
        "wallet_id": str(address.address),
        "mnemonic": mnemonic
    })
    
          