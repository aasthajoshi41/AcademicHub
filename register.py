from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from tkinter import ttk, messagebox
import sqlite3

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1910x1000+0+0")

        # === Background ===
        self.bg_img = Image.open("IMAGES/bgfull.png")
        self.bg_img = self.bg_img.resize((1910, 1000), Image.Resampling.LANCZOS)
        self.bg_img = self.bg_img.filter(ImageFilter.GaussianBlur(radius=5))
        self.bg = ImageTk.PhotoImage(self.bg_img)
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

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
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=550, y=180, width=800, height=650)

        title = Label(frame1, text="REGISTER HERE", font=("times new roman", 25, "bold"),
                      bg="white", fg="green")
        title.place(relx=0.5, y=40, anchor="center")

        # ===== Form Fields (Slightly Lowered) =====
        Label(frame1, text="First Name", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=100)
        Entry(frame1, textvariable=self.var_fname, font=("times new roman", 15), bg="lightgray").place(x=50, y=130, width=280)

        Label(frame1, text="Last Name", font=("times new roman", 15, "bold"), bg="white").place(x=420, y=100)
        Entry(frame1, textvariable=self.var_lname, font=("times new roman", 15), bg="lightgray").place(x=420, y=130, width=280)

        Label(frame1, text="Contact No.", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=170)
        Entry(frame1, textvariable=self.var_contact, font=("times new roman", 15), bg="lightgray").place(x=50, y=200, width=280)

        Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white").place(x=420, y=170)
        Entry(frame1, textvariable=self.var_email, font=("times new roman", 15), bg="lightgray").place(x=420, y=200, width=280)

        Label(frame1, text="Security Question", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=240)
        cmb_quest = ttk.Combobox(frame1, textvariable=self.var_quest, font=("times new roman", 13), state='readonly', justify=CENTER)
        cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name", "Your Favourite Colour")
        cmb_quest.place(x=50, y=270, width=280)
        cmb_quest.current(0)

        Label(frame1, text="Answer", font=("times new roman", 15, "bold"), bg="white").place(x=420, y=240)
        Entry(frame1, textvariable=self.var_answer, font=("times new roman", 15), bg="lightgray").place(x=420, y=270, width=280)

        Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=310)
        Entry(frame1, textvariable=self.var_pass, font=("times new roman", 15), bg="lightgray", show="*").place(x=50, y=340, width=280)

        Label(frame1, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white").place(x=420, y=310)
        Entry(frame1, textvariable=self.var_cpass, font=("times new roman", 15), bg="lightgray", show="*").place(x=420, y=340, width=280)

        Checkbutton(frame1, text="I agree to the Terms & Conditions", variable=self.var_chk,
                    font=("times new roman", 13), bg="white", onvalue=1, offvalue=0).place(x=50, y=390)

        self.btn_reg = Button(frame1, text="Register Now", font=("times new roman", 15, "bold"),
                              bg="green", fg="white", cursor="hand2", command=self.register_data)
        self.btn_reg.place(x=50, y=450, width=250, height=40)

        self.btn_reg.bind("<Enter>", lambda e: self.btn_reg.config(bg="#228B22"))
        self.btn_reg.bind("<Leave>", lambda e: self.btn_reg.config(bg="green"))

        btn_login = Button(frame1, text="Sign In", font=("times new roman", 15, "bold"),
                   bg="#0066CC", fg="white", cursor="hand2", command=self.redirect_to_login)
        btn_login.place(x=420, y=450, width=250, height=40)



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
