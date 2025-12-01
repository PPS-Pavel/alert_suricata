import requests, time

TOKEN = "8249012810:AAFKQ24Kp_EoMvA6hEze1aVz9zVGLB28YOA"
USERS = ["654891316"]
SIDS = ["1000002", "1000003","1000004", "1000005"]

# Открываем файл и сразу переходим в конец
with open("/var/log/suricata/fast.log", "r") as f:
    f.seek(0, 2)  # Перемещаемся в самый конец файла
    
    while True:
        line = f.readline()
        
        if not line:  # Нет новых данных
            time.sleep(1)  # Ждем
            continue
        
        if '[**]' in line and any(sid in line for sid in SIDS):
            for user_id in USERS:
                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    data={'chat_id': user_id, 'text': line.strip()'}
                )


