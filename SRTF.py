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
class SRTF:

    def __init__(self, window):
        self.window = window
        self.window.geometry("1920x1024")
        self.window.title("SRTF")
        
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

        run_button = tk.Button(self.input_frame, text="Run SRTF", command=self.Calculate_SRTF)
        run_button.grid(row=num_jobs+2, column = 0, columnspan=5)


    #dito icocompute tapos isosort yung algorithm
    """def srtf(self, job_list):
        time = 0
        gantt = []
        completed = {}
        job_list.sort(key=lambda x: (x[1], x[2]))  # Sort jobs by arrival time
        job_queue = []
        index = 0  

        while index < len(job_list) or job_queue:
            # ilalagay sa heap yung mga jobs na nakapasok na
            while index < len(job_list) and job_list[index][1] <= time:
                heapq.heappush(job_queue, (job_list[index][0], job_list[index][1], job_list[index][2]))
                index += 1                              #bt,     at,       id

            if job_queue:
                # ilalabas sa heap  yung pinakamababa yung bt
                burst_time, arrival_time, job_name = heapq.heappop(job_queue)
                gantt.append((job_name, time, time + 1))
                burst_time -= 1
                time += 1
                
                if burst_time > 0:
                    heapq.heappush(job_queue, (burst_time, arrival_time, job_name))  #ibabalik yung job kung may nadaanan
                else:
                    ct = time
                    tat = ct - arrival_time
                    wt = tat - burst_time
                    completed[job_name] = [ct, tat, wt]
            else:
                time += 1

        return gantt, completed"""

    def average(self, completed):
        num_jobs = int(self.process_entry.get())
        total_tat = sum(values[1] for values in completed.values())
        average_tat = total_tat / num_jobs

        total_wt = sum(values[2]for values in completed.values())
        average_wt = total_wt / num_jobs

        return average_tat, average_wt
    
    
    def Calculate_SRTF(self):
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

        gantt, completed = self.srtf(process_list)
        average_tat, average_wt = self.average(completed)

        # ito yung sa gantt chart
        self.gantt_text.config(state=tk.NORMAL)
        self.gantt_text.delete(1.0, tk.END)
        self.gantt_text.insert(tk.END, "Gantt Chart:\n")
        for task, start_time, end_time in gantt:
            self.gantt_text.insert(tk.END, f"{task}  ||  \n")
            self.gantt_text.insert(tk.END, f"{' '* 5} ({end_time}) \n")
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