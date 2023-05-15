import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

class ClientGUI:
    def __init__(self):
        self.client_socket = None
        self.host = 'localhost'
        self.port = 5000

        self.root = tk.Tk()
        self.root.title("Client")
        self.root.geometry("400x200")

        self.select_file_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        self.send_button = tk.Button(self.root, text="Send File", command=self.send_file, state=tk.DISABLED)
        self.send_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Not Connected")
        self.status_label.pack(pady=10)

        self.root.mainloop()

    def select_file(self):
        self.file_path = filedialog.askopenfilename(initialdir="./", title="Select File")
        if self.file_path:
            self.send_button.config(state=tk.NORMAL)

    def send_file(self):
        self.select_file_button.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

        self.send_thread = threading.Thread(target=self.send_file_thread)
        self.send_thread.start()

    def send_file_thread(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.status_label.config(text=f"Connected to server {self.host}:{self.port}")
            filename = self.file_path.split("/")[-1]
            self.client_socket.sendall(filename.encode())
            response = self.client_socket.recv(1024)
            if response == b"cancel":
                self.status_label.config(text="Canceled by Server")
                return
            with open(self.file_path, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.client_socket.sendall(data)
            messagebox.showinfo("File Transfer", f"{filename} sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if self.client_socket:
                self.client_socket.close()
            self.select_file_button.config(state=tk.NORMAL)
            self.status_label.config(text="Not Connected")

if __name__ == "__main__":
    ClientGUI()