# Ed Preview Bot

A Slack App which shows a custom preview of Ed Discussion links which are sent in channels.

### Installation

1. If needed, create an app with the [manifest.json](./manifest.json) file by following the instructions [here](https://docs.slack.dev/app-manifests/configuring-apps-with-app-manifests/#creating_apps).
2. Provide an `.env` file with the following variables: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, and `ED_API_TOKEN`.
3. Install requirements by running `pip install -r requirements.txt`
4. Start the bot by running `python3 bot.py`