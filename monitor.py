import requests
import time
import re
from datetime import datetime

TOKEN = "8249012810:AAFKQ24Kp_EoMvA6hEze1aVz9zVGLB28YOA"
USER = ["654891316"]
SIDS = ["1000002", "1000003", "1000004", "1000005"]

def log_time(log_line):
    match = re.search(r'(\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}\.\d{6})', log_line)
    if match:
        try:
            return datetime.strptime(match.group(1), '%m/%d/%Y-%H:%M:%S.%f')
        except:
            return None
    return None

def monitor_logs():
    start_time = datetime.now()
    print("Monitoring start")
    
    while True:
        try:
            with open("/var/log/suricata/fast.log", "r") as f:
                for line in f:
                    event_time = log_time(line)
                    
                    if not event_time or event_time <= start_time:
                        continue
                    
                    if '[**]' in line and any(sid in line for sid in SIDS):
                        for user_id in USER:
                            requests.post(
                                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                data={'chat_id': user_id, 'text': line.strip()'}
                            )
            
            start_time = datetime.now()
            
        except Exception as e:
            print(e)

if __name__ == "__main__":
    monitor_logs()
