import requests
from os import path
import json
import yaml


def webhooks_ms_teams(config, webhookJsonFile):
    url = config['webhooks']['ms_teams']
    if path.exists(webhookJsonFile):
        with open(webhookJsonFile) as webhookJson:
            jsonPayload = json.load(webhookJson)
        response = requests.post(
            url, json=jsonPayload, headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            isNotified = 1
        else:
            print("ERROR: Unable to send webhook to Teams General Channel")
    else:
        print("ERROR: Webhook json payload file not found")
        
if (__name__ == "__main__"):
    working_dir = "/home/saradindu/dev/mlops_pipeline_flair/"
    with open(f"{working_dir}/config/config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    webhookJsonFile = config['webhooks']['webhook_payload']
    webhooks_ms_teams(config, webhookJsonFile)
