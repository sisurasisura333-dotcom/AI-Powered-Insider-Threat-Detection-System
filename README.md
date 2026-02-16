# AI-Powered Insider Threat Detection System

A professional SOC-style dashboard that predicts insider threats using AI and real-time user activity logs.  
This system simulates a Security Operations Center (SOC) with alerts, charts, and live monitoring.


| Feature               | Description                                                                                                                                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Live Log Simulation   | Simulates user activity logs in real-time and updates the dashboard automatically                                                                       |
| AI Risk Analysis      | Calculates risk scores for each user based on login hours, file access, downloads, failed logins, USB usage, sensitive file access, and network uploads |
| Risk Level Table      | Table showing LOW, MEDIUM, HIGH risk users with color-coded rows                                                                                        |
| Visualizations        | Pie chart showing risk distribution and bar chart showing risk scores per user                                                                          |
| High-Risk Alerts      | Popup alerts and sound notifications for high-risk users                                                                                                |
| Dark/Light Theme      | Toggle between dark and light UI themes                                                                                                                 |
| Start/Stop Simulation | Start or stop live log simulation at any time                                                                                                           |
| Export Reports        | Export analyzed data to CSV for documentation                                                                                                           |


| Step | Action                                                                     |
| ---- | -------------------------------------------------------------------------- |
| 1    | Click **Load Logs** and select `sample_logs.csv`                           |
| 2    | Click **Analyze Threats** to calculate risk scores and populate the table  |
| 3    | Observe charts showing risk distribution and user risk scores              |
| 4    | Click **Start Live Simulation** to see real-time updates every few seconds |
| 5    | Click **Stop Simulation** to pause live updates                            |
| 6    | Toggle **Dark/Light Theme** for preferred view                             |
| 7    | Click **Export Report** to save CSV file of results                        |

Sample Logs

| username | login_hour | files_accessed | files_downloaded | failed_logins | usb_used | sensitive_access | network_uploads |
| -------- | ---------- | -------------- | ---------------- | ------------- | -------- | ---------------- | --------------- |
| alice    | 9          | 5              | 2                | 0             | 0        | 0                | 0               |
| bob      | 2          | 300            | 150              | 5             | 1        | 1                | 200             |
| carol    | 10         | 6              | 4                | 0             | 0        | 0                | 0               |
| dan      | 23         | 200            | 180              | 4             | 1        | 1                | 150             |


Technology Stack

| Technology   | Purpose                        |
| ------------ | ------------------------------ |
| Python       | Main programming language      |
| Tkinter      | GUI development                |
| Pandas       | Data processing                |
| Matplotlib   | Data visualization             |
| Scikit-learn | AI detection models            |
| Winsound     | Alert notifications on Windows |

