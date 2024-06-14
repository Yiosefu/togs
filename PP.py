from tkinter import *  #para magka roon ng GUI
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import heapq
"""
TO DO:
    Timeline
"""
class PP:

    def __init__(self, window):
        self.window = window
        self.window.geometry("1920x1024")
        self.window.title("Preemptive Priority Scheduling")
        
        self.process_label = tk.Label(window, text="Enter The number of Jobs you are going to Process: ", font=('Helvetica', 16))
        self.process_label.grid(row=0, column=0, padx=10, pady=5)
        self.process_entry = tk.Entry(window, width=10)
        self.process_entry.grid(row=0, column=1, padx=10, pady=5) 

        self.button = tk.Button(window, text="Update", command=self.update_table)
        self.button.grid(row=0, column=2, padx=10, pady=5)

        self.process_list = []
        self.gantt_text = None
        self.completion_text = None
        self.process_list_list = []

    def update_table(self):
        try:
            num_jobs = int(self.process_entry.get())
            if num_jobs <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of jobs.")
            return
        
        if hasattr(self, 'input_frame'):
            self.input_frame.destroy()

        self.input_frame = tk.Frame(self.window)
        self.input_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        self.process_list.clear()
        self.process_list_list.clear()
        
        job_title = tk.Label(self.input_frame, font=('Helvetica', 14), text="Job")
        job_title.grid(row=1, column=1)
        AT_title = tk.Label(self.input_frame, font=('Helvetica', 14), text="Arrival time")
        AT_title.grid(row=1, column=2)
        BT_title = tk.Label(self.input_frame, font=('Helvetica', 14), text="Burst Time")
        BT_title.grid(row=1, column=3)
        p_title = tk.Label(self.input_frame, font=('Helvetica', 14), text="Priority")
        p_title.grid(row=1, column=4)

        for i in range(num_jobs):
            job_label = tk.Label(self.input_frame, font=('Helvetica', 14), text=f"Job {i+1}: ", width=5)
            job_label.grid(row=i+2, column=1)
            
            arrival_entry = tk.Entry(self.input_frame)
            arrival_entry.grid(row=i+2, column=2)
            
            burst_entry = tk.Entry(self.input_frame)
            burst_entry.grid(row=i+2, column=3)

            priority_entry = tk.Entry(self.input_frame)
            priority_entry.grid(row=i+2, column=4)
            
            self.process_list.extend([arrival_entry, burst_entry, priority_entry])
            self.process_list_list.append((arrival_entry, burst_entry, priority_entry))

        run_button = tk.Button(self.input_frame, text="Run PP", command=self.Calculate_PP)
        run_button.grid(row=num_jobs+2, column=0, columnspan=5)

    def pp(self, job_list):
        # Sorting job_list based on arrival time
        job_list.sort(key=lambda x: x[1])
        
        current_time = 0
        gantt_chart = []
        completed = {}
        job_queue = []
        
        i = 0
        n = len(job_list)
        while i < n or job_queue:
            while i < n and job_list[i][1] <= current_time:
                heapq.heappush(job_queue, (job_list[i][3], job_list[i][1], job_list[i][2], job_list[i][0]))  # (priority, arrival_time, burst_time, job_id)
                i += 1
            
            if job_queue:
                priority, arrival_time, burst_time, job_id = heapq.heappop(job_queue)
                if not gantt_chart or gantt_chart[-1][0] != job_id:
                    if gantt_chart:
                        last_job, last_start, last_end = gantt_chart[-1]
                        if last_end < current_time:
                            gantt_chart.append((last_job, last_end, current_time))
                    start_time = current_time
                else:
                    start_time = gantt_chart[-1][2]
                    gantt_chart.pop()

                # Run the job for 1 unit of time
                current_time += 1
                burst_time -= 1

                if burst_time > 0:
                    heapq.heappush(job_queue, (priority, arrival_time, burst_time, job_id))
                    gantt_chart.append((job_id, start_time, current_time))
                else:
                    ct = current_time
                    tat = ct - arrival_time
                    wt = tat - (job_list[i-1][2] - burst_time)  # Original burst time - remaining burst time
                    completed[job_id] = (ct, tat, wt)
                    gantt_chart.append((job_id, start_time, current_time))
            else:
                current_time += 1

        return gantt_chart, completed

    def average(self, completed):
        num_jobs = len(completed)
        total_tat = sum(values[1] for values in completed.values())
        average_tat = total_tat / num_jobs

        total_wt = sum(values[2] for values in completed.values())
        average_wt = total_wt / num_jobs

        return average_tat, average_wt

    def Calculate_PP(self):
        try:
            process_list = []
            for arrival_entry, burst_entry, priority_entry in self.process_list_list:
                arrival_time = int(arrival_entry.get())
                burst_time = int(burst_entry.get())
                priority = int(priority_entry.get())
                process_list.append([f"p{len(process_list) + 1}", arrival_time, burst_time, priority])
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for arrival, burst times, and priority.")
            return

        gantt, completed = self.pp(process_list)
        average_tat, average_wt = self.average(completed)

        solution_window = tk.Toplevel(self.window)
        solution_window.title("SOLUTION")
        solution_window.geometry("900x500")

        self.gantt_text = tk.Text(solution_window, height=15, width=150)  
        self.gantt_text.grid(row=1, column=0, columnspan=5) 
        self.gantt_text.config(state=tk.NORMAL)
        self.gantt_text.delete(1.0, tk.END)
        self.gantt_text.insert(tk.END, "Gantt Chart:\n")
        for task, start_time, end_time in gantt:
            self.gantt_text.insert(tk.END, f"{task}  ||\n")
            self.gantt_text.insert(tk.END, f"{' ' * 5}({end_time})\n")
        self.gantt_text.config(state=tk.DISABLED)

        self.completion_text = tk.Text(solution_window, height=15, width=150) 
        self.completion_text.grid(row=2, columnspan=5) 
        self.completion_text.config(state=tk.NORMAL)
        self.completion_text.delete(1.0, tk.END)
        self.completion_text.insert(tk.END, "Completion Times:\n")
        self.completion_text.insert(tk.END, "||   JOB   ||   Completion Time   ||   Turn Around Time   ||   Waiting Time   ||\n")
        for pid, values in completed.items():
            self.completion_text.insert(tk.END, f"{' ' * 6}{pid}{' ' * 16}{values[0]}{' ' * 24}{values[1]}{' ' * 11}{values[2]}{' ' * 10}\n")
        self.completion_text.insert(tk.END, "\nAverage:\n")
        self.completion_text.insert(tk.END, f"Turn Around Time: {average_tat:.2f} \n")
        self.completion_text.insert(tk.END, f"Waiting Time: {average_wt:.2f} \n")
        self.completion_text.config(state=tk.DISABLED)