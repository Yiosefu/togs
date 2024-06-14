from tkinter import *  #para magka roon ng GUI
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import heapq
"""
TO DO:
    Timeline
    sorting
    gantt
    table
    average
"""
class RR:

    def __init__(self, window):
        self.window = window
        self.window.geometry("1920x1024")
        self.window.title("RR")
        
        #dito input kung ilang jobs ilalagay
        self.process_label = tk.Label(window, text="Enter The number of Jobs you are going to Process: ", font=('Helvetica', 16))
        self.process_label.grid(row=0, column=0, padx=10, pady=5)
        self.process_entry = tk.Entry(window, width=10)  #ito yung input kung ilang numjobs
        self.process_entry.grid(row=0, column=1, padx=10, pady=5) 

        #the button that will change the table
        self.button = tk.Button(window, text="Update", command=self.update_table)
        self.button.grid(row=0, column=2, padx=10, pady=5)


        self.process_list = []

        self.gantt_text = None
        self.completion_text = None
        
        self.process_list_list = [] #dito naalagay yung mga ininput
        
    def update_table(self):
        try:
            num_jobs = int(self.process_entry.get())
            if num_jobs <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of jobs.")
            return
        
        self.input_frame = tk.Frame(self.window)
        self.input_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        #pag nagupdate kung ilang job aalisin yung mga nainput nung una
        self.process_list.clear()
        self.process_list_list.clear()
        
        #dito yung mga input 
        job_title = tk.Label(self.input_frame, font=('Helvetica', 14), text="Job")
        job_title.grid(row=1, column = 1)
        AT_title = tk.Label(self.input_frame, font=('Helvetica', 14), text="Arrival time")
        AT_title.grid(row=1, column = 2)
        BT_title = tk.Label(self.input_frame, font=('Helvetica', 14), text="Burst Time")
        BT_title.grid(row=1, column = 3)
        q_title = tk.Label(self.input_frame, font=('Helvetica', 14), text="Quantum")
        q_title.grid(row=1, column = 4)

        for i in range(num_jobs):
            job_label = tk.Label(self.input_frame, font=('Helvetica', 14), text=f"Job {i+1}: ", width=5)
            job_label.grid(row=i+2, column=1)
            
            arrival_entry = tk.Entry(self.input_frame)
            arrival_entry.grid(row=i+2, column=2)
            
            burst_entry = tk.Entry(self.input_frame)
            burst_entry.grid(row=i+2, column=3)
            
            self.process_list.extend([ arrival_entry, burst_entry])
            self.process_list_list.append((arrival_entry, burst_entry))

        quantum_entry = tk.Entry(self.input_frame)
        quantum_entry.grid(row=2, column=4)

        run_button = tk.Button(self.input_frame, text="Run RR", command=self.Calculate_RR)
        run_button.grid(row=num_jobs+2, column = 0, columnspan=5)

    #dito icocompute tapos isosort yung algorithm
    def rr(self, job_list):
        pass


    
    def average(self, completed):
        num_jobs = int(self.process_entry.get())
        total_tat = sum(values[1] for values in completed.values())
        average_tat = total_tat / num_jobs

        total_wt = sum(values[2]for values in completed.values())
        average_wt = total_wt / num_jobs

        return average_tat, average_wt
    
    def Calculate_RR(self):
        pass