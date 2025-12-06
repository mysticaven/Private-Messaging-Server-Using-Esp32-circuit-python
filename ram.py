import wifi
import socketpool
import os

wifi.radio.connect(
    os.getenv("CIRCUITPY_WIFI_SSID"),
    os.getenv("CIRCUITPY_WIFI_PASSWORD")
)

print("IP:", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(1)

while True:
    conn, addr = s.accept()
    conn.recv(1024)

    conn.send(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n\r\n"
        b"ESP32 WORKS"
    )
    conn.close()
