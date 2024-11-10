# routes/wallet.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes
from fastapi.responses import JSONResponse
from config import NodeConfig 

import os
from dotenv import load_dotenv
from iota_sdk import (ClientOptions, CoinType, StrongholdSecretManager, Utils,
                      Wallet)
load_dotenv()

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

# Define the /wallet route
@router.get("/wallet", response_class=HTMLResponse)
async def read_wallet(request: Request):
    return templates.TemplateResponse("wallet.html", {"request": request, "active_page": "wallet"})


@router.post("/wallet")
async def register_user(
    request: Request
):
    
    #node_url = os.environ.get('NODE_URL', 'https://api.testnet.shimmer.network')
    #print(str(node_url))

    node_url = NodeConfig.NODE_URL
    client_options = ClientOptions(nodes=[node_url])
    STRONGHOLD_PASSWORD = NodeConfig.STRONGHOLD_PASSWORD
    STRONGHOLD_SNAPSHOT_PATH = NodeConfig.STRONGHOLD_SNAPSHOT_PATH

    # A password to encrypt the stored data.
    # WARNING: Never hardcode passwords in production code.
    # STRONGHOLD_PASSWORD = os.environ.get(
    #     'STRONGHOLD_PASSWORD', 'a-secure-password')
    
    

    # # The path to store the account snapshot.
    # STRONGHOLD_SNAPSHOT_PATH = 'vault.stronghold'


    if os.path.exists(STRONGHOLD_SNAPSHOT_PATH):
        os.remove(STRONGHOLD_SNAPSHOT_PATH)
        print("Existing Stronghold vault and accounts deleted.")
    else:
        print("No existing Stronghold vault found.")

    # Setup Stronghold secret manager
    secret_manager = StrongholdSecretManager(
        STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)

    # Set up and store the wallet.
    client_options = ClientOptions(nodes=[node_url])

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

    return JSONResponse(content={
        "wallet_id": str(address.address),
        "mnemonic": mnemonic
    })
    #print(os.environ['WALLET_DB_PATH'])
          