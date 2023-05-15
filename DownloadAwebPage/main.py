import requests
import tkinter as tk
import threading


class Downloader:
    def __init__(self, url):
        self.url = url

    def download(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            content = response.text

            with open("C:/Users/sheri/Desktop/webpage.html.txt", "w", encoding="utf-8") as f:
                f.write(content)
                print(f"Writing {len(content)} bytes to file...")
                print("File write completed successfully!")
        except requests.RequestException as e:
            print(f"Error downloading file: {e}")


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x100")
        self.root.title("Web Page Downloader")

        self.url_label = tk.Label(self.root, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()

        self.download_button = tk.Button(self.root, text="Download", command=self.download)
        self.download_button.pack()

        self.root.mainloop()

    def download(self):
        url = self.url_entry.get()
        downloader = Downloader(url)
        t = threading.Thread(target=downloader.download)
        t.start()


if __name__ == '__main__':
    gui = GUI()
