import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random
import os


#------------------------------------------------------------------------------------------------- Functions for selecting, loading, saving, and HTML page set up

def clear_previous_values():
    with open('Workout.html', 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if "Your estimated VO2 max is:" not in line and "Your estimated one-rep max (1RM) is:" not in line:
                file.write(line)
        file.truncate()

def save_values_to_workout_file():
    clear_previous_values()
    vo2max_value = vo2max_result_label.cget("text")
    estimated_1rm_value = result_label.cget("text")
    user_text = user_text_entry.get("1.0", tk.END).strip()  # Get text from Text widget
    with open('Workout.html', 'a') as file:
        file.write(f"<p>{vo2max_value}</p>\n")
        file.write(f"<p>{user_text}: {estimated_1rm_value}</p>\n")
    # Clear the input text after saving
    user_text_entry.delete("1.0", tk.END)



# Function definitions for workout selection
def load_selection():
    selection_options = set()  # Remove "Random" from the default options
    with open('Selection.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            selection_options.add(row[0])
    return list(selection_options)

def load_modes():
    modes_options = set()
    with open('Modes.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            modes_options.add(row[0])
    return list(modes_options)

def load_3rd_column_options(workout_focus):
    options = set()
    with open('Selection.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == workout_focus:
                options.add(row[3])
    return list(options)

def load_4th_column_options(workout_focus, has_imbalance):
    options = set()
    with open('Selection.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == workout_focus and row[3] == has_imbalance:
                options.add(row[4])
    return list(options)

def load_modality_options(workout_focus):
    options = set()
    with open('Selection.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == workout_focus:
                options.add(row[1])
    return list(options)

def get_random_focus():
    selection_options = load_selection()
    return random.choice(selection_options)

def on_random():
    # Select a random workout focus
    workout_focus = get_random_focus()

    # Update the combobox selection
    workout_focus_combobox.set(workout_focus)

    # Clear selections for imbalance and injury
    has_imbalance_combobox.set("No")
    has_injury_combobox.set("No")


def on_focus_select(event):
    workout_focus = workout_focus_combobox.get().strip()
    if workout_focus:
        # Load and set options for the "Modality" menu
        modality_options = load_modality_options(workout_focus)
        modality_combobox['values'] = modality_options

        # Load and set options for the "Imbalance" menu based on the selected "Workout Focus"
        options = load_3rd_column_options(workout_focus)
        has_imbalance_combobox['values'] = options

        # Update injury options based on workout focus and has imbalance
        has_imbalance = has_imbalance_combobox.get().strip()
        if has_imbalance:
            injury_options = load_4th_column_options(workout_focus, has_imbalance)
            has_injury_combobox['values'] = injury_options


# Function to save the workout to a file
def save_to_file(info_text):
    with open('Workout.html', 'a') as file:
        file.write(info_text.strip() + '\n\n')

# Function to display the matching rows based on workout focus, imbalance, and injury
def on_submit():
    workout_focus = workout_focus_combobox.get().strip()
    has_imbalance = has_imbalance_combobox.get().strip()
    has_injury = has_injury_combobox.get().strip()
    selected_mode = selected_mode_combobox.get().strip()

    if workout_focus.lower() == "random":
        # If "Random" is selected, choose a random workout focus
        workout_focus = get_random_focus()

    matching_rows = get_matching_rows(workout_focus, has_imbalance, has_injury)

    # Clear the existing content in the info_display Text widget
    info_display.delete('1.0', tk.END)

    # Display the entries with save buttons
    display_entries(matching_rows)

# Function to retrieve matching rows from the CSV file
def get_matching_rows(workout_focus, has_imbalance, has_injury):
    def matches_additional_criteria(row):
        # Convert all values to lowercase for case-insensitive comparison
        row_workout_focus = row[0].lower()
        row_has_imbalance = row[3].lower()
        row_has_injury = row[4].lower()

        # Check if the row matches the criteria
        return row_workout_focus == workout_focus.lower() and \
               row_has_imbalance == has_imbalance.lower() and \
               row_has_injury == has_injury.lower()

    matching_rows = []
    with open('Selection.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if matches_additional_criteria(row):
                matching_rows.append(row)

    if not matching_rows:
        print("No matching rows found.")
    else:
        for row in matching_rows:
            print(row)

    return matching_rows

# Function to display entries in the Text widget
def display_entries(matching_rows):
    for index, row in enumerate(matching_rows, start=1):
        exercise_text = f"Exercise: {row[5]}\n"
        mode_info = print_matching_modes(selected_mode_combobox.get())
        if mode_info:
            mode_info_text = f"Sets: {mode_info[1]}\nReps: {mode_info[2]}\nTime: {mode_info[3]}\nRest Time: {mode_info[4]}\n\n"
        else:
            mode_info_text = ""
        
        entry_text = exercise_text + mode_info_text

        # Display the entry text in the info_display Text widget
        info_display.insert(tk.END, entry_text, 'entry_font')
        info_display.insert(tk.END,  " " * 1)  # Add space after the text
        
        # Creating the save button under each entry
        save_button = ttk.Button(root, text="Save", command=lambda text=entry_text: save_selected_entry(text))
        info_display.window_create(tk.END, window=save_button)
        info_display.insert(tk.END, "\n\n")  # Add space after the button

# Function to print matching modes
def print_matching_modes(selected_mode):
    with open('Modes.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == selected_mode:
                return row

# Function to save the selected entry to a file
def save_selected_entry(entry_text, font_size=12):
    # Split the entry text into lines to format each selection on a new line
    entry_lines = entry_text.strip().split('\n')

    # Create HTML code for each selection in a vertical list with specified font size
    formatted_entry = f'<div style="display: flex; justify-content: center;">\n'
    
    # Left column for exercise details
    formatted_entry += '<div style="text-align: center; font-size: {font_size}px;">\n'
    for line in entry_lines:
        if line.startswith("Exercise:"):
            formatted_entry += f'<input type="checkbox" style="border: 1px solid black;"> {line}<br>\n'
        else:
            formatted_entry += f'{line}<br>\n'
    formatted_entry += '</div>\n'
    
    # Right column for notes
    formatted_entry += '<div style="border-left: 1px solid black; padding-left: 10px; margin-left: 10px;">\n'
    formatted_entry += '<b>Notes:</b><br>\n'
    formatted_entry += '</div>\n'
    
    formatted_entry += '</div><br><br>\n'

    # Add the formatted entry to the HTML file
    with open('Workout.html', 'a') as file:
        file.write(formatted_entry)

# Function to print the workout
def print_workout():
    os.startfile("Workout.html")

# Function to delete the workout file
def delete_workout_file():
    confirm = messagebox.askyesno("Confirmation", "Are you sure you wish to delete this workout? A blank one will be auto-generated.")
    if confirm:
        try:
            os.remove("Workout.html")
            messagebox.showinfo("Success", "Workout file deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            # Create an empty Workout.html file if it doesn't exist
    with open('Workout.html', 'a'):
        pass
        banner_text = "\n\n<div class='banner'><span class='workout'>Workout</span> <span class='plan'>Plan</span></div>\n\n"
        with open('Workout.html', 'a') as file:
            if file.tell() == 0:  # Check if the file is empty
                # Write the banner text with specified font, color, and size options
                file.write('<html>\n<head>\n<style>\n')
                file.write('body { font-family: Arial; position: relative; }\n')
                file.write('.banner { font-size: 40px; display: block; border-bottom: 2px solid black; padding:40px; text-align: center; margin: 0 auto; }\n')
                file.write('.workout { color: blue; }\n')
                file.write('.plan { color: #90EE90; }\n')
                file.write('.logo-container { position: absolute; top: 10px; right: 10px; }\n')  # Position logo at the top right
                file.write('.logo-container img { width: 100px; height: 100px; }\n')  # Adjust the width and height as needed
                file.write('</style>\n</head>\n<body>\n')
                file.write('<div class="logo-container"><img src="Logo.jpg" alt="Logo"></div>\n')  # Logo at the top right
                file.write(banner_text)
                file.write('</body>\n</html>\n')




#------------------------------------------------------------------------------------------------- GUI Window 

# Main window
root = tk.Tk()
root.title("Workout Selection Tool")

# Define custom font
entry_font = ('TkDefaultFont', 8)

# Workout Selection GUI
workout_frame = ttk.Frame(root)
workout_frame.grid(row=0, column=0, padx=10, pady=5)

workout_focus_label = ttk.Label(workout_frame, text="Workout Focus:")
workout_focus_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
workout_focus_options = load_selection()
workout_focus_combobox = ttk.Combobox(workout_frame, values=workout_focus_options)
workout_focus_combobox.grid(row=0, column=1, padx=5, pady=2)
workout_focus_combobox.bind("<<ComboboxSelected>>", on_focus_select)

modality_label = ttk.Label(workout_frame, text="Modality:")
modality_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')
modality_combobox = ttk.Combobox(workout_frame)
modality_combobox.grid(row=1, column=1, padx=5, pady=2)

has_imbalance_label = ttk.Label(workout_frame, text="Do you have an Imbalance here?")
has_imbalance_label.grid(row=2, column=0, padx=5, pady=2, sticky='w')
has_imbalance_combobox = ttk.Combobox(workout_frame, values=["Yes", "No"])
has_imbalance_combobox.grid(row=2, column=1, padx=5, pady=2)
has_imbalance_combobox.bind("<<ComboboxSelected>>", on_focus_select)

has_injury_label = ttk.Label(workout_frame, text="Injury?")
has_injury_label.grid(row=3, column=0, padx=5, pady=2, sticky='w')
has_injury_combobox = ttk.Combobox(workout_frame)
has_injury_combobox.grid(row=3, column=1, padx=5, pady=2)

selected_mode_label = ttk.Label(workout_frame, text="I want to perform this exercise for what purpose?")
selected_mode_label.grid(row=4, column=0, padx=5, pady=2, sticky='w')
selected_mode_options = load_modes()
selected_mode_combobox = ttk.Combobox(workout_frame, values=selected_mode_options)
selected_mode_combobox.grid(row=4, column=1, padx=5, pady=2)

random_button = ttk.Button(workout_frame, text="Random Exercise", command=on_random)
random_button.grid(row=5, columnspan=2, padx=5, pady=5)

submit_button = ttk.Button(workout_frame, text="Submit", command=on_submit)
submit_button.grid(row=6, columnspan=2, padx=5, pady=5)


# Display area for workout selection results
info_display = tk.Text(root, height=30, width=80)
info_display.grid(row=1, columnspan=1, padx=5, pady=5)

# Buttons for saving, printing, and clearing workout data
save_button = ttk.Button(root, text="Save All Entries", command=lambda: save_selected_entry(info_display.get("1.0", tk.END)))
save_button.grid(row=3, column=0, padx=5, pady=5)

print_workout_button = ttk.Button(root, text="Print Workout", command=print_workout)
print_workout_button.grid(row=3, column=1, padx=5, pady=5)

clear_button = ttk.Button(root, text="Clear Workout Data", command=delete_workout_file)
clear_button.grid(row=4, columnspan=5, padx=5, pady=5)

# Configure tags for formatting
info_display.tag_configure('entry_font', font=entry_font)




#------------------------------------------------------------------------------------------------- 1 RM and and VO2 Max Calulations and GUI 


# Function definitions for VO2 max calculation
def calculate_vo2max(age, weight_lb, time_minutes, heart_rate, gender):
    # Constants for the Rockport Fitness Walking Test formula
    a = 132.853 - (0.0769 * age) - (0.3877 * weight_lb) + (6.315 * gender) - (3.2649 * time_minutes) - (0.1565 * heart_rate)
    # VO2 max calculation
    vo2max = a
    return vo2max

def calculate_vo2max_and_display():
    try:
        age = int(age_entry.get())
        weight_lb = int(weight_entry.get())
        time_minutes = int(time_entry.get())
        heart_rate = int(heart_rate_entry.get())
        gender = float(gender_combobox.get())

        vo2max = calculate_vo2max(age, weight_lb, time_minutes, heart_rate, gender)
        vo2max_result_label.config(text=f"Your estimated VO2 max is: {vo2max}")
    
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid values.")


# VO2 Max Estimator GUI
vo2max_frame = ttk.Frame(root)
vo2max_frame.grid(row=0, column=2, padx=10, pady=5)

age_label = ttk.Label(vo2max_frame, text="Age (years):")
age_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
age_entry = ttk.Entry(vo2max_frame)
age_entry.grid(row=0, column=1, padx=5, pady=2)

weight_label = ttk.Label(vo2max_frame, text="Weight (lb):")
weight_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')
weight_entry = ttk.Entry(vo2max_frame)
weight_entry.grid(row=1, column=1, padx=5, pady=2)

time_label = ttk.Label(vo2max_frame, text="Time to complete 1 mile walk (minutes):")
time_label.grid(row=2, column=0, padx=5, pady=2, sticky='w')
time_entry = ttk.Entry(vo2max_frame)
time_entry.grid(row=2, column=1, padx=5, pady=2)

heart_rate_label = ttk.Label(vo2max_frame, text="Heart Rate (10 seconds at the end of the 1-mile walk):")
heart_rate_label.grid(row=3, column=0, padx=5, pady=2, sticky='w')
heart_rate_entry = ttk.Entry(vo2max_frame)
heart_rate_entry.grid(row=3, column=1, padx=5, pady=2)

gender_label = ttk.Label(vo2max_frame, text="Gender (0 for female, 1 for male):")
gender_label.grid(row=4, column=0, padx=5, pady=2, sticky='w')
gender_combobox = ttk.Combobox(vo2max_frame, values=["0", "1"])
gender_combobox.grid(row=4, column=1, padx=5, pady=2)

calculate_vo2max_button = ttk.Button(vo2max_frame, text="Calculate VO2 max", command=calculate_vo2max_and_display)
calculate_vo2max_button.grid(row=5, columnspan=2, padx=5, pady=5)

vo2max_result_label = ttk.Label(vo2max_frame, text="")
vo2max_result_label.grid(row=6, columnspan=2)


# Function definitions for 1RM estimation
def calculate_1rm(weight_lifted, reps_completed):
    if reps_completed < 1:
        return "Invalid input: Reps completed must be at least 1"
    
    if reps_completed == 1:
        return weight_lifted
    
    # Epley Formula for estimating 1RM
    estimated_1rm = weight_lifted * (1 + reps_completed / 30)
    return round(estimated_1rm, 2)


def calculate_1rm_and_display():
    try:
        # Convert weight_lifted to an integer
        weight_lifted_str = weight_entry.get().strip()
        weight_lifted = float(weight_lifted_str)
        
        reps_completed = float(reps_entry.get())
        
        if reps_completed < 1:
            messagebox.showerror("Error", "Reps completed must be at least 1")
            return
        
        if reps_completed == 1:
            estimated_1rm = weight_lifted
        else:
            # Epley Formula for estimating 1RM
            estimated_1rm = calculate_1rm(weight_lifted, reps_completed)
        
        result_label.config(text=f"Your estimated one-rep max (1RM) is: {estimated_1rm} pounds")
    
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

# 1RM Estimator GUI
rm_frame = ttk.Frame(root)
rm_frame.grid(row=0, column=3, padx=10, pady=5)

weight_label = ttk.Label(rm_frame, text="Weight Lifted (lbs):")
weight_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
weight_entry = ttk.Entry(rm_frame)
weight_entry.grid(row=0, column=1, padx=5, pady=2)

reps_label = ttk.Label(rm_frame, text="Repetitions Completed:")
reps_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')
reps_entry = ttk.Entry(rm_frame)
reps_entry.grid(row=1, column=1, padx=5, pady=2)

calculate_button = ttk.Button(rm_frame, text="Calculate 1RM", command=calculate_1rm_and_display)
calculate_button.grid(row=2, columnspan=2, padx=5, pady=5)

result_label = ttk.Label(rm_frame, text="")
result_label.grid(row=3, columnspan=2)

# Entry for user to input text
user_text_label = ttk.Label(rm_frame, text="What is this 1RPM for?")
user_text_label.grid(row=4, column=0, padx=5, pady=2, sticky='w')
user_text_entry = tk.Text(rm_frame, height=1, width=30)
user_text_entry.grid(row=4, column=1, padx=5, pady=2, columnspan=2)

# Button to save values to Workout.html
save_values_button = ttk.Button(root, text="Save 1RPM and/or VO2 Max Values to Workout.html", command=save_values_to_workout_file)
save_values_button.grid(row=3, column=3, columnspan=2, padx=5, pady=5)

root.mainloop()

