from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class SubjectsClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Subjects")
        self.root.geometry("1300x550+300+300")
        self.root.config(bg="white")
        self.root.focus_force()

        # === Title ===
        title = Label(self.root, text="Manage Subject Details", font=("times new roman", 18, "bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=1280, height=35)

        # === Variables ===
        self.var_subject_id = StringVar()
        self.var_name = StringVar()
        self.var_time = StringVar()
        self.var_topics = StringVar()
        self.var_search = StringVar()

        # === Widgets ===
        Label(self.root, text="Course Name", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=70)
        Label(self.root, text="Time", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=110)
        Label(self.root, text="Topics", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=150)

        self.course_name_combobox = ttk.Combobox(self.root, textvariable=self.var_name, font=("times new roman", 15), state="readonly")
        self.course_name_combobox['values'] = self.get_course_names()
        self.course_name_combobox.place(x=150, y=70, width=250)

        # Search Button
        Button(self.root, text="Search", font=("times new roman", 15), fg="#03a9f4", bd=0, cursor="hand2", command=self.search).place(x=410, y=70, width=80, height=30)

        self.txt_time = Entry(self.root, textvariable=self.var_time, font=("times new roman", 15), bg="lightyellow", state="readonly")
        self.txt_time.place(x=150, y=110, width=250)

        self.txt_topics = Entry(self.root, textvariable=self.var_topics, font=("times new roman", 15), bg="lightyellow")
        self.txt_topics.place(x=150, y=150, width=250)

        # ===Buttons=====
        self.btn_add=Button(self.root, text="Save", font=("times new roman", 15, "bold"),bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=150, y=230, width=110, height=40)

        self.btn_update=Button(self.root, text="Update", font=("times new roman", 15, "bold"),bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=230, width=110, height=40)

        self.btn_delete=Button(self.root, text="Delete", font=("times new roman", 15, "bold"),bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=230, width=110, height=40)

        self.btn_clear=Button(self.root, text="Clear", font=("times new roman", 15, "bold"),bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=510, y=230, width=110, height=40)

        # Search Panel
        Label(self.root, text="Search by Course Name", font=("times new roman", 15, "bold"), bg="white").place(x=800, y=60)
        self.txt_search = Entry(self.root, textvariable=self.var_search, font=("times new roman", 15), bg="lightyellow")
        self.txt_search.place(x=1020, y=60, width=180)
        self.txt_search.bind("<KeyRelease>", self.search_table)

        # Table Frame
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=770, y=100, width=520, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.SubjectsTable = ttk.Treeview(self.C_Frame, columns=("id", "name", "time", "topics"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SubjectsTable.xview)
        scrolly.config(command=self.SubjectsTable.yview)

        self.SubjectsTable.heading("id", text="ID")
        self.SubjectsTable.heading("name", text="Course Name")
        self.SubjectsTable.heading("time", text="Time")
        self.SubjectsTable.heading("topics", text="Topics")
        self.SubjectsTable["show"] = "headings"

        self.SubjectsTable.column("id", width=50)
        self.SubjectsTable.column("name", width=150)
        self.SubjectsTable.column("time", width=100)
        self.SubjectsTable.column("topics", width=200)

        self.SubjectsTable.pack(fill=BOTH, expand=1)
        self.SubjectsTable.bind("<ButtonRelease-1>", self.get_data)

        self.show_subjects()

    def get_course_names(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            con.close()
            return [row[0] for row in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
            con.close()
            return []

    def get_course_duration(self, name):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT duration FROM course WHERE name=?", (name,))
            result = cur.fetchone()
            con.close()
            if result:
                return result[0]
            return ""
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
            con.close()
            return ""

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_name.get() == "" or self.var_time.get() == "" or self.var_topics.get() == "":
                messagebox.showerror("Error", "Course Name, Time, and Topics are required", parent=self.root)
            else:
                # Insert with NULL user_id since it's not collected from UI
                cur.execute("INSERT INTO subjects(user_id, name, time, topics) VALUES (?, ?, ?, ?)", (
                    None,  # user_id set to NULL
                    self.var_name.get(),
                    self.var_time.get(),
                    self.var_topics.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Subject added successfully", parent=self.root)
                self.clear()
                self.show_subjects()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show_subjects(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT id, name, time, topics FROM subjects")
            rows = cur.fetchall()
            self.SubjectsTable.delete(*self.SubjectsTable.get_children())
            for row in rows:
                self.SubjectsTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search_table(self, ev):
        """Search functionality for the table"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            search_term = self.var_search.get()
            if search_term == "":
                cur.execute("SELECT id, name, time, topics FROM subjects")
            else:
                cur.execute("SELECT id, name, time, topics FROM subjects WHERE name LIKE ?", (f'%{search_term}%',))
            
            rows = cur.fetchall()
            self.SubjectsTable.delete(*self.SubjectsTable.get_children())
            for row in rows:
                self.SubjectsTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        r = self.SubjectsTable.focus()
        content = self.SubjectsTable.item(r)
        row = content["values"]
        if row:
            # We need to get the full record including ID for operations
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            try:
                cur.execute("SELECT id FROM subjects WHERE name=? AND time=? AND topics=?", 
                           (row[1], row[2], row[3]))  # row[1]=name, row[2]=time, row[3]=topics
                result = cur.fetchone()
                if result:
                    self.var_subject_id.set(result[0])
                    self.var_name.set(row[1])
                    self.var_time.set(row[2])
                    self.var_topics.set(row[3])
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
            finally:
                con.close()

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_subject_id.get() == "":
                messagebox.showerror("Error", "Please select a subject from the list", parent=self.root)
                return
            
            cur.execute("UPDATE subjects SET name=?, time=?, topics=? WHERE id=?", (
                self.var_name.get(),
                self.var_time.get(),
                self.var_topics.get(),
                self.var_subject_id.get()
            ))
            con.commit()
            messagebox.showinfo("Success", "Subject updated successfully", parent=self.root)
            self.clear()
            self.show_subjects()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_subject_id.get() == "":
                messagebox.showerror("Error", "Please select a subject from the list", parent=self.root)
                return
            
            op = messagebox.askyesno("Confirm", "Do you really want to delete this subject?", parent=self.root)
            if op:
                cur.execute("DELETE FROM subjects WHERE id=?", (self.var_subject_id.get(),))
                con.commit()
                messagebox.showinfo("Deleted", "Subject deleted successfully", parent=self.root)
                self.clear()
                self.show_subjects()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_subject_id.set("")
        self.var_name.set("")
        self.var_time.set("")
        self.var_topics.set("")
        self.course_name_combobox.set('')
        self.show_subjects()

    def search(self):
        selected_course = self.var_name.get()
        
        if not selected_course:
            messagebox.showerror("Error", "Please select a course from the dropdown", parent=self.root)
            return

        course_duration = self.get_course_duration(selected_course)

        if course_duration:
            self.var_time.set(course_duration)
            messagebox.showinfo("Info", f"Found course '{selected_course}' with duration '{course_duration}'.", parent=self.root)
        else:
            messagebox.showinfo("Info", "No course found with this name. Please add the course first.", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = SubjectsClass(root)
    root.mainloop()