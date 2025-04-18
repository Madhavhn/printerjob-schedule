import tkinter as tk
from tkinter import PhotoImage
import ctypes

# Load the C DLL
c_dll = ctypes.CDLL(".\print_queue.dll")

# Define C struct for PrintJob
class PrintJob(ctypes.Structure):
    _fields_ = [
        ("pagesToPrint", ctypes.c_int),
        ("priority", ctypes.c_int),
        ("computerID", ctypes.c_int),
        ("JobID", ctypes.c_int),
    ]

# Define the functions to call C functions
c_dll.initializeQueue.restype = None
c_dll.initializeQueue.argtypes = [ctypes.c_void_p]
c_dll.is_empty.restype = ctypes.c_int
c_dll.is_empty.argtypes = [ctypes.c_void_p]
c_dll.is_full.restype = ctypes.c_int
c_dll.is_full.argtypes = [ctypes.c_void_p]
c_dll.enqueue.restype = None
c_dll.enqueue.argtypes = [ctypes.c_void_p, PrintJob]
c_dll.wait_time.restype = ctypes.c_int
c_dll.wait_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
c_dll.dequeue.restype = PrintJob
c_dll.dequeue.argtypes = [ctypes.c_void_p]
c_dll.peek.restype = PrintJob
c_dll.peek.argtypes = [ctypes.c_void_p]

# Create the GUI
root = tk.Tk()
root.title("Print Queue Simulator")

# Define the PrintQueue struct
class PrintQueue(ctypes.Structure):
    _fields_ = [
        ("jobs", PrintJob * 1000),
        ("front", ctypes.c_int),
        ("rear", ctypes.c_int),
    ]

# Initialize the PrintQueue
printerQueue = PrintQueue()
c_dll.initializeQueue(ctypes.byref(printerQueue))

# Function to add a job to the queue
def add_job():
    pages = int(pages_entry.get())
    priority = int(priority_entry.get())
    computer_id = computer_buttons.index(computer_var.get())
    
    new_job = PrintJob(pages, priority, computer_id, -1)
    c_dll.enqueue(ctypes.byref(printerQueue), new_job)
    update_printer_status()

# Function to finish a job
def finish_job():
    finished_job = c_dll.dequeue(ctypes.byref(printerQueue))
    if finished_job.pagesToPrint >= 0:
        update_printer_status()

# Function to check wait time
def check_wait_time():
    job_id = int(job_id_entry.get())
    wait_time = c_dll.wait_time(ctypes.byref(printerQueue), job_id)
    wait_time_label.config(text=f"Wait time for Job {job_id}: {wait_time} seconds")

# Function to update the printer status label
def update_printer_status():
    top_job = c_dll.peek(ctypes.byref(printerQueue))
    if top_job.pagesToPrint >= 0:
        printer_status_label.config(text=f"Printing Job {top_job.JobID} ({top_job.pagesToPrint} pages)")

# Create GUI components
pages_label = tk.Label(root, text="Number of Pages:")
pages_label.pack()
pages_entry = tk.Entry(root)
pages_entry.pack()

priority_label = tk.Label(root, text="Priority:")
priority_label.pack()
priority_entry = tk.Entry(root)
priority_entry.pack()

add_button = tk.Button(root, text="Add Job", command=add_job)
add_button.pack()

computer_buttons = ["Computer 1", "Computer 2", "Computer 3", "Computer 4"]
computer_var = tk.StringVar()
computer_var.set(computer_buttons[0])

for computer in computer_buttons:
    computer_button = tk.Radiobutton(root, text=computer, variable=computer_var, value=computer)
    computer_button.pack()

finish_button = tk.Button(root, text="Finish Job", command=finish_job)
finish_button.pack()

printer_image = PhotoImage(file="printer.png")
printer_label = tk.Label(root, image=printer_image)
printer_label.pack()

printer_status_label = tk.Label(root, text="Printer Idle")
printer_status_label.pack()

job_id_label = tk.Label(root, text="Enter Job ID:")
job_id_label.pack()
job_id_entry = tk.Entry(root)
job_id_entry.pack()

check_wait_time_button = tk.Button(root, text="Check Wait Time", command=check_wait_time)
check_wait_time_button.pack()

wait_time_label = tk.Label(root, text="")
wait_time_label.pack()

# Main loop
root.mainloop()
