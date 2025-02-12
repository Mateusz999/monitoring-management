import tkinter as tk
from tkinter import scrolledtext
from netmiko import ConnectHandler
import logging
from time import sleep
unreachablePortsList = []
'''
nie zapominaj o ssh na switchu oraz ip ssh password-auth
'''
NetworkDevice = {
    "host": "192.168.1.254",
    "username": "cisco",
    "device_type": "cisco_s300",
    "password": "Mochnik1",
}
def log_message(message, log_type):
    if log_type == "error":
        log_text.config(fg="red")
    elif log_type == "success":
        log_text.config(fg="green")
    else:
        log_text.config(fg="black")
    log_text.insert(tk.END, message + '\n')
    log_text.yview(tk.END)

def on_button_click(port_number):
        log_message(f"Port {port_number} was clicked", "black")
        
        try:
            PortConnection = ConnectHandler(**NetworkDevice)

            output = PortConnection.send_command(f"ping 192.168.1.{port_number}")
            if "timeout" in output:
                log_message(f"Port 192.168.1.{port_number} not respond.","black")
                unreachablePortsList.append(port_number)
                root.update()

            else:
                log_message(output,"black")
                root.update()
               
            PortConnection.disconnect()

        except Exception as e:
            print(f"Error: {e}")

def clear_logs():
    log_text.delete(1.0, tk.END)

def connect_to_switch():
    try:
        tryConnect = ConnectHandler(**NetworkDevice)

        log_message("Succesfully connected", "black")
          
        tryConnect.disconnect()

    except Exception as e:
        log_message(f"Error: {e}","black")

def scan_ports():
    try:
        connection = ConnectHandler(**NetworkDevice)

        for lastOctet in range (7,11,1):
            output = connection.send_command(f"ping 192.168.1.{lastOctet}")
            if "timeout" in output:
                log_message(f"Port 192.168.1.{lastOctet} not respond.","black")
                unreachablePortsList.append(lastOctet)
                root.update()

            else:
                log_message(output,"black")
                root.update()

        connection.disconnect()

    except Exception as e:
        print(f"Error: {e}")
    for port in unreachablePortsList:
        log_message(f"Port  192.168.1.{port} power off","black")
        sleep(1)
        root.update()

    for port in unreachablePortsList:
        log_message(f"Port  192.168.1.{port} power up","black")
        sleep(1)
        root.update()


root = tk.Tk()
root.title("Cisco Switch - Port Monitor")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=10)

buttons = []
for i in range(1, 25):
    button = tk.Button(frame, text=f"Port {i}", width=10, command=lambda i=i: on_button_click(i))
    buttons.append(button)

for i, button in enumerate(buttons):
    row = i // 6
    col = i % 6
    button.grid(row=row, column=col, padx=5, pady=5)

log_text = scrolledtext.ScrolledText(root, width=90, height=15, wrap=tk.WORD)
log_text.pack(pady=10)

clear_button = tk.Button(root, text="Clear Logs", command=clear_logs)
clear_button.pack(pady=5)

connect_button = tk.Button(root, text="Connect to Switch", command=connect_to_switch)
connect_button.pack(pady=5)

scan_button = tk.Button(root, text="Scan Ports", command=scan_ports)
scan_button.pack(pady=5)

root.mainloop()
