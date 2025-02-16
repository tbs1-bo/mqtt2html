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
    messages[msg.topic] = msg.payload.decode("utf-8")

def export_to_html():
    while True:
        time.sleep(10)  # Alle 10 Sekunden
        with open("output.html","w") as f:
            f.write("<html><body><table border='1'><tr><th>Topic</th><th>Inhalt</th></tr>")
            for topic, content in messages.items():
                f.write(f"<tr><td>{topic}</td><td>{content}</td></tr>")
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