import requests
import time

TOKEN = "8249012810:AAFKQ24Kp_EoMvA6hEze1aVz9zVGLB28YOA"
USERS = ["654891316"]
SIDS = ["1000002", "1000003", "1000004", "1000005"]

def monitor_simple():
    """Простой мониторинг - запоминаем кол-во строк"""
    print("Start monitoring")
    
    # Считаем строки при запуске
    try:
        with open("/var/log/suricata/fast.log", "r") as f:
            initial_lines = len(f.readlines())
    except:
        initial_lines = 0
    
    while True:
        try:
            # Читаем все строки
            with open("/var/log/suricata/fast.log", "r") as f:
                all_lines = f.readlines()
                
            new_lines = all_lines[initial_lines:]
            for line in new_lines:
                if '[**]' in line and any(sid in line for sid in SIDS):  
                    for user_id in USERS:
                        try:
                            requests.post(
                                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                data={'chat_id': user_id, 'text': line.strip()},
                                timeout=5
                            )
                        except:
                            pass
            
            # Обновляем счетчик
            initial_lines = len(all_lines)
            
        except Exception as e:
            print(f"Ошибка: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    monitor_simple()
