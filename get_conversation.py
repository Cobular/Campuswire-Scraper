# Install the Python Requests library:
# `pip install requests`

import requests
from environment import CLASS

def send_request(post: str, bearer: str):
    # cURL
    # GET https://api.campuswire.com/v1/group/<CLASS>/posts/e9588530-7121-4182-b6e6-cd6191a27896/comments

    try:
        response = requests.get(
            url=f"https://api.campuswire.com/v1/group/{CLASS}/posts/{post}/comments",
            headers={
                "Authorization": bearer,
            },
        )
        if not response.ok:
            raise Exception('HTTP Request failed')
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


