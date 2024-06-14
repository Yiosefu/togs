import tkinter as tk

def fcfs(process_list):
    time = 0
    gantt = []
    completed = {}
    process_list.sort()

    while process_list != []:
        if process_list[0][0] > time:
            time += 1
            gantt.append(("idle", time))
            continue
        else:
            process = process_list.pop(0)
            gantt.append((process[2], time))
            time += process[1]
            pid = process[2]
            ct = time
            tat = ct - process[0]
            wt = tat - process[1]
            completed[pid] = [ct, tat, wt]
    return gantt, completed

class FIFO:
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x600")
        self.window.title("FIFO")

        self.job_labels = []
        self.arrival_entries = []
        self.burst_entries = []

        self.process_label = tk.Label(window, text="Enter The number of Jobs you are going to Process:", font=('Helvetica', 16))
        self.process_label.grid(row=0, column=0, padx=10, pady=5)
        self.process_entry = tk.Entry(window, width=10)
        self.process_entry.grid(row=0, column=1, padx=10, pady=5)
        self.button = tk.Button(window, text="Update", command=self.update_table)
        self.button.grid(row=0, column=2, padx=10, pady=5)

    def update_table(self):
        try:
            num_jobs = int(self.process_entry.get())
            if num_jobs <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of jobs.")
            return

        for widget in self.window.winfo_children():
            widget.destroy()

        self.job_labels = []
        self.arrival_entries = []
        self.burst_entries = []

        for i in range(num_jobs):
            job_label = tk.Label(self.window, text=f"Job {i+1}:", font=('Helvetica', 14))
            job_label.grid(row=i+1, column=0, padx=10, pady=5)
            self.job_labels.append(job_label)

            arrival_label = tk.Label(self.window, text="Arrival Time:", font=('Helvetica', 14))
            arrival_label.grid(row=i+1, column=1, padx=5, pady=5)
            arrival_entry = tk.Entry(self.window, width=10)
            arrival_entry.grid(row=i+1, column=2, padx=10, pady=5)
            self.arrival_entries.append(arrival_entry)

            burst_label = tk.Label(self.window, text="Burst Time:", font=('Helvetica', 14))
            burst_label.grid(row=i+1, column=3, padx=5, pady=5)
            burst_entry = tk.Entry(self.window, width=10)
            burst_entry.grid(row=i+1, column=4, padx=10, pady=5)
            self.burst_entries.append(burst_entry)

        calculate_button = tk.Button(self.window, text="Calculate", command=self.calculate_FCFS)
        calculate_button.grid(row=num_jobs+1, column=1, padx=10, pady=5)

    def calculate_FCFS(self):
        process_list = []
        for i in range(len(self.job_labels)):
            arrival_time = int(self.arrival_entries[i].get())
            burst_time = int(self.burst_entries[i].get())
            process_list.append([arrival_time, burst_time, f"p{i + 1}"])

        gantt, completed = fcfs(process_list)

        # Display results in a new window
        result_window = tk.Toplevel(self.window)
        result_window.title("FCFS Results")

        result_label = tk.Label(result_window, text="Results", font=('Helvetica', 16))
        result_label.pack()

        gantt_label = tk.Label(result_window, text="Gantt Chart:")
        gantt_label.pack()
        gantt_text = ""
        for task, time in gantt:
            gantt_text += f"{task}({time}) "
        gantt_label = tk.Label(result_window, text=gantt_text)
        gantt_label.pack()

        completion_label = tk.Label(result_window, text="Completion Times:")
        completion_label.pack()
        for pid, values in completed.items():
            completion_text = f"{pid}: {values}"
            completion_label = tk.Label(result_window, text=completion_text)
            completion_label.pack()


# Create main window
root = tk.Tk()
fifo_app = FIFO(root)
root.mainloop()
