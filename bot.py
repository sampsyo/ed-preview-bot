import logging

from edapi import EdAPI
from bs4 import BeautifulSoup
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

'''
References:
https://docs.slack.dev/messaging/unfurling-links-in-messages
https://docs.slack.dev/tools/bolt-python/getting-started
https://github.com/smartspot2/edapi/blob/master/docs/api_docs.md
'''

logging.basicConfig(level=logging.INFO)

ed = EdAPI()
# call this first since it reads the env file
ed.login()

# create Slack app
app = App()

@app.event("link_shared")
def handle_link_shared_events(event: dict, client: WebClient):
    logging.info(f"Link shared event received!")

    # parse and fetch data for each link
    unfurl_data = {}
    for link in event.get("links", []):
        thread_id = link['url'].split("/")[-1]
        logging.info(f"Shared link: {link['url']} has thread ID: {thread_id}")
        unfurl_data[link['url']] = process_ed_thread(int(thread_id))

    # call unfurl web API
    client.chat_unfurl(
        source=event["source"],
        unfurl_id=event["unfurl_id"],
        unfurls=unfurl_data
    )

def process_ed_thread(thread_id: int):
    thread = ed.get_thread(thread_id)
    title = f"{thread['title']} (#{thread['number']})"

    soup = BeautifulSoup(thread['content'], 'html.parser')
    images = [img['src'] for img in soup.find_all('image')]

    return {
        "preview": {
            "title": {
                "type": "plain_text",
                "text": title
            },
            "icon_url": "https://edcdn.net/assets/favicon-64x64.eab1c85f.png"
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_Category: {thread['category']}_\n\n{thread['document']}"
                }
            },
            *[
                {
                    "type": "image",
                    "image_url": img_url,
                    "alt_text": "Image from Ed thread"
                } for img_url in images
            ]
        ]
    }

# start Slack app
if __name__ == "__main__":
    SocketModeHandler(app).start()
