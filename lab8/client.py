import socket
import datetime


def main():
    host = '127.0.0.1'
    port = 54321
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))

        with open("user_logs.txt", "a", encoding="utf-8") as log_file:
            while True:
                user_input = input("Enter message: ")
                if not user_input:
                    print("Message cannot be empty. Please try again.")
                    continue

                log_message = f"Sent message to the server: {str(user_input)} at {datetime.datetime.now()}\n"
                print(log_message)

                log_file.write(log_message)

                s.send(user_input.encode('utf-8'))
                data = s.recv(1024)
                log_message = f'Received message from the server: {str(data.decode("utf-8"))} at {datetime.datetime.now()}\n'
                print(log_message)

                log_file.write(log_message)

                ans = input('\nDo you want to continue? (y/n): ')
                if ans.lower() != 'y':
                    log_message = f"Connection to the server {host}:{port} terminated at {datetime.datetime.now()}\n"
                    print(log_message)

                    log_file.write(log_message)
                    break

    except Exception as ex:
        log_message = f"An error occurred: {ex}"
        print(log_message)
        with open("server_logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_message)
    finally:
        s.close()


if __name__ == '__main__':
    main()
