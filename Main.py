import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from time import time
import re


# reading all files with error handling
def read_files(filenames):
    file_contents = []
    for filename in filenames:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                if content:  # Check if the file is not empty
                    file_contents.append({"file_name": filename, "content": content})
                else:
                    print(f"Warning: {filename} is empty.")
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except Exception as e:
            print(f"Error: {filename} could not be read due to {e}")
    return file_contents


# finding row and column number of the match
def find_row_column(text, index):
    lines = text.splitlines()
    running_length = 0
    for row_num, line in enumerate(lines):
        if running_length + len(line) >= index:
            column_num = index - running_length
            return row_num + 1, column_num + 1
        running_length += len(line) + 1
    return -1, -1


# Brute Force Search with whole word option
def brute_force_search(text, pattern, case_sensitive=False, whole_word=False):  # o(n*m)
    matches = []

    # adjust for case sensitivity
    if not case_sensitive:
        text = text.lower()
        pattern = pattern.lower()

    # define regex based on whether we need whole word or substring match
    
    # Whole word match
    if whole_word:
        regex = rf"\b{re.escape(pattern)}\b"  
        
    # Substring within a word match
    else:
        regex = rf"\w*{re.escape(pattern)}\w*"  

    # Find all matches using the regex
    for match in re.finditer(regex, text):
        word = match.group()
        start_index = match.start()
        row, col = find_row_column(text, start_index)
        matches.append(f"Match at row {row}, column {col}: {word}")

    return matches


# KMP Search with whole word option
def kmp_search(text, pattern, case_sensitive=False, whole_word=False):  # o(n+m)
    matches = []

    # ddjust for case sensitivity
    if not case_sensitive:
        text = text.lower()
        pattern = pattern.lower()

    # define regex based on whether we need whole word or substring match
    
    # whole word match
    if whole_word:
        regex = rf"\b{re.escape(pattern)}\b"  
        
    # substring within a word match
    else:
        regex = rf"\w*{re.escape(pattern)}\w*"  
        
    # find all matches using the regex
    for match in re.finditer(regex, text):
        word = match.group()
        start_index = match.start()
        row, col = find_row_column(text, start_index)
        matches.append(f"Match at row {row}, column {col}: {word}")

    return matches


#  Benchmarking the algorithms
def benchmark_algorithms(files, keyword, case_sensitive=False, whole_word=False):
    results = {}

    start_time = time()
    brute_force_results = search_keyword(
        files, keyword, case_sensitive, whole_word, "brute_force"
    )
    results["Brute Force"] = time() - start_time

    start_time = time()
    kmp_results = search_keyword(files, keyword, case_sensitive, whole_word, "kmp")
    results["KMP"] = time() - start_time

    return brute_force_results, kmp_results, results


# search function that calls appropriate search algorithms
def search_keyword(
    files, keyword, case_sensitive=False, whole_word=False, algorithm="brute_force"
):
    search_results = []
    for file in files:
        matches = []
        if algorithm == "brute_force":
            matches = brute_force_search(
                file["content"], keyword, case_sensitive, whole_word
            )
        elif algorithm == "kmp":
            matches = kmp_search(file["content"], keyword, case_sensitive, whole_word)

        if matches:
            search_results.append({"file_name": file["file_name"], "matches": matches})
    return search_results


