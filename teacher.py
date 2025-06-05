from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class TeacherClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1300x600+300+300")  # Slightly taller for new fields
        self.root.config(bg="white")
        self.root.focus_force()

        # ===title=====
        title = Label(self.root, text="Manage Teacher Details", font=("Georgia", 18, "bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=1280, height=35)

        # ===variables=====
        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        # self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_department = StringVar()
        #self.var_join_date = StringVar()
        self.var_qualification = StringVar()
        self.var_experience = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        #self.var_pin = StringVar()

        # ===widgets=====
        # ==col1======
        Label(self.root, text="Teacher ID", font=("Georgia", 13, "bold"), bg="white").place(x=10, y=60)
        Label(self.root, text="Name", font=("Georgia", 13, "bold"), bg="white").place(x=10, y=100)
        Label(self.root, text="Email", font=("Georgia", 13, "bold"), bg="white").place(x=10, y=140)
        Label(self.root, text="Gender", font=("Georgia", 13, "bold"), bg="white").place(x=10, y=180)

        Label(self.root, text="State", font=("Georgia", 13, "bold"), bg="white").place(x=10, y=220)
        Entry(self.root, textvariable=self.var_state, font=("Georgia", 13, "bold"), bg="lightyellow").place(x=150, y=225, width=150)

        Label(self.root, text="City", font=("Georgia", 13, "bold"), bg="white").place(x=360, y=220)
        Entry(self.root, textvariable=self.var_city, font=("Georgia", 13, "bold"), bg="lightyellow").place(x=540, y=225, width=100)

        # Label(self.root, text="Pincode", font=("Georgia", 13, "bold"), bg="white").place(x=490, y=220)
        # Entry(self.root, textvariable=self.var_pin, font=("Georgia", 13, "bold"), bg="lightyellow").place(x=570, y=225, width=110)

        Label(self.root, text="Address", font=("Georgia", 13, "bold"), bg="white").place(x=10, y=260)

        # Entry Fields
        self.txt_id = Entry(self.root, textvariable=self.var_id, font=("Georgia", 13, "bold"), bg="lightyellow")
        self.txt_id.place(x=150, y=60, width=200)
        Entry(self.root, textvariable=self.var_name, font=("Georgia", 13, "bold"), bg="lightyellow").place(x=150, y=100, width=200)
        Entry(self.root, textvariable=self.var_email, font=("Georgia", 13, "bold"), bg="lightyellow").place(x=150, y=140, width=200)
        self.txt_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), font=("Georgia", 13, "bold"), state='readonly', justify=CENTER)
        self.txt_gender.place(x=150, y=180, width=200)
        self.txt_gender.current(0)

        # ==col2====
        #Label(self.root, text="D.O.B", font=("Georgia", 15, "bold"), bg="white").place(x=360, y=60)
        Label(self.root, text="Contact", font=("Georgia", 13, "bold"), bg="white").place(x=360, y=140)
        # Label(self.root, text="Join Date", font=("Georgia", 15, "bold"), bg="white").place(x=360, y=140)
        lbl_course = Label(self.root, text="Course", font=("Georgia", 13, "bold"), bg="white")
        lbl_course.place(x=360, y=180)

        self.var_course = StringVar()
        self.cmb_course = ttk.Combobox(self.root, textvariable=self.var_course, state="readonly", justify=CENTER, font=("Georgia", 13, "bold"))
        self.cmb_course.place(x=540, y=180, width=180)
        self.fetch_courses()

        #Entry(self.root, textvariable=self.var_dob, font=("Georgia", 15, "bold"), bg="lightyellow").place(x=480, y=60, width=200)
        Entry(self.root, textvariable=self.var_contact, font=("Georgia", 13, "bold"), bg="lightyellow").place(x=540, y=140, width=180)
        #Entry(self.root, textvariable=self.var_join_date, font=("Georgia", 15, "bold"), bg="lightyellow").place(x=480, y=140, width=200)
        # self.txt_department = ttk.Combobox(self.root, textvariable=self.var_department, values=self.var_department, font=("Georgia", 15, "bold"), state='readonly', justify=CENTER)
        # self.txt_department.place(x=480, y=180, width=200)
        # self.txt_department.set("Select")

        # ==col3 new fields==
        Label(self.root, text="Qualification", font=("Georgia", 13, "bold"), bg="white").place(x=360, y=60)
        Label(self.root, text="Experience (Years)", font=("Georgia", 13, "bold"), bg="white").place(x=360, y=100)

        Entry(self.root, textvariable=self.var_qualification, font=("Georgia", 13, "bold"), bg="lightyellow").place(x=540, y=60, width=180)
        Entry(self.root, textvariable=self.var_experience, font=("Georgia", 13, "bold"), bg="lightyellow").place(x=540, y=100, width=180)
        # ===text address=====
        self.txt_address = Text(self.root, font=("Georgia", 13, "bold"), bg="lightyellow")
        self.txt_address.place(x=150, y=280, width=540, height=130)

        # ===Buttons=====
        Button(self.root, text="Save", font=("Georgia", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add).place(x=150, y=450, width=110, height=40)
        Button(self.root, text="Update", font=("Georgia", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update).place(x=270, y=450, width=110, height=40)
        Button(self.root, text="Delete", font=("Georgia", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete).place(x=390, y=450, width=110, height=40)
        Button(self.root, text="Clear", font=("Georgia", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear).place(x=510, y=450, width=110, height=40)

        # ===search panel=====
        self.var_search = StringVar()
        Label(self.root, text="Teacher ID", font=("Georgia", 15, "bold"), bg="white").place(x=770, y=70)
        Entry(self.root, textvariable=self.var_search, font=("Georgia", 15, "bold"), bg="lightyellow").place(x=900, y=70, width=180)
        Button(self.root, text="Search", font=("Georgia", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=1090, y=70, width=120, height=28)

        # ===Teacher details panel=====
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=770, y=120, width=470, height=350)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.TeacherTable = ttk.Treeview(self.C_Frame, columns=(
            "id", "name", "email", "gender", "contact", "qualification",
            "experience", "state", "city", "address","course"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
            show='headings'  # Hide first empty column
        )

        # Attach scrollbars to Treeview
        scrolly.config(command=self.TeacherTable.yview)
        scrollx.config(command=self.TeacherTable.xview)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        # Set headings
        self.TeacherTable.heading("id", text="Teacher ID")
        self.TeacherTable.heading("name", text="Name")
        self.TeacherTable.heading("email", text="Email")
        self.TeacherTable.heading("gender", text="Gender")
        self.TeacherTable.heading("contact", text="Contact")
        self.TeacherTable.heading("qualification", text="Qualification")
        self.TeacherTable.heading("experience", text="Experience")
        self.TeacherTable.heading("state", text="State")
        self.TeacherTable.heading("city", text="City")
        self.TeacherTable.heading("address", text="Address")
        self.TeacherTable.heading("course", text="Course")

        # Set column widths
        self.TeacherTable.column("id", width=100, anchor=CENTER)
        self.TeacherTable.column("name", width=150)
        self.TeacherTable.column("email", width=150)
        self.TeacherTable.column("gender", width=100, anchor=CENTER)
        self.TeacherTable.column("contact", width=120)
        self.TeacherTable.column("qualification", width=120)
        self.TeacherTable.column("experience", width=100, anchor=CENTER)
        self.TeacherTable.column("state", width=100)
        self.TeacherTable.column("city", width=100)
        self.TeacherTable.column("address", width=200)
        self.TeacherTable.column("course", width=120)

        self.TeacherTable.pack(fill=BOTH, expand=1)
        self.TeacherTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()


    def fetch_courses(self):
        try:
            con = sqlite3.connect("rms.db")  # Use your database name
            cur = con.cursor()

            # Fetch all courses from the course table
            cur.execute("SELECT name FROM course")
            all_courses = [row[0] for row in cur.fetchall()]

            # Fetch already assigned courses from the teacher table
            cur.execute("SELECT course FROM teacher")
            assigned_courses = [row[0] for row in cur.fetchall() if row[0] is not None]

            # Filter out assigned courses
            unassigned_courses = [course for course in all_courses if course not in assigned_courses]

            self.cmb_course['values'] = unassigned_courses
            self.cmb_course.set("Select")
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")



    def fetch_data(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM teacher")
            rows = cur.fetchall()
            self.TeacherTable.delete(*self.TeacherTable.get_children())
            for row in rows:
                self.TeacherTable.insert('', 'end', values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"FETCH_DATA ERROR:\n{str(ex)}")
        finally:
            con.close()



    def search(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM teacher WHERE id=?", (self.var_search.get(),))
            row = cur.fetchone()
            if row:
                self.TeacherTable.delete(*self.TeacherTable.get_children())
                self.TeacherTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)


    def add(self):
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Teacher ID is required", parent=self.root)
                return
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Teacher Name is required", parent=self.root)
                return
            if self.var_email.get() == "":
                messagebox.showerror("Error", "Email is required", parent=self.root)
                return
            if self.var_contact.get() == "":
                messagebox.showerror("Error", "Contact number is required", parent=self.root)
                return

            address = self.txt_address.get("1.0", END).strip()
            #print(f"Address: {repr(address)}")  # For debugging
            
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()

            # Optional: Check if teacher with same ID exists
            cur.execute("SELECT * FROM teacher WHERE id = ?", (self.var_id.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "This Teacher ID already exists", parent=self.root)
                return

            cur.execute(
                "INSERT INTO teacher (id, name, email, gender, contact, qualification, experience, state, city, address, course) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.var_id.get(),
                    self.var_name.get(),
                    self.var_email.get(),
                    self.var_gender.get(),
                    self.var_contact.get(),
                    self.var_qualification.get(),
                    self.var_experience.get(),
                    self.var_state.get(),
                    self.var_city.get(),
                    self.txt_address.get("1.0", END).strip(),
                    self.var_course.get()
                )
            )
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Teacher added successfully", parent=self.root)
            self.fetch_data()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)



    def show(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM teacher")
            rows = cur.fetchall()
            self.TeacherTable.delete(*self.TeacherTable.get_children())
            for row in rows:
                self.TeacherTable.insert('', END, values=row)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self, ev):
            f = self.TeacherTable.focus()
            content = self.TeacherTable.item(f)
            row = content["values"]

            # Set values in the entry fields correctly
            self.var_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_qualification.set(row[4])
            self.var_experience.set(row[5])
            self.var_contact.set(row[6])
            self.var_state.set(row[7])
            self.var_city.set(row[8])
            self.txt_address.delete("1.0",END)
            self.txt_address.insert(END, row[9])
            self.var_course.set(row[10])

    def update(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Teacher ID is required", parent=self.root)
                return
            cur.execute("SELECT * FROM teacher WHERE id=?", (self.var_id.get(),))
            row = cur.fetchone()
            if not row:
                messagebox.showerror("Error", "Invalid Teacher ID", parent=self.root)
            else:
                cur.execute("""UPDATE teacher SET name=?, email=?, gender=?, contact=?, 
                            qualification=?, experience=?, state=?, city=?,  address=? WHERE id=?""", (
                    self.var_name.get(),
                    self.var_email.get(),
                    self.var_gender.get(),
                    self.var_contact.get(),
                    self.var_qualification.get(),
                    self.var_experience.get(),
                    self.var_state.get(),
                    self.var_city.get(),
                    self.txt_address.get("1.0", END).strip(),
                    self.var_id.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Teacher record updated", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Teacher ID is required", parent=self.root)
                return
            cur.execute("SELECT * FROM teacher WHERE id=?", (self.var_id.get(),))
            row = cur.fetchone()
            if not row:
                messagebox.showerror("Error", "Invalid Teacher ID", parent=self.root)
            else:
                confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete?", parent=self.root)
                if confirm:
                    cur.execute("DELETE FROM teacher WHERE id=?", (self.var_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Deleted successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_course.set("Select")  # REMOVE course clear
        self.var_qualification.set("")
        self.var_experience.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.txt_address.delete('1.0', END)


    def assign_course_to_teacher(self, teacher_id, course_id):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("INSERT INTO teacher_course (teacher_id, course_id) VALUES (?, ?)", (teacher_id, course_id))
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error in assigning course: {str(ex)}", parent=self.root)
        finally:
            con.close()

    
if __name__ == "__main__":
    root = Tk()
    obj = TeacherClass(root)
    root.mainloop()
