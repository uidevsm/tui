import socket
from ping3 import ping
import time
from colorama import Fore, Style

def get_color_code(color_name):
    color_codes = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'reset': Style.RESET_ALL
    }
    return color_codes.get(color_name.lower(), Fore.RESET)

def print_colored_text(color_name, text):
    color_code = get_color_code(color_name)
    print(color_code + text + Style.RESET_ALL)

def check_minecraft_server(ip, port=49208, interval=1):
    port_status = None  # Track the previous port status

    try:
        while True:
            # Check Port (Minecraft server)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Timeout for the connection attempt
            result = sock.connect_ex((ip, port))
            sock.close()

            current_port_status = (result == 0)  # True if port is open, False otherwise
            
            if current_port_status:
                # Print port status
                if current_port_status != port_status:
                    print_colored_text('blue', f"Minecraft server is reachable on port {port}.")
                    port_status = current_port_status
                
                # Only check ping if the port is open
                response_time = ping(ip)
                if response_time is None:
                    print_colored_text('red', f"Server {ip} is not responding to ping.")
                else:
                    # Construct the message with colors
                    ip_colored = get_color_code('green') + ip + Style.RESET_ALL
                    ping_colored = get_color_code('green') + f"{response_time * 1000:.2f} ms" + Style.RESET_ALL
                    message = f"Ping to {ip_colored} is {ping_colored}."
                    print_colored_text('white', message)
                
            else:
                # Print "Connection timed out" if the port is closed
                print_colored_text('red', "Connection timed out")
                port_status = current_port_status  # Update port status to closed

            time.sleep(interval)
    except KeyboardInterrupt:
        print_colored_text('yellow', "Server monitoring stopped.")
    except Exception as e:
        print_colored_text('red', f"An error occurred: {e}")

check_minecraft_server("185.107.192.44")