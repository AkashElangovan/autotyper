import pyautogui
import keyboard
import threading
import time
import tkinter as tk
from tkinter import messagebox
import webbrowser  
#main code
class AutoTyper:
    def __init__(self, text, wpm, trigger_key):
        self.text = text
        self.wpm = wpm
        self.trigger_key = f'ctrl+{trigger_key}'  
        self.is_active = False 
        self.stop_flag = threading.Event() 
        self.thread = None 

    def start_typing(self):
       
        time_per_word = 60 / self.wpm  
        time_per_char = time_per_word / 5  

        for char in self.text:
            if self.stop_flag.is_set():
                print(f"Auto-typing stopped for trigger key: Ctrl+{self.trigger_key[-1]}")
                break 
            pyautogui.typewrite(char)
            time.sleep(time_per_char)

    def toggle_typing(self):
        if self.is_active:
            
            self.stop_flag.set()
            self.is_active = False
            print(f"Typing stopped for Ctrl+{self.trigger_key[-1]}")
        else:
            self.stop_flag.clear()
            self.is_active = True
            print(f"Typing started for Ctrl+{self.trigger_key[-1]}")
            self.thread = threading.Thread(target=self.start_typing)
            self.thread.start()
    def run(self):
        keyboard.add_hotkey(self.trigger_key, self.toggle_typing)
        keyboard.wait(self.trigger_key)

def create_auto_typer_instance(text, wpm, trigger_key):
    auto_typer = AutoTyper(text, wpm, trigger_key)
    thread = threading.Thread(target=auto_typer.run)
    thread.daemon = True  
    thread.start()


# GUI 
class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Typer with Custom Speed and Ctrl+Number Triggers")

        self.instances = []

        tk.Label(root, text="Text to type (preserves indentation):").grid(row=0, column=0, padx=10, pady=10)
        self.text_entry = tk.Text(root, width=40, height=10)
        self.text_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Typing speed (words per minute):").grid(row=1, column=0, padx=10, pady=10)
        self.speed_entry = tk.Entry(root, width=40)
        self.speed_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Number key to trigger (0-9, automatically uses Ctrl):").grid(row=2, column=0, padx=10, pady=10)
        self.trigger_key_entry = tk.Entry(root, width=40)
        self.trigger_key_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Auto-Typer Instance", command=self.add_instance)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.instance_listbox = tk.Listbox(root, width=60, height=10)
        self.instance_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.github_link = tk.Label(root, text="Made with ❤️", fg="blue", cursor="hand2")
        self.github_link.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.github_link.bind("<Button-1>", lambda e: self.open_github())  

    def add_instance(self):
        text = self.text_entry.get("1.0", tk.END)  
        try:
            wpm = int(self.speed_entry.get())
            if wpm <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for WPM (greater than 0).")
            return

        trigger_key = self.trigger_key_entry.get()

        if not text.strip() or not trigger_key.isdigit() or not (0 <= int(trigger_key) <= 9):
            messagebox.showerror("Invalid Input", "Please enter all fields and ensure the trigger key is a number between 0 and 9.")
            return

       
        try:
            create_auto_typer_instance(text, wpm, trigger_key)
            instance_info = f"Text: {text[:30]}..., WPM: {wpm}, Trigger Key: Ctrl+{trigger_key}"
            self.instance_listbox.insert(tk.END, instance_info)
        except ValueError as e:
            messagebox.showerror("Invalid Shortcut Key", f"Error: {e}")

    def open_github(self):
        webbrowser.open("https://github.com/AkashElangovan")  


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
