import paho.mqtt.client as mqtt
import sys
import configparser
import time
from threading import Thread

CONFIG_FILE = "config.ini"
messages = {}

config = configparser.ConfigParser()
print("Lese Konfiguration aus", CONFIG_FILE)
config.read(CONFIG_FILE)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Verbindung hergestellt")
    topics = [t.strip() for t in config["mqtt"]["topics"].split(",")]
    print("Abonniere folgende Topics:", topics)
    for t in topics:
        client.subscribe(t)

def on_message(client, userdata, msg):
    messages[msg.topic] = {
        'content': msg.payload.decode("utf-8"),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

def export_to_html():
    while True:
        time.sleep(10)  # Alle 10 Sekunden
        with open("output.html","w") as f:
            f.write("<html><body><table border='1'>")
            f.write("<tr><th>Topic</th><th>Inhalt</th><th>Letzte Aktualisierung</th></tr>")
            for topic, data in messages.items():
                f.write(f"<tr><td>{topic}</td><td>{data['content']}</td><td>{data['timestamp']}</td></tr>")
            f.write("</table></body></html>")

def main():
    host = config["mqtt"]["host"]
    port = int(config["mqtt"]["port"])

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    print("Verbinde zu", host, "auf Port", port)
    client.connect(host, port, 60)


    Thread(target=export_to_html, daemon=True).start()
    client.loop_forever()

if __name__ == "__main__":
    main()