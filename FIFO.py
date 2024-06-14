from tkinter import *  #para magka roon ng GUI
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
"""
TO DO:
    TIMELINE
"""
class FIFO:

    def __init__(self, window):
        self.window = window
        self.window.geometry("1920x1024")
        self.window.title("FIFO")
        
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

        for i in range(num_jobs):
            job_label = tk.Label(self.input_frame, font=('Helvetica', 14), text=f"Job {i+1}: ", width=5)
            job_label.grid(row=i+2, column=1)
            
            arrival_entry = tk.Entry(self.input_frame)
            arrival_entry.grid(row=i+2, column=2)
            
            burst_entry = tk.Entry(self.input_frame)
            burst_entry.grid(row=i+2, column=3)

            self.process_list.extend([ arrival_entry, burst_entry])
            self.process_list_list.append((arrival_entry, burst_entry))

        run_button = tk.Button(self.input_frame, text="Run FIFO", command=self.Calculate_FIFO)
        run_button.grid(row=num_jobs+2, column = 0, columnspan=5)


    #ito yung algorithm dito nasosort
    def fifo(self, job_list):
        time = 0
        gantt = []
        completed = {}
        job_list.sort()

        while job_list:
            if job_list[0][0] > time:
                time += 1
                continue
            else:
                job = job_list.pop(0)
                time += job[1]
                job_name = job[2]
                ct = time
                tat = ct - job[0]
                wt = tat - job[1]
                gantt.append((job[2], ct))
                completed[job_name] = [ct, tat, wt]
        return gantt, completed    
    
    #ito yung mga average
    def average(self, completed):
        num_jobs = int(self.process_entry.get())
        total_tat = sum(values[1] for values in completed.values())
        average_tat = total_tat / num_jobs

        total_wt = sum(values[2]for values in completed.values())
        average_wt = total_wt / num_jobs

        return average_tat, average_wt
        


    #ito yung display ng computation
    def Calculate_FIFO(self):
        
        try:
            #gagawa bagong window
            solution_window = tk.Toplevel(self.window)
            solution_window.title("SOLUTION")
            solution_window.geometry("900x500")
            #Ito yung paglalagyan ng result
            self.gantt_text = tk.Text(solution_window, height=15, width=150)  
            self.gantt_text.grid(row=1, column = 0, columnspan=5) 
            self.gantt_text.config(state=tk.DISABLED)  

            self.completion_text = tk.Text(solution_window, height=15, width=150) 
            self.completion_text.grid(row=2, columnspan=5) 
            self.completion_text.config(state=tk.DISABLED) 
            process_list = []
            for arrival_entry, burst_entry in self.process_list_list:
                arrival_time = int(arrival_entry.get())
                burst_time = int(burst_entry.get())
                process_list.append([arrival_time, burst_time, f"p{len(process_list) + 1}"])
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for arrival and burst times.")
            return

        gantt, completed = self.fifo(process_list)
        average_tat, average_wt = self.average(completed)

        # ito yung sa gantt chart
        self.gantt_text.config(state=tk.NORMAL)
        self.gantt_text.delete(1.0, tk.END)
        self.gantt_text.insert(tk.END, "Gantt Chart:\n")
        for task, ct in gantt:
            self.gantt_text.insert(tk.END, f"  {task} ||  \n")
            self.gantt_text.insert(tk.END, f"{' ' * 5}({ct})\n")
        self.gantt_text.insert(tk.END, "\n\n")
        self.gantt_text.insert(tk.END, "Timeline:\n") #kulang timeline

        self.gantt_text.config(state=tk.DISABLED)  # Disable text widget after insertion

        #ito yung sa table
        self.completion_text.config(state=tk.NORMAL)
        self.completion_text.delete(1.0, tk.END)
        self.completion_text.insert(tk.END, "Completion Times:\n")
        self.completion_text.insert(tk.END, f"||   JOB   ||   Completion Time   ||   Turn Around Time   ||   Waiting Time   ||\n")
        for pid, values in completed.items():
            self.completion_text.insert(tk.END, f"{' ' * 6}{pid}{' ' * 16}{values[0]}{' ' * 24}{values[1]}{' ' * 11}{values[2]}{' ' * 10}\n")
        self.completion_text.insert(tk.END,"\n")
        self.completion_text.insert(tk.END, "Average:\n")
        self.completion_text.insert(tk.END, f"Turn Around Time: {average_tat: .2f} \n")
        self.completion_text.insert(tk.END, f"Waiting TIme: {average_wt: .2f} \n")
        self.completion_text.config(state=tk.DISABLED)  # Disable text widget after insertion  
        