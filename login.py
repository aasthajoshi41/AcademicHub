from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import sys


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Window")
        self.root.geometry("1910x1000+0+0")

        # === Background ===
        self.bg_img = Image.open("IMAGES/bgfull.png")
        self.bg_img = self.bg_img.resize((1910, 1000), Image.Resampling.LANCZOS)
        self.bg_img = self.bg_img.filter(ImageFilter.GaussianBlur(radius=5))
        self.bg = ImageTk.PhotoImage(self.bg_img)
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # === Variables ===
        self.var_email = StringVar()
        self.var_password = StringVar()

        # === Login Frame ===
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=650, y=250, width=600, height=400)

        title = Label(login_frame, text="SIGN IN", font=("times new roman", 25, "bold"),
                      bg="white", fg="#0066CC")
        title.place(relx=0.5, y=40, anchor="center")

        # ==== Email Field ====
        Label(login_frame, text="Email", font=("times new roman", 15, "bold"), bg="white").place(x=100, y=100)
        self.email_entry = Entry(login_frame, textvariable=self.var_email, font=("times new roman", 15),
                                 bg="lightgray")
        self.email_entry.place(x=100, y=130, width=400)

        # ==== Password Field ====
        Label(login_frame, text="Password", font=("times new roman", 15, "bold"), bg="white").place(x=100, y=180)
        self.password_entry = Entry(login_frame, textvariable=self.var_password, font=("times new roman", 15),
                                    bg="lightgray", show="*")
        self.password_entry.place(x=100, y=210, width=400)

        # ==== Login Button ====
        self.btn_login = Button(login_frame, text="Login", font=("times new roman", 15, "bold"),
                        bg="#0066CC", fg="white", cursor="hand2", command=self.login_user)
        self.btn_login.place(x=100, y=270, width=150, height=40)

        self.btn_login.bind("<Enter>", lambda e: self.btn_login.config(bg="#004C99"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.config(bg="#0066CC"))

        # ==== Register Redirect Button ====
        self.register_label = Label(login_frame, text="Register New Account?", font=("times new roman", 13, "underline"),
                            fg="blue", bg="white", cursor="hand2")
        self.register_label.place(x=100, y=330)
        self.register_label.bind("<Button-1>", lambda e: self.open_register())





    def login_user(self):
        if self.var_email.get() == "" or self.var_password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                # Modified query to match your actual database column names
                cur.execute("SELECT * FROM employee WHERE email=? AND password=?", (
                    self.var_email.get(), self.var_password.get()
                ))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid username or password", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Login successful!", parent=self.root)
                    self.root.destroy()
                    subprocess.Popen([sys.executable, "dashboard.py"])
                con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Database Error: {str(e)}", parent=self.root)

    def reset(self):
        if self.var_secq.get() == "Select":
            messagebox.showerror("Error", "Select security question", parent=self.forget_win)
        elif self.var_secans.get() == "":
            messagebox.showerror("Error", "Please enter answer", parent=self.forget_win)
        elif self.var_newpass.get() == "":
            messagebox.showerror("Error", "Please enter new password", parent=self.forget_win)
        else:
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                # Modified query to match your actual database column names
                cur.execute("SELECT * FROM employee WHERE email=? AND question=? AND answer=?", (
                    self.var_email.get(), self.var_secq.get(), self.var_secans.get()
                ))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Incorrect security question or answer", parent=self.forget_win)
                else:
                    cur.execute("UPDATE employee SET password=? WHERE email=?", (
                        self.var_newpass.get(), self.var_email.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Password reset successfully", parent=self.forget_win)
                    self.forget_win.destroy()
                con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Database Error: {str(e)}", parent=self.forget_win)

    def forget_password(self):
        if self.var_email.get() == "":
            messagebox.showerror("Error", "Please enter the email to reset password", parent=self.root)
        else:
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=?", (self.var_email.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "No user found with this email", parent=self.root)
                else:
                    con.close()
                    self.forget_password_window()
            except Exception as e:
                messagebox.showerror("Error", f"Database Error: {str(e)}", parent=self.root)


        

    def open_register(self):
        self.root.destroy()
        subprocess.Popen([sys.executable, "register.py"])



    def forget_password_window(self):
        self.forget_win = Toplevel(self.root)
        self.forget_win.title("Reset Password")
        self.forget_win.geometry("400x400+600+200")
        self.forget_win.config(bg="white")

        Label(self.forget_win, text="Forget Password", font=("times new roman", 20, "bold"), bg="white", fg="red").place(x=0, y=20, relwidth=1)

        Label(self.forget_win, text="Security Question", font=("times new roman", 15), bg="white").place(x=50, y=100)
        self.var_secq = StringVar()
        cmb_quest = ttk.Combobox(self.forget_win, textvariable=self.var_secq, font=("times new roman", 13), state='readonly', justify=CENTER)
        cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name", "Your Favourite Colour")
        cmb_quest.place(x=50, y=130, width=300)
        cmb_quest.current(0)

        Label(self.forget_win, text="Answer", font=("times new roman", 15), bg="white").place(x=50, y=170)
        self.var_secans = StringVar()
        Entry(self.forget_win, textvariable=self.var_secans, font=("times new roman", 15), bg="lightgray").place(x=50, y=200, width=300)

        Label(self.forget_win, text="New Password", font=("times new roman", 15), bg="white").place(x=50, y=240)
        self.var_newpass = StringVar()
        Entry(self.forget_win, textvariable=self.var_newpass, font=("times new roman", 15), bg="lightgray", show="*").place(x=50, y=270, width=300)

        Button(self.forget_win, text="Reset Password", font=("times new roman", 15, "bold"),
            bg="green", fg="white", cursor="hand2", command=self.reset).place(x=100, y=320)



# ==== Run Program ====
if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
