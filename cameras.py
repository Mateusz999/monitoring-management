import tkinter as tk
from tkinter import scrolledtext
from netmiko import ConnectHandler
import logging
from time import sleep
from datetime import datetime
unreachablePortsList = {}
'''
nie zapominaj o ssh na switchu oraz ip ssh password-auth
'''
NetworkDevice = {
    "host": "192.168.1.254",
    "username": "cisco",
    "device_type": "cisco_s300",
    "password": "Mochnik1",
}

portList = {
    "gi1" : "192.168.1.10",
    "gi2" : "192.168.1.64"
}

def periodicallyPortScan():
    try:
        connection = ConnectHandler(**NetworkDevice)

        for key, value in portList.items():
            print(f"Key: {key}, Value: {value}")
            output = connection.send_command(f"ping {value}")
            if "timeout" in output:
                log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}ERROR: Port {portList[key]} can't be reached...", "black")
                unreachablePortsList[key] = value
                root.update()

            else:
                log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Port {portList[key]} works properly", "black")
                root.update()

        for key, value in unreachablePortsList.items():
            log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Port {key} :  {value} power off","black")
            output = connection.send_config_set(["configure terminal", f"interface {key}", "shutdown"])


            sleep(1)
            root.update()

        for port in unreachablePortsList:
            log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Port {key} :  {value} power up","black")
            
            output = connection.send_config_set(["configure terminal", f"interface {key}", "no shutdown"])
            root.update()
        unreachablePortsList.clear()
        connection.disconnect()

    except Exception as e:
        print(f"Error: {e}")
    root.after(120000,periodicallyPortScan)

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
        log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")} Port Gi{port_number} -  {portList['gi' + str(port_number)]} is clicked", "black")
        
        try:
            PortConnection = ConnectHandler(**NetworkDevice)

            output = PortConnection.send_command(f"ping {portList['gi'+ str(port_number)]}")
            if "timeout" in output:
                log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Port {portList['gi' + str(port_number)]} not respond", "black")

                unreachablePortsList['gi'+str(port_number)] = portList['gi'+str(port_number)]
                print(unreachablePortsList)

                root.update()

            else:
                log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Port {portList['gi' + str(port_number)]} works properly", "black")
                
                root.update()
               
            PortConnection.disconnect()

        except Exception as e:
            print(f"Error: {e}")

def clear_logs():
    log_text.delete(1.0, tk.END)

def connect_to_switch():
    try:
        tryConnect = ConnectHandler(**NetworkDevice)

        log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Succesfully connected", "black")
          
        tryConnect.disconnect()

    except Exception as e:
        log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Error: {e}","black")

def scan_ports():
    try:
        connection = ConnectHandler(**NetworkDevice)

        for key, value in portList.items():
            print(f"Key: {key}, Value: {value}")
            output = connection.send_command(f"ping {value}")
            if "timeout" in output:
                log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}ERROR: Port {portList[key]} can't be reached...", "black")
                unreachablePortsList[key] = value
                root.update()

            else:
                log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Port {portList[key]} works properly", "black")
                root.update()

        for key, value in unreachablePortsList.items():
            log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Port {key} :  {value} power off","black")
            output = connection.send_config_set(["configure terminal", f"interface {key}", "shutdown"])


            sleep(1)
            root.update()

        for port in unreachablePortsList:
            log_message(f"{datetime.now().strftime("%d.%m.%y %H:%M:%S: ")}Port {key} :  {value} power up","black")
            
            output = connection.send_config_set(["configure terminal", f"interface {key}", "no shutdown"])
            sleep(1)
            root.update()
        unreachablePortsList.clear()
        connection.disconnect()

    except Exception as e:
        print(f"Error: {e}")



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

root.after(1000,periodicallyPortScan)

root.mainloop()
