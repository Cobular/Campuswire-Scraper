# Campuswire Scraper

Easily scrape a whole campuswire class in one go! Great for saving all those important resources you don't want to miss out on.

## Usage

1. Clone the repo
2. Make a venv `python3 -m venv venv`, activate the venv `source venv/bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Copy over the example environment `cp environment.example.py environment.py` and update the values. You'll need to extract both from a request in your browser, see below for more details.
5. Run the script `python3 fetch_posts_script.py`

## Getting the values for environment.py

You'll need to get the values for the CLASS and BEARER from a sample request on campuswire. To do this, open up the network tab in your browser's dev tools and reload the page. Pick a request titled `posts` and take the following values:

1. The `CLASS` variable comes from the first UUID in the url. For a class like this: `https://api.campuswire.com/v1/group/209b3a18-c94a-4a57-9431-dab10c53ea1e/posts?number=20` you want `209b3a18-c94a-4a57-9431-dab10c53ea1e`
2. The header `Authorization`, in it's entirety, is the `BEARER` variable. You want the whole thing, including the `Bearer ` part and the whole JWT blob after it.


## Other notes

I take no liability for anything here! This is probably against TOS and while I've taken some basic steps to limit the throughput of the script, I can't guarantee it won't get you banned. Use at your own risk!
