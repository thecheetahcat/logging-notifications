# Logging and Encrypted Notifications Package

---

This package provides two main functionalities:
1. **Logging Helper**: A simple logger utility to log messages to a file with timestamp, module name, and logging level.
2. **Matrix NIO Encrypted Notifications**: A utility to send encrypted notifications to a Matrix room using the `matrix-nio` library.

## Features
- **Custom Logging**: Creates log files with detailed information on message logs, errors, and other events.
- **Encrypted Notifications**: Send encrypted messages to a Matrix room using credentials stored in a `.env` file.
  

---

## Installation

### Requirements
- Python 3.8+
- `matrix-nio`
- `logging` (standard Python library)
- `dotenv` for loading environment variables from a `.env` file.

You can install the required dependencies via `pip`:
```bash
pip install -r requirements.txt
```

Or, if you've packaged the project:
```bash
pip install -e .
```

---

## Required Environment Variables
The encrypted notifications functionality relies on the following environment variables stored in a `.env` file:
```bash
# MATRIX NIO Credentials
USERNAME=<your-matrix-username>
PASSWORD=<your-matrix-password>
ROOM_ID=<your-matrix-room-id>
```
- Your Matrix username is: @your_username:matrix.org where your_username is created by you when you make a Matrix account
- You will set your own password when you create your account
- If you are using Element, you can find your room ID by clicking the three dots on the room --> settings --> advanced

---

## Usage
### 1. Logging Helper
The `LoggerHelper` class creates log files for each run and logs messages with timestamps. This is especially useful for tracking events in long-running processes such as trading algorithms.

**Example:**
```python
from logs.logger_helper import LoggerHelper

# Create a logger for the current file
logger = LoggerHelper(__file__).get_logger(__name__)

# Log messages
logger.info("This is an info message")
logger.error("This is an error message")
```

The logger will automatically create log files in the same directory as the logger script, with the filename containing a timestamp.

### 2. Matrix NIO Encrypted Notifications
This `MatrixNio` class is designed to send encrypted messages to a Matrix room using the `matrix-nio` library, which allows secure communication between your application and a Matrix server. This is useful for sending alerts or notifications to a private Matrix chat room.

**Example:**
```python
import asyncio
from encrypted_notifications.matrix_nio import MatrixNio

async def main():
    # Initialize MatrixNio with default credentials from .env file
    matrix_nio = MatrixNio()

    # Start the Matrix client
    await matrix_nio.start()

    # Send an encrypted message
    await matrix_nio.send_message("This is a secure test message.")

    # Close the connection
    await matrix_nio.close()

# Run the async function
asyncio.run(main())
```

Make sure the .env file contains the correct Matrix credentials (username, password, room ID). The Matrix client will attempt to log in and send messages securely.

When you first use the class, it will automatically generate a store directory which keeps your encryption keys and other necessary information. Do not delete this directory,
as once this is created, it will read your keys directly and re-use them rather than generating new keys each time. 

When you send the first message, you will want to verify your session manually in Element. 
Click on your profile --> all settings --> sessions --> find your session, and then click --> verify session

**Learn more about Matrix and Element here:**
- Matrix: https://matrix.org/
- Element: https://element.io/

---

#### License
This package is licensed under the MIT License. See the LICENSE file for details.