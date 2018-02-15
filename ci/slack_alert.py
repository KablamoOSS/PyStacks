import requests
import json

# Change:
# 1. webhook url
# 2. channel field

SLACK_CHANNEL = ''
SLACK_WEBHOOK_URL = ''
REPO_URL = '' # EG https://github.com/github/github/

# ## Richly formatted

# Get a commit file with the following bash command:
# $ git slack -1 > /tmp/commit.json

commit = {}
with open('/tmp/commit.json', 'r') as f:
    commit = json.loads(f.read())
commit['repository'] = REPO_URL

attachments = [
    {
        "fallback": "The following commit just broke the PyStacks build: <{repository}/commits/{hash}|{hash}>".format(**commit),
        "color": "danger",  # Can either be one of 'good', 'warning', 'danger', or any hex color code
        # Fields are displayed in a table on the message
        "fields": [
            {
                "title": "Test failed - PyStack",
                "value": "The following commit just broke the PyStacks build: <{repository}/commits/{hash}|{hash}>".format(**commit),
            }
        ]
    },
    {
        "pretext": "<{repository}/addon/pipelines/home#!|Github Pipelines>".format(**commit)
    }
]

message_json = {'channel': SLACK_CHANNEL, "username": "Github-Pipelines",
                # "text": "<!channel>",
                "link_names": "1",
                "icon_emoji": ":speak_no_evil:",
                "attachments": attachments,
                }

response = requests.post(
    url=SLACK_WEBHOOK_URL,
    json=message_json,
)

# return "response.status_code"
