
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import time
import validators


def check_expiry():
    print("Checking periodic expiry")
    curr_dir = os.getcwd()
    pastes_dir = os.path.join(curr_dir, "pastes")
    for file in os.listdir(pastes_dir):
        file_path = os.path.join(pastes_dir, file)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
            curr_epoch = int(time.time())
            epoch_exp = 86400  # 24 hr epoch
            time_since = curr_epoch-data['date']
            if time_since > epoch_exp:
                print(f"{file} has expired. Removing pastebin!")
                os.remove(file_path)


def make_scheduler():

    # The "apscheduler." prefix is hard coded
    scheduler = BackgroundScheduler({

        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.executors.processpool': {
            'type': 'processpool',
            'max_workers': '5'
        },
        'apscheduler.job_defaults.coalesce': 'false',
        'apscheduler.job_defaults.max_instances': '3',
        'apscheduler.timezone': 'UTC',
    })
    return scheduler


def check_url_paste(paste_name):
    curr_dir = os.getcwd()
    pastes_dir = os.path.join(curr_dir, "pastes")
    if paste_name in os.listdir(pastes_dir):
        file_path = os.path.join(pastes_dir, paste_name)
        with open(file_path, "r") as file:
            data = json.load(file)
        if validators.url(data['content']) or data['content'].startswith("www."):
            return data['content']
