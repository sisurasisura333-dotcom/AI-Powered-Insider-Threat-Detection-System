import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from risk_engine import calculate_risk_score, get_risk_level
from model_engine import run_ai_detection
import winsound  # for alert sound on Windows


class ProfessionalSOC:
    def __init__(self, root):
        self.root = root
        self.root.title("SOC Insider Threat Detection System")
        self.root.geometry("1350x750")
        self.root.configure(bg="#0f172a")

        self.data = pd.DataFrame()
        self.simulation_running = False
        self.dark_mode = True

        # Title
        title = tk.Label(root, text="Professional SOC Insider Threat Dashboard",
                         font=("Segoe UI", 22, "bold"), fg="#38bdf8", bg="#0f172a")
        title.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root, bg="#0f172a")
        btn_frame.pack(pady=10)

        self.load_btn = tk.Button(btn_frame, text="Load Logs", font=("Segoe UI", 12),
                                  bg="#1e293b", fg="white", width=18, command=self.load_logs)
        self.load_btn.grid(row=0, column=0, padx=10)

        self.analyze_btn = tk.Button(btn_frame, text="Analyze Threats", font=("Segoe UI", 12),
                                     bg="#1e293b", fg="white", width=18, command=self.analyze)
        self.analyze_btn.grid(row=0, column=1, padx=10)

        self.export_btn = tk.Button(btn_frame, text="Export Report", font=("Segoe UI", 12),
                                    bg="#1e293b", fg="white", width=18, command=self.export)
        self.export_btn.grid(row=0, column=2, padx=10)

        self.simulate_btn = tk.Button(btn_frame, text="Start Live Simulation", font=("Segoe UI", 12),
                                      bg="#1e293b", fg="white", width=20, command=self.start_simulation)
        self.simulate_btn.grid(row=0, column=3, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="Stop Simulation", font=("Segoe UI", 12),
                                  bg="#ef4444", fg="white", width=18, command=self.stop_simulation)
        self.stop_btn.grid(row=0, column=4, padx=10)

        self.theme_btn = tk.Button(btn_frame, text="Toggle Dark/Light", font=("Segoe UI", 12),
                                   bg="#1e293b", fg="white", width=18, command=self.toggle_theme)
        self.theme_btn.grid(row=0, column=5, padx=10)

        # High Risk Counter
        self.counter_label = tk.Label(root, text="High Risk Users: 0",
                                      font=("Segoe UI", 14, "bold"), fg="#ef4444", bg="#0f172a")
        self.counter_label.pack()

        # Table
        table_frame = tk.Frame(root, bg="#0f172a")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#1e293b", foreground="white", rowheight=25,
                        fieldbackground="#1e293b", font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"),
                        background="#0ea5e9", foreground="black")
        style.map("Treeview", background=[('selected', '#2563eb')])

        self.tree = ttk.Treeview(table_frame, columns=("User", "Score", "Level"), show="headings")
        self.tree.heading("User", text="Username")
        self.tree.heading("Score", text="Risk Score")
        self.tree.heading("Level", text="Risk Level")
        self.tree.column("User", width=250)
        self.tree.column("Score", width=150)
        self.tree.column("Level", width=150)
        self.tree.pack(fill="both", expand=True)

        # Chart frame
        self.chart_frame = tk.Frame(root, bg="#0f172a")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Status bar
        self.status = tk.Label(root, text="Status: Ready", font=("Segoe UI", 10),
                               fg="white", bg="#020617", anchor="w")
        self.status.pack(fill="x")

    def load_logs(self):
        file = filedialog.askopenfilename()
        if file:
            self.data = pd.read_csv(file)
            self.status.config(text="Status: Logs Loaded")
            messagebox.showinfo("Success", "Logs loaded successfully")

    def analyze(self):
        if self.data.empty:
            messagebox.showerror("Error", "Load logs first")
            return

        self.status.config(text="Status: Analyzing threats...")
        self.data = run_ai_detection(self.data)

        scores = []
        levels = []

        for _, row in self.data.iterrows():
            score = calculate_risk_score(row)
            level = get_risk_level(score)
            scores.append(score)
            levels.append(level)

        self.data['risk_score'] = scores
        self.data['risk_level'] = levels

        # Update table
        for item in self.tree.get_children():
            self.tree.delete(item)

        high_risk_count = 0
        for _, row in self.data.iterrows():
            if row['risk_level'] == "HIGH":
                high_risk_count += 1
                winsound.Beep(1000, 300)  # Play sound for high-risk
            self.tree.insert("", "end", values=(row['username'], row['risk_score'], row['risk_level']))

        # Color rows dynamically
        for i, row in enumerate(self.tree.get_children()):
            level = self.tree.item(row)['values'][2]
            if level == "LOW":
                self.tree.tag_configure('low', background='#10b981', foreground='black')
                self.tree.item(row, tags=('low',))
            elif level == "MEDIUM":
                self.tree.tag_configure('medium', background='#facc15', foreground='black')
                self.tree.item(row, tags=('medium',))
            else:
                self.tree.tag_configure('high', background='#ef4444', foreground='white')
                self.tree.item(row, tags=('high',))

        self.counter_label.config(text=f"High Risk Users: {high_risk_count}")
        self.status.config(text="Status: Analysis Complete")

        if high_risk_count > 0:
            messagebox.showwarning("SOC ALERT", f"{high_risk_count} High Risk Users Detected")

        # Update charts
        self.update_charts()

    def update_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(8, 3), dpi=100)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # Pie chart for risk distribution
        risk_counts = self.data['risk_level'].value_counts()
        labels = risk_counts.index
        sizes = risk_counts.values
        colors = ['#10b981', '#facc15', '#ef4444']  # LOW, MEDIUM, HIGH
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.set_title("Risk Level Distribution")

        # Bar chart for user scores
        ax2.bar(self.data['username'], self.data['risk_score'],
                color=['#10b981' if l == "LOW" else '#facc15' if l == "MEDIUM" else '#ef4444'
                       for l in self.data['risk_level']])
        ax2.set_xticklabels(self.data['username'], rotation=45, ha='right')
        ax2.set_ylabel("Risk Score")
        ax2.set_title("Risk Scores by User")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def export(self):
        if self.data.empty:
            return
        self.data.to_csv("threat_report.csv", index=False)
        self.status.config(text="Status: Report Exported")
        messagebox.showinfo("Exported", "Threat report saved successfully")

    # Live log simulation
    def start_simulation(self):
        if self.data.empty:
            messagebox.showerror("Error", "Load logs first")
            return
        self.simulation_running = True
        self.status.config(text="Status: Live Simulation Running...")
        self.simulate_logs()

    def stop_simulation(self):
        self.simulation_running = False
        self.status.config(text="Status: Simulation Stopped")

    def simulate_logs(self):
        if not self.simulation_running:
            return

        # Randomly pick a user to simulate suspicious behavior
        idx = random.randint(0, len(self.data) - 1)
        self.data.at[idx, 'login_hour'] = random.randint(0, 23)
        self.data.at[idx, 'files_accessed'] = random.randint(1, 300)
        self.data.at[idx, 'files_downloaded'] = random.randint(1, 300)
        self.data.at[idx, 'failed_logins'] = random.randint(0, 5)
        self.data.at[idx, 'usb_used'] = random.randint(0, 1)
        self.data.at[idx, 'sensitive_access'] = random.randint(0, 1)
        self.data.at[idx, 'network_uploads'] = random.randint(0, 300)

        # Re-run analysis
        self.analyze()

        # Repeat simulation every 5 seconds
        self.root.after(5000, self.simulate_logs)

    # Toggle Dark/Light theme
    def toggle_theme(self):
        if self.dark_mode:
            self.root.configure(bg="white")
            self.counter_label.configure(bg="white", fg="black")
            self.status.configure(bg="lightgrey", fg="black")
            self.chart_frame.configure(bg="white")
            self.dark_mode = False
        else:
            self.root.configure(bg="#0f172a")
            self.counter_label.configure(bg="#0f172a", fg="#ef4444")
            self.status.configure(bg="#020617", fg="white")
            self.chart_frame.configure(bg="#0f172a")
            self.dark_mode = True


root = tk.Tk()
app = ProfessionalSOC(root)
root.mainloop()
