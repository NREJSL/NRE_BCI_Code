import requests

def make_header():
    return {
        'Content-Type': 'application/json'
    }


def make_url(base_url, port, endpoint):
    return f'http://{base_url}:{port}/v1/{endpoint}'


def handle_request_errors(e):
    if isinstance(e, requests.exceptions.RequestException):
        print(f"Request Error: {e.response.text}")
    elif isinstance(e, requests.exceptions.HTTPError):
        print(f"HTTP Error: {e}")
    elif isinstance(e, requests.exceptions.Timeout):
        print(f"Request timed out: {e}")
    else:
        print(f"An unexpected error occurred: {e}")
