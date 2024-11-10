from dotenv import load_dotenv
import os
  
class Config:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "dbpassword")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    #DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "isaid")

config = Config()

class AppConfig:
    load_dotenv() # Load environment variables from a .env file
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

appConfig = AppConfig()


class NodeConfig:
    load_dotenv() # Load environment variables from a .env file
    NODE_URL = os.getenv("NODE_URL")
    STRONGHOLD_PASSWORD = os.getenv("STRONGHOLD_PASSWORD")
    STRONGHOLD_SNAPSHOT_PATH = os.getenv("STRONGHOLD_SNAPSHOT_PATH")

nodeConfig = NodeConfig()