
import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

def log_function_name(func):
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        logging.debug(f"Entering function: {function_name}")
        return func(*args, **kwargs)
    return wrapper

# Function to get team data for a given team ID
def get_team_data(team_id):
    team_data = fetch_data(f"/teams/{team_id}")
    return team_data


# Function to fetch pro players data
def fetch_pro_players():
    pro_players_data = fetch_data(os.environ.get("HTTP_PROPLAYERS_URL"))
    return pro_players_data
fetch_pro_players = log_function_name(fetch_pro_players)


# Function to fetch data from the API
def fetch_data(endpoint):
    base_url = os.environ.get("HTTP_DOTA_BASE_URL")
    url = f"{base_url}{endpoint}"
    # logging.debug(f"fetch_data {url}")
    max_retries = 3  # Maximum number of retries for HTTP 429 error
    retry_interval = 30  # Default retry interval in seconds

    for attempt in range(max_retries + 1):

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
                if response.status_code == 429:
                    error_time = time.time()
                    logging.info(f"error time: {error_time}")
                    retry_after = response.headers.get('Retry-After')
                    if retry_after is not None:
                        retry_interval = int(retry_after)
                    logging.warning(f"Received HTTP 429 (Too Many Requests). Retrying after {retry_interval} seconds...")
                    time.sleep(retry_interval)  # Wait before attempting a retry
                else:
                    http_error_string = os.environ.get("MSG_HTTP_ERROR_OCCURRED")
                    logging.error(f"{http_error_string}{http_err}")
                    if attempt < max_retries:
                        logging.info(f"Retrying after {retry_interval} seconds...")
                        time.sleep(retry_interval)  # Wait before attempting a retry
                    else:
                        logging.error(f"Max retries reached. Unable to fetch data from {url}")
                        break  # Break the loop for other HTTP errors
        
        except requests.exceptions.RequestException as req_err:

            logging.error(f"Fetching: {endpoint}")
            http_error_string=os.environ.get("MSG_REQUEST_ERROR_OCCURRED")
            error_time = time.time()
            if "Expecting value: line 1 column 1" in str(req_err):
                break  # Break out of the loop
            logging.error(f"{error_time} {http_error_string} {req_err}")
        except Exception as err:
            error_string = os.environ.get("MSG_ERROR_OCCURRED")
            logging.error(f"{error_string} {err}")
    # Print the response content and status code for debugging purposes
    logging.debug(f"Response Content: {response.content}")
    # logging.debug(f"Response Status Code: {response.status_code}")

    return None
