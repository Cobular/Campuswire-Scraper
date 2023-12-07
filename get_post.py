# Install the Python Requests library:
# `pip install requests`

from typing import Optional
import requests
from environment import CLASS

def send_request(number: int, bearer: str, before: Optional[str] = None):
    # cURL
    # GET https://api.campuswire.com/v1/group/<CLASS>/posts

    params = {
        "number": str(number),
    }

    if before:
        params["before"] = before

    try:
        response = requests.get(
            url=f"https://api.campuswire.com/v1/group/{CLASS}/posts",
            params=params,
            headers={
                "Authorization": bearer,
            },
        )
        if not response.ok:
            raise Exception('HTTP Request failed')
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


