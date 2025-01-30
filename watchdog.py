import websocket
import json
import time
import _thread
import subprocess

# 记录最后接收消息的时间
last_message_time = time.time()

def on_message(ws, message):
    global last_message_time
    try:
        json_message = json.loads(message)
        print(f"Received message: {json_message}")
        last_message_time = time.time()  # 更新最后接收时间
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON message: {e}")

def on_error(ws, error):
    print(f"An error occurred: {error}")
    reconnect()

def on_close(wsapp, close_status_code, close_msg):
    print("on_close args:")
    if close_status_code or close_msg:
        print("close status code: " + str(close_status_code))
        print("close message: " + str(close_msg))
    reconnect()

def on_open(ws):
    ws.send('{"sub_type":"connect","meta_event_type":"lifecycle","time":'+str(int(time.time()))+',"self_id":549308442,"post_type":"meta_event"}')
    
    def run(*args):
        while True:
            ws.send('{"message_type":"private","sub_type":"friend","message_id":18611679,"user_id":3281544867,"message":[{"type":"text","data":{"text":"code print(3)"}}],"raw_message":"code print(3)","font":0,"sender":{"user_id":3281544867,"nickname":"\u732B\u732B\u866B","sex":"unknown"},"target_id":549308442,"time":'+str(int(time.time()))+',"self_id":549308442,"post_type":"message"}')
            time.sleep(5)
    
    _thread.start_new_thread(run, ())

def monitor():
    global last_message_time
    while True:
        time.sleep(30)  # 每 30 秒检查一次
        if time.time() - last_message_time > 30:  # 超过 30 秒没收到消息
            print("No messages received for 1 minute. Restarting container...")
            subprocess.run(["docker", "restart", "nonebot-bot-1"], check=True)
            last_message_time = time.time()  # 重新记录时间，避免重复重启

def reconnect():
    print("Reconnecting...")
    time.sleep(5)  # 等待 5 秒后重新连接
    start_websocket()

def start_websocket():
    ws_url = "ws://127.0.0.1:8080/onebot/v11/ws"  # 替换为你的 WebSocket 服务器 URI
    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header={"X-Client-Role": "Universal", 'X-Self-ID': '549308442'}
    )
    ws.on_open = on_open
    ws.run_forever()

_thread.start_new_thread(monitor, ())  # 启动监控线程
start_websocket()