# tkinter GUI Class
class WordSearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Search Engine")
        self.geometry("600x700")
        self.configure(bg="#f0f7f7")

        # styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TLabel", font=("Arial", 12), background="#f0f7f7", foreground="#333"
        )
        style.configure(
            "TButton",
            font=("Arial", 12, "bold"),
            background="#00796b",
            foreground="#ffffff",
            padding=5,
        )
        style.map("TButton", background=[("active", "#004d40")])
        style.configure(
            "TCheckbutton", font=("Arial", 11), background="#f0f7f7", foreground="#333"
        )
        style.configure("TEntry", font=("Arial", 12), padding=5, relief="flat")
        style.configure(
            "TProgressbar", thickness=20, troughcolor="#e0e0e0", background="#00796b"
        )

        # main frame
        self.main_frame = tk.Frame(self, bg="#f0f7f7")
        self.main_frame.pack(expand=True)

        # widgets
        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(
            self.main_frame,
            text="Welcome to Your Word Search Engine",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(
            row=0, column=0, columnspan=2, pady=(5, 15)
        )  # Reduced top padding

        # keyword Entry
        keyword_frame = tk.Frame(self.main_frame, bg="#f0f7f7")
        keyword_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Label(keyword_frame, text="Keyword:").grid(row=0, column=0, padx=5)
        self.keyword_entry = ttk.Entry(keyword_frame, width=25)
        self.keyword_entry.grid(row=0, column=1, padx=(0, 10))

        # search Method Dropdown
        self.algorithm_option = ttk.Combobox(
            keyword_frame, values=["brute_force", "kmp", "both"], width=15
        )
        self.algorithm_option.set("brute_force")
        self.algorithm_option.grid(row=0, column=2, padx=5)

        # search Button
        ttk.Button(keyword_frame, text="Search", command=self.perform_search).grid(
            row=0, column=3, padx=5
        )

        # options
        options_frame = tk.Frame(self.main_frame, bg="#f0f7f7")
        options_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.case_sensitive = tk.BooleanVar()
        self.whole_word = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame, text="Case Sensitive", variable=self.case_sensitive
        ).grid(row=0, column=0, padx=5)
        ttk.Checkbutton(
            options_frame, text="Whole Word Only", variable=self.whole_word
        ).grid(row=0, column=1, padx=5)

        # loading Bar
        self.progress = ttk.Progressbar(self.main_frame, mode="determinate", length=500)
        self.progress.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.results_text = scrolledtext.ScrolledText(
            self.main_frame, wrap=tk.WORD, width=65, height=15, font=("Arial", 10)
        )
        self.results_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.results_text.configure(bg="#e0f7fa", fg="#333", state="disabled")

        # execution Time Label and Box
        execution_frame = tk.Frame(self.main_frame, bg="#f0f7f7")
        execution_frame.grid(row=5, column=0, columnspan=2, pady=(10, 20), sticky="w")

        time_label = ttk.Label(
            execution_frame, text="Execution Time:", font=("Arial", 12, "bold")
        )
        time_label.grid(row=0, column=0, sticky="w", padx=10)

        self.time_text = tk.Text(
            execution_frame, height=2, width=65, bg="#e0f7fa", font=("Arial", 10)
        )
        self.time_text.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 20))
        self.time_text.configure(state="disabled", fg="#333")

    def perform_search(self):
        keyword = self.keyword_entry.get().strip()
        case_sensitive = self.case_sensitive.get()
        whole_word = self.whole_word.get()
        algorithm = self.algorithm_option.get()  

        if not keyword:
            messagebox.showwarning("Input Error", "Keyword cannot be empty.")
            return

        filenames = [
            "Research#1.txt",
            "Research#2.txt",
            "Research#3.txt",
            "Research#4.txt",
            "Research#5.txt",
            "Research#6.txt",
            "Research#7.txt",
            "Research#8.txt",
            "Research#9.txt",
            "Research#10.txt",
        ]
        data = read_files(filenames)

        # show progress bar effect and execute search after a short delay
        self.progress["value"] = 0
        
        # update UI immediately to show progress bar effect
        self.update_idletasks()  
        self.after(
            100,
            self.execute_search,
            data,
            keyword,
            case_sensitive,
            whole_word,
            algorithm,
        )

    def execute_search(self, data, keyword, case_sensitive, whole_word, algorithm):
        if algorithm == "both":
            brute_force_results, kmp_results, timing = benchmark_algorithms(
                data, keyword, case_sensitive, whole_word
            )
            self.display_results(
                brute_force_results,
                f"Brute Force: {timing['Brute Force']:.4f} s\nKMP: {timing['KMP']:.4f} s",
            )
            self.display_time(
                f"Brute Force: {timing['Brute Force']:.4f} seconds\nKMP: {timing['KMP']:.4f} seconds"
            )
        else:
            # Simulate progress bar for single algorithm search
            for i in range(0, 101, 20):
                self.progress["value"] = i
                self.update_idletasks()
                self.after(50)

            start_time = time()
            results = search_keyword(
                data, keyword, case_sensitive, whole_word, algorithm
            )
            execution_time = time() - start_time
            self.display_results(results)
            self.display_time(
                f"{algorithm.capitalize()} Execution Time: {execution_time:.4f} seconds"
            )

        # Finish loading bar
        self.progress["value"] = 100

    def display_results(self, results, timings=None):
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        if not results:
            self.results_text.insert(tk.END, "No matches found.\n")
        else:
            for result in results:
                self.results_text.insert(tk.END, f"\nFile: {result['file_name']}\n")
                for match in result["matches"]:
                    self.results_text.insert(tk.END, f" - {match.strip()}\n")
        if timings:
            self.results_text.insert(tk.END, f"\n{timings}")
        self.results_text.config(state="disabled")

    def display_time(self, time_info):
        self.time_text.config(state="normal")
        self.time_text.delete("1.0", tk.END)
        self.time_text.insert(tk.END, time_info)
        self.time_text.config(state="disabled")


if __name__ == "__main__":
    app = WordSearchApp()
    app.mainloop()
