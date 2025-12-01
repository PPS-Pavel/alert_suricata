import requests, time, os

TOKEN = "8249012810:AAFKQ24Kp_EoMvA6hEze1aVz9zVGLB28YOA"
USERS = ["654891316"]
SIDS = ["1000002", "1000003","1000004", "1000005"]

last_size = 0  # Запоминаем размер файла

while True:
    current_size = os.path.getsize("/var/log/suricata/fast.log")
    
    if current_size > last_size:  # Файл вырос
        with open("/var/log/suricata/fast.log") as f:
            f.seek(last_size)  # Переходим к новым данным
            for line in f:
                if '[**]' in line and any(sid in line for sid in SIDS):
                    for user_id in USERS:
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                     data={'chat_id': user_id, 'text': f'🚨 {line.strip()}'})
        last_size = current_size
    
    time.sleep(1)  # Проверяем чаще, но не нагружаем CPU