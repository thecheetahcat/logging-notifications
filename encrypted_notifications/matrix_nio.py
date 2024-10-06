from encrypted_notifications.constants import (
    USERNAME,
    PASSWORD,
    ROOM_ID,
    HOME_SERVER,
    STORE_PATH,
    CREDENTIALS_FILE,
    DEVICE_NAME,
    MatrixLoginError
)
from logs.logger_helper import LoggerHelper
import os
import json
import logging
from typing import Optional, Tuple
# 'nio' module is provided by the 'matrix-nio' package
from nio import AsyncClient, LoginResponse

# suppress specific warnings related to event decryption and crypto operations
logging.getLogger("nio.event_decryption").setLevel(logging.ERROR)
logging.getLogger("nio.crypto").setLevel(logging.ERROR)


class MatrixNio:
    """
    MatrixNio is a class that handles sending encrypted messages to a Matrix room using the matrix-nio library.

    This class simplifies the process of logging in, handling encryption keys, and sending messages,
    making it suitable for integration into applications like trading algorithms where secure communication is needed.

    Attributes:
        logger (LoggerHelper): Logs info and errors regarding MatrixNio execution.
        username (str): The Matrix username (including homeserver) of the account to use.
        password (str): The password for the Matrix account.
        room_id (str): The ID of the Matrix room to send messages to.
        homeserver (str): The URL of the Matrix homeserver.
        store_path (str): The path to store encryption keys and session data.
        credentials_file (str): The path to the credentials file for storing access tokens.
        client (AsyncClient): The matrix-nio AsyncClient instance used for communication.
    """

    def __init__(
        self,
        username: str = USERNAME,
        password: str = PASSWORD,
        room_id: str = ROOM_ID,
        homeserver: str = HOME_SERVER,
        store_path: str = STORE_PATH,
    ):
        """
        Initializes the MatrixNio client with the provided credentials and settings.

        :param username: The full Matrix username (e.g., "@user:matrix.org").
        :param password: The password for the Matrix account.
        :param room_id: The ID of the Matrix room to send messages to.
        :param homeserver: The URL of the Matrix homeserver (default is "https://matrix.org").
        :param store_path: The directory path to store encryption keys and session data (default is "./store/").
        """
        self.logger = LoggerHelper(__file__).get_logger(__name__)
        self.username = username
        self.password = password
        self.homeserver = homeserver
        self.room_id = room_id
        self.store_path = store_path
        self.credentials_file = os.path.join(store_path, CREDENTIALS_FILE)
        self.client = None  # initialized in `start()`

    async def start(self):
        """
        Starts the MatrixNio client by initializing the AsyncClient, logging in if necessary,
        and performing an initial sync to prepare for sending messages.

        This method must be called before attempting to send messages.
        """
        access_token, device_id, user_id = self.load_credentials()
        self.initialize_client(access_token, device_id, user_id)

        if not self.client.access_token:  # check if we need to log in
            await self.login()

        await self.load_and_sync_client()

    def initialize_client(self, access_token: Optional[str] = None, device_id: Optional[str] = None, user_id: Optional[str] = None):
        """
        Initializes the MatrixNio client with the provided credentials and settings.

        :param access_token: The access token obtained after logging in.
        :param device_id: The device ID assigned by the homeserver.
        :param user_id: The user ID associated with the account.
        """
        self.client = AsyncClient(
            homeserver=self.homeserver,
            user=self.username,
            device_id=device_id,
            store_path=self.store_path,
        )

        self.client.user_id = user_id or self.username
        self.client.access_token = access_token

    async def login(self):
        """
        Logs in to the Matrix server and updates the client with the new credentials.
        """
        response = await self.client.login(password=self.password, device_name=DEVICE_NAME)

        if isinstance(response, LoginResponse):  # update client attributes with the response data
            self.client.access_token = response.access_token
            self.client.device_id = response.device_id
            self.client.user_id = response.user_id

            self.save_credentials(  # save credentials for future use
                access_token=response.access_token,
                device_id=response.device_id,
                user_id=response.user_id,
            )

            await self.client.keys_upload()  # upload encryption keys after login

            self.logger.info(f"Logged in as {self.client.user_id} on device {self.client.device_id}")
            self.logger.info("Please verify this device in your Matrix client to enable encrypted messaging.")
        else:
            self.logger.error(f"Login failed: {response}")
            raise MatrixLoginError

    async def load_and_sync_client(self):
        """
        Loads the store and performs an initial sync to fetch encryption keys and device lists.
        """
        self.client.load_store()
        await self.client.sync(full_state=True)

    async def send_message(self, message: str):
        """
        Sends an encrypted message to the specified Matrix room.

        :param message: The message content to send.
        """
        await self.client.room_send(
            room_id=self.room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message,
            },
            ignore_unverified_devices=True,
        )
        self.logger.info(f"Sent message to Matrix Room: {message}")

    async def close(self):
        """
        Closes the MatrixNio client session and releases any held resources.
        """
        await self.client.close()

    def load_credentials(self) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Loads stored credentials from the credentials file if it exists.

        :return: A tuple containing (access_token, device_id, user_id), or (None, None, None) if not found.
        """
        os.makedirs(self.store_path, exist_ok=True)

        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, "r") as f:
                creds = json.load(f)
                access_token = creds.get("access_token")
                device_id = creds.get("device_id")
                user_id = creds.get("user_id")
                return access_token, device_id, user_id
        else:
            return None, None, None

    def save_credentials(self, access_token: str, device_id: str, user_id: str):
        """
        Saves credentials to the credentials file for future use.

        :param access_token: The access token obtained after logging in.
        :param device_id: The device ID assigned by the homeserver.
        :param user_id: The user ID associated with the account.
        """
        creds = {
            "access_token": access_token,
            "device_id": device_id,
            "user_id": user_id,
        }
        with open(self.credentials_file, "w") as f:
            json.dump(creds, f)
