import socket
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

        self.select_button = tk.Button(self.root, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Select an image")
        self.status_label.pack(pady=10)

        self.send_button = tk.Button(self.root, text="Send Image", command=self.send_image, state=tk.DISABLED)
        self.send_button.pack(pady=10)

        self.root.mainloop()

    def select_image(self):
        file_path = filedialog.askopenfilename(initialdir="./", title="Select Image",
                                               filetypes=[("PNG Image", "*.png"),("JPEG Image","*.jpg")])
        if file_path:
            self.file_path = file_path
            self.status_label.config(text=f"Selected image: {file_path}")
            self.send_button.config(state=tk.NORMAL)

    def send_image(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            filename = self.file_path.split("/")[-1]
            self.client_socket.sendall(filename.encode())
            response = self.client_socket.recv(1024).decode()
            if response == "cancel":
                self.status_label.config(text="Image transfer cancelled")
                return
            with open(self.file_path, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.client_socket.sendall(data)
            self.status_label.config(text="Image sent")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send image: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()

if __name__ == "__main__":
    client_gui = ClientGUI()