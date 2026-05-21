import tkinter as tk
from tkinter import ttk
import pandas as pd
import threading
from camara import run_camera

# ---------------- SETTINGS ----------------
LOW_ATTENDANCE = 75

TEACHERS = {
    "sk": {"password": "1234", "subject": "OOPs"},
    "pg": {"password": "1234", "subject": "COA"},
    "bs": {"password": "1234", "subject": "CG"},
    "bp": {"password": "1234", "subject": "Communication"},
    "ab": {"password": "1234", "subject": "Automata"}
}

# ---------------- LOGIN ----------------
def login():

    user = entry_user.get()
    pwd = entry_pass.get()

    if user in TEACHERS and TEACHERS[user]["password"] == pwd:

        login_window.destroy()
        open_main_app(user)

    else:
        status_label.config(text="Invalid Login ❌")


# ---------------- CAMERA THREAD ----------------
def start_camera(subject, hours, status_label):

    threading.Thread(
        target=run_camera,
        args=(
            subject,
            hours,
            lambda msg: status_label.config(text=msg)
        ),
        daemon=True
    ).start()


# ---------------- MAIN APP ----------------
def open_main_app(user):

    app = tk.Tk()
    app.title("Smart Attendance System")
    app.state("zoomed")
    app.configure(bg="#0b1120")

    subject = TEACHERS[user]["subject"]

    # ---------------- HEADER ----------------
    header = tk.Frame(app, bg="#111827", height=80)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Smart Attendance System",
        font=("Arial", 20, "bold"),
        bg="#111827",
        fg="#60a5fa"
    ).pack(pady=10)

    tk.Label(
        header,
        text=f"Subject: {subject}",
        font=("Arial", 12),
        bg="#111827",
        fg="white"
    ).pack()

    # ---------------- MAIN FRAME ----------------
    main_frame = tk.Frame(app, bg="#0b1120")
    main_frame.pack(pady=30)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "TCombobox",
        fieldbackground="#1e293b",
        background="#1e293b",
        foreground="white"
    )

    # ---------------- YEAR ----------------
    tk.Label(
        main_frame,
        text="Select Year",
        font=("Arial", 11),
        bg="#0b1120",
        fg="white"
    ).grid(row=0, column=0, pady=10)

    year_var = tk.StringVar(value="3")

    year_combo = ttk.Combobox(
        main_frame,
        textvariable=year_var,
        values=["1", "2", "3", "4"],
        width=20,
        state="readonly"
    )

    year_combo.grid(row=0, column=1, padx=10)

    # ---------------- HOURS ----------------
    tk.Label(
        main_frame,
        text="Class Hours",
        font=("Arial", 11),
        bg="#0b1120",
        fg="white"
    ).grid(row=1, column=0, pady=10)

    hours_var = tk.StringVar(value="1")

    hours_combo = ttk.Combobox(
        main_frame,
        textvariable=hours_var,
        values=["1", "2"],
        width=20,
        state="readonly"
    )

    hours_combo.grid(row=1, column=1, padx=10)

    # ---------------- STATUS ----------------
    status = tk.Label(
        app,
        text="System Ready ",
        font=("Arial", 12, "bold"),
        bg="#0b1120",
        fg="#4ade80"
    )

    status.pack(pady=20)

    # ---------------- BUTTON FRAME ----------------
    button_frame = tk.Frame(app, bg="#0b1120")
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Start Camera",
        font=("Arial", 12, "bold"),
        bg="#2563eb",
        fg="white",
        width=18,
        height=2,
        relief="flat",
        command=lambda: start_camera(
            subject,
            hours_var.get(),
            status
        )
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        button_frame,
        text="View Attendance",
        font=("Arial", 12, "bold"),
        bg="#1e293b",
        fg="white",
        width=18,
        height=2,
        relief="flat",
        command=lambda: show_attendance(subject)
    ).grid(row=0, column=1, padx=10)

    # ---------------- FOOTER ----------------
    tk.Label(
        app,
        text="Press Q to close camera",
        bg="#0b1120",
        fg="gray"
    ).pack(side="bottom", pady=10)

    app.mainloop()


# ---------------- VIEW ATTENDANCE ----------------
def show_attendance(subject):

    window = tk.Toplevel()
    window.title("Attendance Sheet")
    window.state("zoomed")
    window.configure(bg="#0b1120")

    tk.Label(
        window,
        text=f"{subject} Attendance",
        font=("Arial", 18, "bold"),
        bg="#0b1120",
        fg="#60a5fa"
    ).pack(pady=15)

    df = pd.read_csv(f"attendance_{subject}.csv")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background="#111827",
        foreground="white",
        rowheight=28,
        fieldbackground="#111827",
        font=("Arial", 10)
    )

    style.configure(
        "Treeview.Heading",
        background="#2563eb",
        foreground="white",
        font=("Arial", 11, "bold")
    )

    tree = ttk.Treeview(
        window,
        columns=("Name", "Attended", "Percentage"),
        show="headings"
    )

    tree.heading("Name", text="Name")
    tree.heading("Attended", text="Attended")
    tree.heading("Percentage", text="Percentage")

    tree.column("Name", width=200)
    tree.column("Attended", width=100)
    tree.column("Percentage", width=120)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    for _, row in df.iterrows():

        tag = ""

        if row["Percentage"] < LOW_ATTENDANCE:
            tag = "low"

        tree.insert(
            "",
            "end",
            values=(
                row["Name"],
                row["Attended"],
                f"{row['Percentage']:.2f}%"
            ),
            tags=(tag,)
        )

    tree.tag_configure("low", foreground="#ef4444")


# ---------------- LOGIN WINDOW ----------------
login_window = tk.Tk()

login_window.title("Smart Attendance Login")
login_window.state("zoomed")
login_window.configure(bg="#0b1120")

# ---------------- CARD FRAME ----------------
frame = tk.Frame(
    login_window,
    bg="#111827",
    padx=30,
    pady=30
)

frame.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- TITLE ----------------
tk.Label(
    frame,
    text="Smart Attendance",
    font=("Arial", 22, "bold"),
    bg="#111827",
    fg="#60a5fa"
).pack(pady=15)

# ---------------- USERNAME ----------------
tk.Label(
    frame,
    text="Username",
    bg="#111827",
    fg="white",
    font=("Arial", 11)
).pack(anchor="w")

entry_user = tk.Entry(
    frame,
    font=("Arial", 12),
    width=28,
    relief="flat"
)

entry_user.pack(pady=8, ipady=5)

# ---------------- PASSWORD ----------------
tk.Label(
    frame,
    text="Password",
    bg="#111827",
    fg="white",
    font=("Arial", 11)
).pack(anchor="w")

entry_pass = tk.Entry(
    frame,
    show="*",
    font=("Arial", 12),
    width=28,
    relief="flat"
)

entry_pass.pack(pady=8, ipady=5)

# ---------------- STATUS ----------------
status_label = tk.Label(
    frame,
    text="",
    bg="#111827",
    fg="#ef4444",
    font=("Arial", 10)
)

status_label.pack()

# ---------------- LOGIN BUTTON ----------------
tk.Button(
    frame,
    text="Login",
    bg="#2563eb",
    fg="white",
    font=("Arial", 12, "bold"),
    width=22,
    height=2,
    relief="flat",
    command=login
).pack(pady=20)

login_window.mainloop()