import tkinter as tk
from tkinter import ttk
import threading
import time


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")

        # Main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.process_button = ttk.Button(self.main_frame, text="Start Process", command=self.start_process)
        self.process_button.grid(row=1, column=0, pady=10)

        # Waiting screen
        self.waiting_screen = tk.Toplevel(root)
        self.waiting_screen.title("Processing...")
        self.waiting_screen.geometry("300x100")
        ttk.Label(self.waiting_screen, text="Please wait, processing...").grid(row=0, column=0, padx=20, pady=20)
        self.waiting_screen.withdraw()  # Hide the waiting screen initially

    def start_process(self):
        # Show the waiting screen
        self.waiting_screen.deiconify()

        # Start the long-running process in a separate thread
        threading.Thread(target=self.long_running_process).start()

    def long_running_process(self):
        # Simulate a long-running process
        time.sleep(5)  # Replace this with the actual processing code

        # Hide the waiting screen after the process is done
        self.root.after(0, self.waiting_screen.withdraw)


# Create the main window
root = tk.Tk()
app = App(root)

# Run the application
root.mainloop()
