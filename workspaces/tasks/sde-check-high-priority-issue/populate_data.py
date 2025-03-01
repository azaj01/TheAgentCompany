# You should do the initialization work in this python file to set up the environment you need
import os
import subprocess
import requests
import logging
from rocketchat_API.rocketchat import RocketChat

############################# init variable ##################################### 
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
CHANNEL_NAME = "general"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()

############################# util function #####################################  
# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        # logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Functionality Test")

############################# Test function ##################################### 

def execute_command(command):
    process = subprocess.run(command, shell=True, check=True)
    logger.info(process.stdout)
    return

def create_user():
    user_name = "Colby Devin"
    user_password = 'Colby@Devin'
    user_email = 'Colby.Devin@andrew.cmu.edu'
    user_username = 'Colby.Devin'
    response = rocket.users_create(user_email,user_name,user_password, user_username).json()
    if response.get('success'):
        logger.info(f"Successfully created user.")
        return True
    else:
        logger.error(f"{response.get('error')}")
        return False


def check_channel_exists(channel_name):
    channels = rocket.channels_list().json()
    channel_names = channels.get("channels", [])
    return any(current_channel['name'] == channel_name for current_channel in channel_names)


def create_channel(channel_name):
    if check_channel_exists(channel_name) == True:
        logger.info("Channel already exists")
        return False
    response = rocket.channels_create(channel_name).json()
    if response.get('success'):
        logger.info(f"Successfully created channel.")
        return True
    else:
        logger.error(f"{response.get('error')}")
        return False
    
def add_user_to_channel(channel_name, username):
    response_user = rocket.users_info(username = username).json()
    user_id = response_user['user']['_id']
    response_channel = rocket.channels_info(channel=channel_name).json()
    channel_id = response_channel['channel']['_id']
    response = rocket.channels_invite(channel_id, user_id).json()
    if response.get('success'):
        logger.info(f"Successfully added {username} to '{channel_name}'.")
        return True
    else:
        logger.error(f"Failed to add {username}  to '{channel_name}' channel.")
        return False

if __name__ == "__main__":
    create_channel("Janusgraph")
    create_user()
    channel_name = "Janusgraph"
    username = 'Colby.Devin'
    print(add_user_to_channel(channel_name, username))