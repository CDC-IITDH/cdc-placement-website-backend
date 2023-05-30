from APIs.models import Contributor
from django.shortcuts import get_object_or_404
import time
from dotenv import load_dotenv
import requests
import os
load_dotenv("../dev.env")

owner = 'CDC-IITDH'
access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
headers = {'Authorization': "Token " + access_token}
maxRetires = 10
REPEAT_AFTER = 60 * 15 #  15 minutes

def getStats():
    try:
        stats = {}
        repos = ['cdc-placement-website-backend', 'cdc-placement-website-frontend']
        for i in repos:
            try:
                repo_name = i
                print(repo_name)
                url = f"https://api.github.com/repos/{owner}/{repo_name}/stats/contributors"
                retry = 0
                contributors = []
                while True:
                    if retry > maxRetires:
                        break
                    req = requests.get(url, headers=headers)
                    contributors = req.json()
                    if req.status_code != 200:
                        print("ERROR:", req.json())
                        retry += 1
                    elif len(contributors):
                        break
                    retry += 1

                    time.sleep(1)

                for contributor in contributors:
                    if contributor['author']['login'] not in stats:
                        stats[contributor['author']['login']] = 0
                    stats[contributor['author']['login']] += contributor['total']
            except Exception as e:
                print(e)

        for i in stats:
            try:
                contributor = get_object_or_404(Contributor, github_id=i)
                contributor.commits = stats[i]
                contributor.save()
            except:
                pass

        stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        for i in stats:
            print(i)
    except Exception as e:
        print(e)
        return stats


def run():
    while True:
        getStats()
        print("Sleeping for", REPEAT_AFTER, "seconds")
        time.sleep(REPEAT_AFTER)
        print("Running send_reminder_mails()")

run()