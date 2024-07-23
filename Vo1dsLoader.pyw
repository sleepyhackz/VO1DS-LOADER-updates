import os
import sys
import shutil
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests

class VoidsLoader(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("VO1DS LOADER")
        self.geometry("800x400")
        self.iconbitmap('vendetta_icon.ico')

        self.attributes('-toolwindow', True)
        self.configure(bg='#2a2a2a')
        self.selected_injector = None

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.injector_files = {
            "ZChair: MW2019": os.path.join(base_dir, "injectors", "zchair.exe"),
            "DosModz: MW2019": os.path.join(base_dir, "injectors", "DosModz.exe"),
            "Vip + Blocker: MW3/WZ": os.path.join(base_dir, "injectors", "Vip_Mw3.exe"),
            "GOTHAM: MW3/WZ": os.path.join(base_dir, "injectors", "gotham.exe"),
            "VO1DS: HWID CHECKER": os.path.join(base_dir, "injectors", "Vo1ds_Hwid.bat"),
            "Fortnite": None,
            "GTA: FIVE M": None
        }

        self.create_widgets()
        self.check_for_updates()

    def check_for_updates(self):
        version_url = "https://example.com/version.txt"
        try:
            response = requests.get(version_url)
            response.raise_for_status()
            latest_version = response.text.strip()
            
            current_version = "1.0.1"

            if latest_version != current_version:
                self.prompt_update()
        except requests.RequestException as e:
            print(f"Update check failed: {e}")

    def prompt_update(self):
        update_message = "A new version of VO1DS Loader is available. Would you like to update now?"
        if messagebox.askyesno("Update Available", update_message):
            self.download_and_apply_update()

    def download_and_apply_update(self):
        update_url = "https://example.com/new_version.exe"
        try:
            response = requests.get(update_url, stream=True)
            response.raise_for_status()

            with open("new_version.exe", "wb") as file:
                shutil.copyfileobj(response.raw, file)

            messagebox.showinfo("Update Downloaded", "The update has been downloaded. The loader will now restart to apply the update.")
            self.apply_update()
        except requests.RequestException as e:
            messagebox.showerror("Update Failed", f"Failed to download the update: {e}")

    def apply_update(self):
        self.destroy()  # Close the current instance of the loader
        os.rename("new_version.exe", "voids_loader.exe")  # Rename the downloaded file to replace the current executable
        os.startfile("voids_loader.exe")  # Restart the loader with the new version

    def create_widgets(self):
        left_panel = tk.Frame(self, bg='#1e1e1e')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

        canvas = tk.Canvas(left_panel, bg='#1e1e1e', highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(left_panel, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5))

        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(canvas, bg='#1e1e1e')
        canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

        injectors = [
            {"name": "ZChair: MW2019", "image_path": "images/image.png"},
            {"name": "DosModz: MW2019", "image_path": "images/DOSMODSFinal.png"},
            {"name": "Vip + Blocker: MW3/WZ", "image_path": "images/MW3-leak-cod2023-modernwarfarelogo-provvisorio.jpg"},
            {"name": "GOTHAM: MW3/WZ", "image_path": "images/shopitem.gif"},
            {"name": "VO1DS: HWID CHECKER", "image_path": "images/revised_red_logo.jpg"},
            {"name": "LoudAim: Fortnite", "image_path": "images/th.jpg"},
            {"name": "GTA: FIVE M", "image_path": "images/FiveM-Symbol.png"}
        ]

        self.injector_widgets = []
        for injector_info in injectors:
            btn_frame = tk.Frame(inner_frame, bg='#1e1e1e', highlightthickness=2, highlightbackground='#1e1e1e')
            btn_frame.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

            if injector_info["image_path"]:
                try:
                    image = Image.open(injector_info["image_path"])
                    image = image.resize((80, 80), Image.LANCZOS)
                    img = ImageTk.PhotoImage(image)

                    img_label = tk.Label(btn_frame, image=img, bg='#1e1e1e')
                    img_label.image = img
                    img_label.pack(side=tk.LEFT, padx=5)
                except FileNotFoundError:
                    messagebox.showerror("File Not Found", f"Image file not found: {injector_info['image_path']}")

            label = tk.Label(btn_frame, text=injector_info["name"], font=("Arial", 12), bg='#1e1e1e', fg='#ffffff')
            label.pack(side=tk.LEFT, padx=10, pady=5)

            btn_frame.bind("<Enter>", lambda event, frame=btn_frame: self.on_enter(event, frame))
            btn_frame.bind("<Leave>", lambda event, frame=btn_frame: self.on_leave(event, frame))
            btn_frame.bind("<Button-1>", lambda event, i=injector_info: self.select_injector(i))

            self.injector_widgets.append((btn_frame, img_label, label))

        inner_frame.update_idletasks()

        canvas.config(scrollregion=canvas.bbox("all"))

        right_panel = tk.Frame(self, bg='#2a2a2a')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.load_vo1ds_logo(right_panel)

        title_frame = tk.Frame(right_panel, bg='#2a2a2a')
        title_frame.pack(anchor=tk.W, padx=10, pady=(0, 10))

        title_label = tk.Label(title_frame, text="VO1DS ", font=("Arial", 16, "bold"), bg='#2a2a2a', fg='#ffffff')
        title_label.pack(side=tk.LEFT)

        loader_label = tk.Label(title_frame, text="LOADER", font=("Arial", 16, "bold"), bg='#2a2a2a', fg='#FF00E1')
        loader_label.pack(side=tk.LEFT)
        loader_label.bind("<Button-1>", lambda event: webbrowser.open_new("https://sleepymodz.sellpass.io/products"))

        discord_icon_filename = "raf360x360075tfafafa_ca443f4786.jpg"
        discord_icon_path = os.path.join("images", discord_icon_filename)

        try:
            discord_icon = Image.open(discord_icon_path)
            discord_icon = discord_icon.resize((20, 20), Image.LANCZOS)
            discord_img = ImageTk.PhotoImage(discord_icon)

            discord_label = tk.Label(title_frame, image=discord_img, bg='#2a2a2a')
            discord_label.image = discord_img
            discord_label.pack(side=tk.LEFT, padx=5)
            discord_label.bind("<Button-1>", lambda event: webbrowser.open_new("https://discord.gg/vo1ds"))
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"Discord icon image not found: {discord_icon_path}")

        self.load_btn = ttk.Button(right_panel, text="Load Cheat", command=self.load_cheat, width=20)
        self.load_btn.pack(pady=10)

        settings_options = ["ALL FIX", "Vcruntime", "Dcontrol"]
        settings_var = tk.StringVar()
        settings_var.set(settings_options[0])

        settings_label = tk.Label(right_panel, text="Download Links/Settings", font=("Arial", 10), bg='#2a2a2a', fg='#ffffff')
        settings_label.pack(pady=5)

        settings_dropdown = ttk.Combobox(right_panel, textvariable=settings_var, values=settings_options, state="readonly")
        settings_dropdown.pack(pady=5)

        download_btn = ttk.Button(right_panel, text="Download", command=lambda: self.download_link(settings_var.get()), width=20)
        download_btn.pack(pady=10)

    def load_vo1ds_logo(self, parent):
        logo_filename = "Vendetta_Mask_Gaming_Logo___Design.com_Logo_Maker___Design.com_-_Google_Chrome_4_14_2024_1_18_08_AM.png"
        logo_path = os.path.join("images", logo_filename)

        try:
            logo = Image.open(logo_path)
            logo = logo.resize((100, 100), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(parent, image=self.logo_img, bg='#2a2a2a')
            logo_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"Logo image file not found: {logo_path}")

    def download_link(self, option):
        links = {
            "ALL FIX": "https://drive.google.com/uc?export=download&id=1mtYyb0tAchPh1HIhslCLWRTk11567Ycw",
            "Vcruntime": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
            "Dcontrol": "https://www.sordum.org/files/downloads.php?st-defender-control"
        }

        if option in links:
            webbrowser.open_new(links[option])

    def on_enter(self, event, frame):
        frame.configure(bg='#383838')

    def on_leave(self, event, frame):
        frame.configure(bg='#1e1e1e')

    def select_injector(self, injector_info):
        self.selected_injector = injector_info["name"]

        for frame, img_label, label in self.injector_widgets:
            frame.configure(highlightbackground='#1e1e1e')

        selected_frame = next(frame for frame, img_label, label in self.injector_widgets if label.cget("text") == injector_info["name"])
        selected_frame.configure(highlightbackground='#FF00E1')

    def load_cheat(self):
        if self.selected_injector:
            if self.selected_injector == "GTA: FIVE M" or self.selected_injector == "LoudAim: Fortnite":
                messagebox.showinfo("Information", "Thanks for your interest in our products. This will be coming very soon!!")
            else:
                injector_file = self.injector_files.get(self.selected_injector)
                if injector_file and os.path.isfile(injector_file):
                    os.startfile(injector_file)
                else:
                    messagebox.showerror("Error", "Injector file not found.")
        else:
            messagebox.showwarning("Warning", "No injector selected.")

    def download_link(self, option):
        links = {
            "ALL FIX": "https://drive.google.com/uc?export=download&id=1mtYyb0tAchPh1HIhslCLWRTk11567Ycw",
            "Vcruntime": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
            "Dcontrol": "https://www.sordum.org/files/downloads.php?st-defender-control"
        }
        link = links.get(option)
        if link:
            webbrowser.open_new(link)
        else:
            messagebox.showerror("Error", "Invalid download option.")

if __name__ == "__main__":
    app = VoidsLoader()
    app.mainloop()
