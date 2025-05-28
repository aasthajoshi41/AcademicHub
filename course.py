from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import login

class CourseClass:
    def __init__(self, root, refresh_callback=None):
        self.root = root
        self.refresh_callback = refresh_callback  # Store callback
        self.root.title("Student Result Management System")
        self.root.geometry("1300x550+300+300")
        self.root.config(bg="white")
        self.root.focus_force()

        # ===title=====
        title = Label(self.root, text="Manage Course Details",font=("times new roman", 18, "bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=1280, height=35)

        # ===variables=====
        self.var_course=StringVar()
        self.var_duration=StringVar()
        self.var_charges=StringVar()


        # ===widgets=====
        lbl_courseName=Label(self.root, text="Course Name",font=("times new roman", 15, "bold"),bg="white").place(x=10,y=60)
        #lbl_duration=Label(self.root, text="Duration",font=("times new roman", 15, "bold"),bg="white").place(x=10,y=100)
        lbl_charges=Label(self.root, text="Charges",font=("times new roman", 15, "bold"),bg="white").place(x=10,y=140)
        lbl_description=Label(self.root, text="Description",font=("times new roman", 15, "bold"),bg="white").place(x=10,y=180)

        # ===Entry Fields=====
        self.txt_courseName=Entry(self.root,textvariable=self.var_course,font=("times new roman", 15, "bold"),bg="lightyellow")
        self.txt_courseName.place(x=150,y=60,width=230)
        
        
            # Duration Label
        lbl_duration = Label(self.root, text="Duration", font=("times new roman", 15, "bold"), bg="white")
        lbl_duration.place(x=10, y=100)

        # Duration Entry with placeholder
        self.txt_duration = Entry(self.root, textvariable=self.var_duration, font=("times new roman", 15, "bold"), fg='grey', bg='lightyellow')
        self.txt_duration.place(x=150, y=100, width=230)
        self.txt_duration.insert(0, "Enter duration in months")
        self.txt_duration.bind("<FocusIn>", self.clear_placeholder)
        self.txt_duration.bind("<FocusOut>", self.add_placeholder)


    
        
        txt_charges=Entry(self.root,textvariable=self.var_charges,font=("times new roman", 15, "bold"),bg="lightyellow").place(x=150,y=140,width=230)   
        self.txt_description=Text(self.root,font=("times new roman", 15, "bold"),bg="lightyellow")
        self.txt_description.place(x=150,y=180,width=500,height=160)

        # ===Buttons=====
        self.btn_add=Button(self.root, text="Save", font=("times new roman", 15, "bold"),bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=150, y=400, width=110, height=40)

        self.btn_update=Button(self.root, text="Update", font=("times new roman", 15, "bold"),bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=400, width=110, height=40)

        self.btn_delete=Button(self.root, text="Delete", font=("times new roman", 15, "bold"),bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=400, width=110, height=40)

        self.btn_clear=Button(self.root, text="Clear", font=("times new roman", 15, "bold"),bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=510, y=400, width=110, height=40)

        # ===search panel=====
        self.var_search=StringVar()
        lbl_search_courseName=Label(self.root, text="Course Name",font=("times new roman", 15, "bold"),bg="white").place(x=770,y=60)
        txt_search_courseName=Entry(self.root,textvariable=self.var_search,font=("times new roman", 15, "bold"),bg="lightyellow").place(x=900,y=60,width=180)
        btn_search=Button(self.root, text="Search", font=("times new roman", 15, "bold"),bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=1090, y=60, width=120, height=28)

        # ===search panel=====
        self.C_Frame=Frame(self.root,bd=2,relief=RIDGE)
        self.C_Frame.place(x=770,y=100,width=470,height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"),
                               xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        # Position Treeview and scrollbars using grid for proper alignment
        self.CourseTable.grid(row=0, column=0, sticky='nsew')
        scrollx.grid(row=1, column=0, sticky='ew')
        scrolly.grid(row=0, column=1, sticky='ns')

        # Configure grid weights so Treeview expands
        self.C_Frame.grid_rowconfigure(0, weight=1)
        self.C_Frame.grid_columnconfigure(0, weight=1)

        # Setup scrollbar commands
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

     
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = 'headings'

        self.CourseTable.heading("cid", text="ID")
        self.CourseTable.column("cid", width=50)

       
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)

        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()



#================================

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', END)
        self.txt_courseName.config(state=NORMAL)


    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                # Check if course exists
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please select a valid course from the list", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete this course?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM course WHERE name=?", (self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Course deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)



    def get_data(self, ev):
        self.txt_courseName.config(state='readonly')
        #self.txt_courseName
        r=self.CourseTable.focus()
        content=self.CourseTable.item(r)
        row=content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete('1.0', END)
        self.txt_description.insert(END, row[4])


    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                # Check if the course name already exists
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Course Name already exists", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO course(name, duration, charges, description) VALUES (?, ?, ?, ?)", (
                            self.var_course.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get("1.0", END).strip()
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                    self.show()

                    # Refresh the dashboard chart if a callback is provided
                    if self.refresh_callback:
                        self.refresh_callback()

                    # Close the add course window
                    self.root.destroy()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)





    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                # Check if the course exists
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select Course from the list", parent=self.root)
                else:
                    cur.execute(
                        "UPDATE course SET duration=?, charges=?, description=? WHERE name=?",
                        (
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get("1.0", END).strip(),
                            self.var_course.get()
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)


            



    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course WHERE name LIKE ?", (f'%{self.var_search.get()}%',))
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")




    def clear_placeholder(self, event):
        if self.txt_duration.get() == "Enter duration in months":
            self.txt_duration.delete(0, END)
            self.txt_duration.config(fg='black')

    def add_placeholder(self, event):
        if not self.txt_duration.get():
            self.txt_duration.insert(0, "Enter duration in months")
            self.txt_duration.config(fg='grey')

if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()

