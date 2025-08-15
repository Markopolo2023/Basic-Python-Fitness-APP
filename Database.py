import tkinter as tk
from tkinter import ttk
import csv







#--------------------------------------------------------------------Database input-------------------------------------------------------------------------------------
def save_selection():
    with open('Selection.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            workoutfocus_entry.get(),
            grouping_entry.get(),
            opposite_entry.get(),
            imbalance_entry.get(),
            injury_entry.get(),
            exercise_entry.get()
        ])
    clear_selection_entries()

def save_modes():
    with open('Modes.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            type_entry.get(),
            sets_entry.get(),
            reps_entry.get(),
            time_entry.get(),
            rest_time_entry.get()
        ])
    clear_modes_entries()

def clear_selection_entries():
    workoutfocus_entry.delete(0, tk.END)
    grouping_entry.delete(0, tk.END)
    opposite_entry.delete(0, tk.END)
    imbalance_entry.delete(0, tk.END)
    injury_entry.delete(0, tk.END)
    exercise_entry.delete(0, tk.END)

def clear_modes_entries():
    type_entry.delete(0, tk.END)
    sets_entry.delete(0, tk.END)
    reps_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    rest_time_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Data Entry")

selection_frame = ttk.LabelFrame(root, text="Selection")
selection_frame.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

workoutfocus_label = ttk.Label(selection_frame, text="WorkoutFocus:")
workoutfocus_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
workoutfocus_entry = ttk.Entry(selection_frame)
workoutfocus_entry.grid(row=0, column=1, padx=5, pady=2)

grouping_label = ttk.Label(selection_frame, text="Grouping:")
grouping_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')
grouping_entry = ttk.Entry(selection_frame)
grouping_entry.grid(row=1, column=1, padx=5, pady=2)

opposite_label = ttk.Label(selection_frame, text="Opposite:")
opposite_label.grid(row=2, column=0, padx=5, pady=2, sticky='w')
opposite_entry = ttk.Entry(selection_frame)
opposite_entry.grid(row=2, column=1, padx=5, pady=2)

imbalance_label = ttk.Label(selection_frame, text="Imbalance:")
imbalance_label.grid(row=3, column=0, padx=5, pady=2, sticky='w')
imbalance_entry = ttk.Entry(selection_frame)
imbalance_entry.grid(row=3, column=1, padx=5, pady=2)

injury_label = ttk.Label(selection_frame, text="Injury:")
injury_label.grid(row=4, column=0, padx=5, pady=2, sticky='w')
injury_entry = ttk.Entry(selection_frame)
injury_entry.grid(row=4, column=1, padx=5, pady=2)

exercise_label = ttk.Label(selection_frame, text="Exercise:")
exercise_label.grid(row=5, column=0, padx=5, pady=2, sticky='w')
exercise_entry = ttk.Entry(selection_frame)
exercise_entry.grid(row=5, column=1, padx=5, pady=2)

save_selection_button = ttk.Button(selection_frame, text="Save Selection", command=save_selection)
save_selection_button.grid(row=6, columnspan=2, padx=5, pady=5)

modes_frame = ttk.LabelFrame(root, text="Modes")
modes_frame.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

type_label = ttk.Label(modes_frame, text="Type:")
type_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
type_entry = ttk.Entry(modes_frame)
type_entry.grid(row=0, column=1, padx=5, pady=2)

sets_label = ttk.Label(modes_frame, text="Sets:")
sets_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')
sets_entry = ttk.Entry(modes_frame)
sets_entry.grid(row=1, column=1, padx=5, pady=2)

reps_label = ttk.Label(modes_frame, text="Reps:")
reps_label.grid(row=2, column=0, padx=5, pady=2, sticky='w')
reps_entry = ttk.Entry(modes_frame)
reps_entry.grid(row=2, column=1, padx=5, pady=2)

time_label = ttk.Label(modes_frame, text="Time (min):")
time_label.grid(row=3, column=0, padx=5, pady=2, sticky='w')
time_entry = ttk.Entry(modes_frame)
time_entry.grid(row=3, column=1, padx=5, pady=2)

rest_time_label = ttk.Label(modes_frame, text="Rest Time (sec):")
rest_time_label.grid(row=4, column=0, padx=5, pady=2, sticky='w')
rest_time_entry = ttk.Entry(modes_frame)
rest_time_entry.grid(row=4, column=1, padx=5, pady=2)

save_modes_button = ttk.Button(modes_frame, text="Save Modes", command=save_modes)
save_modes_button.grid(row=5, columnspan=2, padx=5, pady=5)

root.mainloop()
#--------------------------------------------------------------------Database input-------------------------------------------------------------------------------------




