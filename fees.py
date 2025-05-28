from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime



class FeesClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Fee Management")
        self.root.geometry("1300x550+300+300")
        self.root.config(bg="white")
        self.root.focus_force()
   
        self.var_roll = StringVar()       # Student roll (student_id)
        self.var_course_name = StringVar()  # Course name (for display only)
        self.var_course_id = None         # Will store course_id internally
        self.var_total = StringVar()
        self.var_paid = StringVar()
        self.var_pending = StringVar()
        self.var_payment = StringVar()

        title = Label(self.root, text="Fee Management System", font=("times new roman", 20), bg="#033054", fg="white").place(x=10, y=10, relwidth=1)

        lbl_roll = Label(self.root, text="Select Roll No", font=("times new roman", 15), bg="white").place(x=50, y=80)
        self.roll_cb = ttk.Combobox(self.root, textvariable=self.var_roll, font=("times new roman", 15), state='readonly')
        self.roll_cb.place(x=200, y=80, width=200)
        self.roll_cb.bind("<<ComboboxSelected>>", self.fetch_student_details)

        lbl_course = Label(self.root, text="Course", font=("times new roman", 15), bg="white").place(x=50, y=130)
        self.txt_course = Entry(self.root, textvariable=self.var_course_name, font=("times new roman", 15), state="readonly", bg="lightyellow")
        self.txt_course.place(x=200, y=130, width=200)

        lbl_total = Label(self.root, text="Total Fees", font=("times new roman", 15), bg="white").place(x=50, y=180)
        self.txt_total = Entry(self.root, textvariable=self.var_total, font=("times new roman", 15), state="readonly", bg="lightyellow")
        self.txt_total.place(x=200, y=180, width=200)

        lbl_paid = Label(self.root, text="Paid", font=("times new roman", 15), bg="white").place(x=50, y=230)
        self.txt_paid = Entry(self.root, textvariable=self.var_paid, font=("times new roman", 15), bg="lightyellow")
        self.txt_paid.place(x=200, y=230, width=200)


        lbl_pending = Label(self.root, text="Pending", font=("times new roman", 15), bg="white").place(x=50, y=280)
        self.txt_pending = Entry(self.root, textvariable=self.var_pending, font=("times new roman", 15), bg="lightyellow", state="readonly")
        self.txt_pending.place(x=200, y=280, width=200)

        # lbl_pay = Label(self.root, text="Pay Now (₹)", font=("times new roman", 15), bg="white").place(x=50, y=330)
        # self.txt_pay = Entry(self.root, textvariable=self.var_payment, font=("times new roman", 15), bg="lightyellow")
        # self.txt_pay.place(x=200, y=330, width=200)

        btn_update = Button(self.root, text="Update Payment", command=self.update_payment, font=("times new roman", 15), bg="#4caf50", fg="white")
        btn_update.place(x=150, y=380, width=200)

        # === TreeView ===
        self.fee_table = ttk.Treeview(self.root, columns=("id", "student_id", "course_id", "total_fees", "paid_amount", "date_paid", "status"), show='headings')
        self.fee_table.place(x=450, y=80, width=800, height=400)


        # Vertical Scrollbar
        vsb = Scrollbar(self.root, orient="vertical", command=self.fee_table.yview)
        vsb.place(x=1250, y=80, height=400)  # Adjust x,y and height as per your layout

        # Horizontal Scrollbar
        hsb = Scrollbar(self.root, orient="horizontal", command=self.fee_table.xview)
        hsb.place(x=450, y=480, width=800)  # Adjust x,y and width as per your layout

        # Attach scrollbars to Treeview
        self.fee_table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Place Treeview
        self.fee_table.place(x=450, y=80, width=800, height=400)




        for col in self.fee_table["columns"]:
            self.fee_table.heading(col, text=col.capitalize())

        self.load_roll_numbers()
        self.show_records()

    def connect(self):
        return sqlite3.connect("rms.db")

    def load_roll_numbers(self):
        con = self.connect()
        cur = con.cursor()
        cur.execute("SELECT roll FROM student")
        rolls = [row[0] for row in cur.fetchall()]
        self.roll_cb['values'] = rolls
        con.close()

    def fetch_student_details(self, event=None):
        con = self.connect()
        cur = con.cursor()
        roll = self.var_roll.get()

        # Get course info for the student
        cur.execute("SELECT course FROM student WHERE roll=?", (roll,))
        data = cur.fetchone()
        if data:
            course_name = data[0]
            self.var_course_name.set(course_name)

            cur.execute("SELECT cid, charges FROM course WHERE name=?", (course_name,))
            course_data = cur.fetchone()
            if course_data:
                course_id, total_fees = course_data
                self.var_total.set(total_fees)
                self.var_course_id = course_id
            else:
                self.var_total.set("")
                self.var_course_id = None
        else:
            self.var_course_name.set("")
            self.var_total.set("")
            self.var_course_id = None

        # Reset paid and pending to blank so user can input manually
        self.var_paid.set("")
        self.var_pending.set("")
        con.close()

    def update_payment(self):
        print("update_payment called")
        try:
            roll = self.var_roll.get()
            course_id = self.var_course_id
            total = int(self.var_total.get())
            
            paid_str = self.var_paid.get()
            if not paid_str.isdigit():
                print("Invalid paid amount entered")
                messagebox.showerror("Error", "Please enter a valid paid amount")
                print("Returning after invalid paid amount")
                return  # <--- Should keep window open
            
            paid = int(paid_str)
            
            if paid > total:
                print("Paid amount greater than total")
                messagebox.showerror("Error", "Paid amount cannot be greater than total fees")
                print("Returning after paid > total")
                return  # <--- Should keep window open
            
            con = self.connect()
            cur = con.cursor()

            # Check existing fee record
            cur.execute("SELECT paid_amount, status FROM fees WHERE student_id=? AND course_id=?", (roll, course_id))
            existing = cur.fetchone()

            if existing:
                existing_paid, existing_status = existing
                print(f"Existing payment: {existing_paid}, status: {existing_status}")

                if existing_status == "Paid":
                    print("Fees already fully paid")
                    messagebox.showinfo("Info", "Fees already fully paid.")
                    print("Returning after fees fully paid")
                    con.close()
                    return  # <--- Should keep window open
                
                # Normal update path
                pending = total - paid
                self.var_pending.set(str(pending))
                status = "Paid" if pending == 0 else "Pending"
                date_paid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cur.execute("""
                    UPDATE fees SET paid_amount=?, status=?, date_paid=?
                    WHERE student_id=? AND course_id=?
                """, (paid, status, date_paid, roll, course_id))
            else:
                # Insert new record
                pending = total - paid
                self.var_pending.set(str(pending))
                status = "Paid" if pending == 0 else "Pending"
                date_paid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cur.execute("""
                    INSERT INTO fees (student_id, course_id, total_fees, paid_amount, date_paid, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (roll, course_id, total, paid, date_paid, status))

            con.commit()
            print("Payment updated successfully")
            messagebox.showinfo("Success", "Payment updated successfully")
            con.close()
            self.show_records()  # Refresh table
            print("Returning normally from update_payment")

        except Exception as e:
            print(f"Exception in update_payment: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
            # Do NOT close or quit the window here






    def show_records(self):
        con = self.connect()
        cur = con.cursor()
        cur.execute("SELECT * FROM fees")
        rows = cur.fetchall()
        self.fee_table.delete(*self.fee_table.get_children())  # Clear existing table rows
        for row in rows:
            self.fee_table.insert('', END, values=row)         # Insert updated rows
        con.close()

    
 

if __name__ == "__main__":
    root = Tk()
    obj = FeesClass(root)
    root.mainloop()

