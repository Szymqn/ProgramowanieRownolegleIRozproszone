import socket
from _thread import *
import threading
import datetime
import platform
import psutil

print_lock = threading.Lock()


def get_server_info():
    hostname = socket.gethostname()
    system = platform.system()
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    info = (
        f"Server Information:\n"
        f"Hostname: {hostname}\n"
        f"System: {system}\n"
        f"CPU Usage: {cpu_usage}%\n"
        f"Memory Usage: {memory_info.percent}%\n"
        f"Disk Usage: {disk_info.percent}%\n"
    )

    return info


def threaded(c, addr):
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')
            print_lock.release()
            break

        if data.decode('utf-8').lower() == 'info':
            server_info = get_server_info()
            c.send(server_info.encode('utf-8'))
        else:
            data = data[::-1]
            c.send(data)

    c.close()

    log_message = f"Disconnected from: {addr[0]}:{addr[1]} at {datetime.datetime.now()}\n"
    print(log_message)

    with open("server_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message)


def main():
    host = ""
    port = 54321
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket bound to the following port", port)
    s.listen(5)
    print("Socket listening")

    log_message = f"Socket bound to port {port} at {datetime.datetime.now()}\n"
    print(log_message)
    with open("server_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message)

    while True:
        try:
            c, addr = s.accept()
            print_lock.acquire()

            log_message = f"Connected to: {addr[0]}:{addr[1]} at {datetime.datetime.now()}\n"
            print(log_message)
            with open("server_logs.txt", "a", encoding="utf-8") as log_file:
                log_file.write(log_message)

            start_new_thread(threaded, (c, addr))
        except KeyboardInterrupt:
            log_message = "Interrupted by the user\n"
            print(log_message)
            with open("server_logs.txt", "a", encoding="utf-8") as log_file:
                log_file.write(log_message)
            break
        except Exception as ex:
            log_message = f"An error occurred: {ex}"
            print(log_message)
            with open("server_logs.txt", "a", encoding="utf-8") as log_file:
                log_file.write(log_message)
    s.close()


if __name__ == '__main__':
    main()
