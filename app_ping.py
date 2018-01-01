import time
import schedule
import requests
import traceback

def job():
    try:
        requests.post('https://<app_name>.herokuapp.com/keep_alive', timeout=1000)
        print('Keep alive: OK.')
    except Exception:
        print(traceback.format_exc())

def main():
    schedule.every(20).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
