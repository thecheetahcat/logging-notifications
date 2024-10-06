from dotenv import load_dotenv
import os

load_dotenv()

# ---------- element credentials ---------- #
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
ROOM_ID = os.getenv("ROOM_ID")

# ---------- file names ---------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_PATH = os.path.join(BASE_DIR, "store")
CREDENTIALS_FILE = "credentials.json"

# ---------- homeserver ---------- #
HOME_SERVER = "https://matrix.org"

# ---------- device name ---------- #
DEVICE_NAME = "abitrager"


# ---------- errors ---------- #
class MatrixLoginError(Exception):
    """
    Raised when login attempt fails.
    """
    pass
