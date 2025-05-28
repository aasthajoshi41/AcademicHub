from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from tkinter import ttk, messagebox
import sqlite3

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1910x1000+0+0")

        self.root.configure(bg="#B0C4DE") 


        side_img = Image.open("C:/Users/sit421/Desktop/STUDENT RESULT MNANAGEMENT/IMAGES/lgg.webp")
        side_img = side_img.resize((630, 630), Image.Resampling.LANCZOS)
        self.side_photo = ImageTk.PhotoImage(side_img)

        side_label = Label(self.root, image=self.side_photo, bg="#FFF5E7")
        side_label.place(x=275, y=180, width=630, height=630)




        # === Variables ===
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_quest = StringVar()
        self.var_answer = StringVar()
        self.var_pass = StringVar()
        self.var_cpass = StringVar()
        self.var_chk = IntVar()

        # === Registration Frame ===
        frame1 = Frame(self.root, bg="#FFFBF6")
        frame1.place(x=905, y=180, width=750, height=630)

        title = Label(frame1, text="REGISTER HERE", font=("Microsoft JhengHei", 23, "bold"),
                      bg="#FFFBF6", fg="#2E2E2E")
        title.place(relx=0.49, y=55, anchor="center")

        # ===== Form Fields (Slightly Lowered) =====
        Label(frame1, text="First Name", font=("Georgia", 13, "bold"), bg="white", fg="#444444").place(x=60, y=115)
        Entry(frame1, textvariable=self.var_fname, font=("Georgia", 15), bg="lightgray").place(x=60, y=155, width=280)

        Label(frame1, text="Last Name", font=("Georgia", 13, "bold"), bg="white", fg="#444444").place(x=415, y=115)
        Entry(frame1, textvariable=self.var_lname, font=("Georgia", 15), bg="lightgray").place(x=415, y=155, width=280)

        Label(frame1, text="Contact No.", font=("Georgia", 13, "bold"), bg="white", fg="#444444").place(x=60, y=200)
        Entry(frame1, textvariable=self.var_contact, font=("Georgia", 15), bg="lightgray").place(x=60, y=235, width=280)

        Label(frame1, text="Email", font=("Georgia", 13, "bold"), bg="white", fg="#444444").place(x=415, y=200)
        Entry(frame1, textvariable=self.var_email, font=("Georgia", 15), bg="lightgray").place(x=415, y=235, width=280)

        Label(frame1, text="Security Question", font=("Georgia", 13, "bold"), bg="white", fg="#444444").place(x=60, y=280)
        cmb_quest = ttk.Combobox(frame1, textvariable=self.var_quest, font=("Georgia", 15), state='readonly', justify=CENTER)
        cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name", "Your Favourite Colour")
        cmb_quest.place(x=60, y=315, width=280)
        cmb_quest.current(0)

        Label(frame1, text="Answer", font=("Georgia", 13, "bold"), 
        bg="white", fg="#444444").place(x=415, y=280)
        Entry(frame1, textvariable=self.var_answer, font=("Georgia", 15), bg="lightgray").place(x=415, y=315, width=280)

        Label(frame1, text="Password", font=("Georgia", 13, "bold"), bg="white", fg="#444444").place(x=60, y=360)
        Entry(frame1, textvariable=self.var_pass, font=("Georgia", 15), bg="lightgray", show="*").place(x=60, y=395, width=280)

        Label(frame1, text="Confirm Password", font=("Georgia", 13, "bold"), bg="white", fg="#444444").place(x=415, y=360)
        Entry(frame1, textvariable=self.var_cpass, font=("Georgia", 15), bg="lightgray", show="*").place(x=415, y=395, width=280)

        Checkbutton(frame1, text="I agree to the Terms & Conditions", variable=self.var_chk,
                    font=("Georgia", 13), bg="white", onvalue=1, offvalue=0).place(x=60, y=440)

        self.btn_reg = Button(frame1, text="Register Now", font=("Georgia", 13, "bold"),
                              bg="green", fg="white", cursor="hand2", command=self.register_data)
        self.btn_reg.place(x=80, y=520, width=250, height=40)

        self.btn_reg.bind("<Enter>", lambda e: self.btn_reg.config(bg="#228B22"))
        self.btn_reg.bind("<Leave>", lambda e: self.btn_reg.config(bg="green"))

        btn_login = Button(frame1, text="Sign In", font=("Georgia", 13, "bold"),
                   bg="#0066CC", fg="white", cursor="hand2", command=self.redirect_to_login)
        btn_login.place(x=430, y=520, width=250, height=40)



    def register_data(self):
        if self.var_fname.get() == "" or self.var_email.get() == "" or self.var_quest.get() == "Select":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
        elif self.var_pass.get() != self.var_cpass.get():
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
        elif self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please agree to terms & conditions", parent=self.root)
        else:
            try:
                con=sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=?", (self.var_email.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "User already exists with this email", parent=self.root)
                else:
                    cur.execute("""INSERT INTO employee (f_name, l_name, contact, email, question, answer, password)VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                        self.var_fname.get(),
                        self.var_lname.get(),
                        self.var_contact.get(),
                        self.var_email.get(),
                        self.var_quest.get(),
                        self.var_answer.get(),
                        self.var_pass.get()
                    ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Registration successful!", parent=self.root)

            except Exception as e:
                messagebox.showerror("Error", f"Database Error: {str(e)}", parent=self.root)

    def redirect_to_login(self):
        self.root.destroy()  # Close current window
        import subprocess
        subprocess.Popen(["python", "login.py"])


# ==== Run Program ====
if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()
