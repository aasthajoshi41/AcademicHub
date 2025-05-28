from tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageDraw
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import sys


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Window")
        self.root.geometry("1910x1000+0+0")

        self.root.configure(bg="#FFF5E7") 

        

        # === Variables ===
        self.var_email = StringVar()
        self.var_password = StringVar()

        # === welcome text ===
        #welcome_text = Label(self.root, text="Welcome to AcademicHub", font=("Helvetica", 38, "bold"), 
                   #          bg="#FFF5E7", fg="#333")
        #welcome_text.place(x=920, y=180, anchor="center")

        
        
        side_img = Image.open("C:/Users/sit421/Desktop/STUDENT RESULT MNANAGEMENT/IMAGES/login2-modified.png")
        side_img = side_img.resize((630, 630), Image.Resampling.LANCZOS)
        self.side_photo = ImageTk.PhotoImage(side_img)

        side_label = Label(self.root, image=self.side_photo, bg="#FFF5E7")
        side_label.place(x=300, y=180, width=630, height=630)





        # === Login Frame ===
        login_frame = Frame(self.root, bg="#FFFBF6")
        login_frame.place(x=890, y=180, width=600, height=630)



        WEL_title = Label(login_frame, text="WELCOME  TO  ACADEMICHUB", font=("Microsoft JhengHei", 23, "bold"),
                      bg="#FFFBF6", fg="#2E2E2E")
        WEL_title.place(relx=0.5, y=60, anchor="center")



        img = Image.open("C:/Users/sit421/Desktop/STUDENT RESULT MNANAGEMENT/IMAGES/Navy Graduation Logo with Book.png")
        img = img.resize((160, 160), Image.Resampling.LANCZOS)  # Resize to fit frame
        self.login_img = ImageTk.PhotoImage(img)

        Label(login_frame, image=self.login_img, bg="#FFFBF6").place(relx=0.5, y=170, anchor="center")



        title = Label(login_frame, text=" Login Panel", font=("Microsoft JhengHei", 26, "bold"),
                      bg="#FFFBF6", fg="BLACK")
        title.place(relx=0.5, y=250, anchor="center")



        # ==== Email Field ====
        Label(login_frame, text="Email", font=("Georgia", 15, "bold"), bg="#FFFBF6", fg="#444444").place(x=65, y=310)
        self.email_entry = Entry(login_frame, textvariable=self.var_email, font=("Georgia ", 15),
                                 bg="lightgray")
        self.email_entry.place(x=60, y=350, width=400)

        # ==== Password Field ====
        Label(login_frame, text="Password", font=("Georgia", 15, "bold"), bg="#FFFBF6",fg="#444444").place(x=65, y=390)
        self.password_entry = Entry(login_frame, textvariable=self.var_password, font=("Georgia", 15),
                                    bg="lightgray", show="*")
        self.password_entry.place(x=60, y=430, width=400)

        # ==== Login Button ====
        self.btn_login = Button(login_frame, text="Login", font=("Georgia", 14, "bold"),
                        bg="#0056B3", fg="white", cursor="hand2", command=self.login_user)
        self.btn_login.place(x=60, y=490, width=150, height=40)

        self.btn_login.bind("<Enter>", lambda e: self.btn_login.config(bg="#004C99"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.config(bg="#0066CC"))

        # ==== Register Redirect Button ====
        self.register_label = Label(login_frame, text="Register New Account?", font=("Georgia", 13, "underline"),
                            fg="#0056B3", bg="#FFFBF6", cursor="hand2")
        self.register_label.place(x=60, y=550)
        self.register_label.bind("<Button-1>", lambda e: self.open_register())





    def login_user(self):
        if self.var_email.get() == "" or self.var_password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=? AND password=?", (
                    self.var_email.get(), self.var_password.get()
                ))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid username or password", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Login successful!", parent=self.root)
                    self.root.destroy()

                    # ✅ Pass user ID (eid) to dashboard.py
                    subprocess.Popen([sys.executable, "dashboard.py", str(row[0])])  # row[0] = eid

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

        Label(self.forget_win, text="Forget Password", font=("Georgia", 20, "bold"), bg="white", fg="red").place(x=0, y=20, relwidth=1)

        Label(self.forget_win, text="Security Question", font=("Georgia", 15), bg="white").place(x=50, y=100)
        self.var_secq = StringVar()
        cmb_quest = ttk.Combobox(self.forget_win, textvariable=self.var_secq, font=("Georgia", 13), state='readonly', justify=CENTER)
        cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name", "Your Favourite Colour")
        cmb_quest.place(x=50, y=130, width=300)
        cmb_quest.current(0)

        Label(self.forget_win, text="Answer", font=("Georgia", 15), bg="white").place(x=50, y=170)
        self.var_secans = StringVar()
        Entry(self.forget_win, textvariable=self.var_secans, font=("Georgia", 15), bg="lightgray").place(x=50, y=200, width=300)

        Label(self.forget_win, text="New Password", font=("Georgia", 15), bg="white").place(x=50, y=240)
        self.var_newpass = StringVar()
        Entry(self.forget_win, textvariable=self.var_newpass, font=("Georgia", 15), bg="lightgray", show="*").place(x=50, y=270, width=300)

        Button(self.forget_win, text="Reset Password", font=("Georgia", 15, "bold"),
            bg="green", fg="white", cursor="hand2", command=self.reset).place(x=100, y=320)



# ==== Run Program ====
if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
