import tkinter as tk
from tkinter import ttk
import asyncio
import webbrowser
import ipaddress
import socket


class HostScannerApp:
    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def __init__(self, master):
        self.master = master
        self.master.title("RHILEX 网关扫描器")

        self.subnet_label = tk.Label(self.master, text="本地网络:")
        self.subnet_label.pack(pady=5, anchor="w")

        # Use Combobox for subnet selection with default value as the local IP
        local_ip = self.get_local_ip()
        self.subnet_combobox = ttk.Combobox(self.master, values=[local_ip])
        self.subnet_combobox.set(local_ip)
        self.subnet_combobox.pack(fill=tk.X, pady=5, anchor="w")

        self.mask_label = tk.Label(self.master, text="子网掩码:")
        self.mask_label.pack(pady=5, anchor="w")

        # Use Combobox for subnet mask selection with default values
        self.mask_combobox = ttk.Combobox(
            self.master, values=["255.255.255.0", "255.255.0.0"]
        )
        self.mask_combobox.set("255.255.255.0")
        self.mask_combobox.pack(fill=tk.X, pady=5, anchor="w")

        self.ip_listbox = tk.Listbox(self.master)
        self.ip_listbox.pack(fill=tk.BOTH, expand=True, pady=10, anchor="w")

        # Add a button to each item in the Listbox
        self.add_buttons_to_listbox()

        self.log_text = tk.Text(
            self.master, height=10, width=50, bg="black", fg="white"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, anchor="w")

        self.progressbar = ttk.Progressbar(
            self.master, orient="horizontal", length=200, mode="determinate"
        )
        self.progressbar.pack(fill=tk.X, pady=5, anchor="w")

        self.scan_button = tk.Button(self.master, text="开始扫描", command=self.start_scan)
        self.scan_button.pack(fill=tk.X, pady=10, anchor="w")

        self.scan_button = tk.Button(self.master, text="访问官网", command=self.goto_homepage)
        self.scan_button.pack(fill=tk.X, pady=10, anchor="w")

        self.center_window(500, 600)

    def add_buttons_to_listbox(self):
        # Bind the button-1 (left mouse button) click event to open_url function
        self.ip_listbox.bind("<Button-1>", self.open_url)

    def open_url(self, event):
        # Get the selected item from the Listbox if an item is selected
        selection = event.widget.curselection()
        if selection:
            selected_item = event.widget.get(selection[0])

            # Extract the IP address from the selected item
            ip = selected_item.split(":")[0].strip()

            # Open the URL in the default web browser
            url = f"http://{ip}:2580"
            webbrowser.open(url)

    def get_local_ip(self):
        try:
            # Create a socket connection to an external server to get the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print(f"Error getting local IP: {e}")
            return "127.0.0.1"

    async def scan_host(self, ip, port, timeout=1):
        try:
            # Use asyncio.wait_for to set a timeout for the connection attempt
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=timeout
            )
            writer.close()
            return ip, port, "SUCCESS"
        except asyncio.TimeoutError:
            return ip, port, "TIMEOUT"
        except Exception as e:
            return ip, port, f"Error - {e}"

    async def scan_network(self):
        subnet_str = self.subnet_combobox.get()
        mask_str = self.mask_combobox.get()

        try:
            subnet = ipaddress.IPv4Network(f"{subnet_str}/{mask_str}", strict=False)
        except ValueError:
            self.log(
                "Invalid subnetwork address or subnet mask. Please enter valid values.",
                "red",
            )
            return

        tasks = []
        total_hosts = 255
        completed_hosts = 0

        for i in range(1, total_hosts + 1):
            ip = f"{subnet.network_address + i}"
            tasks.append(self.scan_host(ip, 2580, timeout=1))
            completed_hosts += 1
            progress = (completed_hosts / total_hosts) * 100
            self.progressbar["value"] = progress
            self.master.update_idletasks()

        results = await asyncio.gather(*tasks)
        for ip, port, status in results:
            try:
                if status == "SUCCESS":
                    result = f"{ip}:{port} - [{status}]"
                    self.ip_listbox.insert(tk.END, result)
                    self.log(
                        color="green",
                        message=  f"网关 http://{ip}:{port} 扫描成功. Status: {status}"
                    )
            except ValueError:
                self.log(f"Invalid response format for host {ip}:{port} - {status}")

    # Note: The processing in open_url remains unchanged

    def log(self, message, color="white"):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.tag_configure(color, foreground=color)
        self.log_text.tag_add(
            color, f"{self.log_text.index(tk.END)}-{len(message)-1}c", tk.END
        )
        self.log_text.see(tk.END)

    def start_scan(self):
        self.ip_listbox.delete(0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.progressbar["value"] = 0
        asyncio.run(self.scan_network())

    def goto_homepage(self):
        webbrowser.open("https://www.hootrhino.com")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = HostScannerApp(root)
    root.mainloop()
