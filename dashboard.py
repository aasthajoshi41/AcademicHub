from tkinter import *
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from PIL import Image, ImageTk
from course import CourseClass
from student import StudentClass
from result import ResultClass
from report import ReportClass
from subjects import SubjectsClass
from teacher import TeacherClass
from fees import FeesClass
from tkinter import messagebox
import sys
import os

if len(sys.argv) > 1:
    user_id = sys.argv[1]
    print("Logged-in User ID:", user_id)
else:
    user_id = None

class RMS:
    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id
        self.root.title("Student Management System")
        self.root.geometry("1910x1000+0+0")
        self.root.config(bg="#E6F2FF")

        #self.show_course_bar_chart()
        # self.show_student_percentage_pie_chart()

        self.table_frame = Frame(self.root, bg="white")
        self.table_frame.place(x=715, y=250, width=1105, height=530)  # Adjust coordinates and size as needed

        show_table(self.table_frame, user_id)







        side_img = Image.open("C:/Users/sit421/Desktop/STUDENT RESULT MNANAGEMENT/IMAGES/dss.png")
        side_img = side_img.resize((630, 660), Image.Resampling.LANCZOS)
        self.side_photo = ImageTk.PhotoImage(side_img)

        side_label = Label(self.root, image=self.side_photo, bg="#E6F2FF")
        side_label.place(x=80, y=240, width=600, height=650)







        # === Title Bar ===

        title = Label(self.root, text="🎓 Welcome to Student Dashboard", padx=10, font=("Segoe UI", 16, "bold"),bg="#E6F2FF",
                             fg="#004E89")
        title.place(x=90, y=65)

        title = Label(self.root, text="AcademicHub", padx=10, font=("Segoe UI", 20, "bold"),
                      bg="#033054", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)


        # === Menu Frame ===
        self.M_Frame = LabelFrame(self.root, text="Menus", font=("Segoe UI", 15), bg="#E6F2FF")
        self.M_Frame.place(x=100, y=110, width=1715, height=95)

        self.add_menu_buttons()

        # === Summary Boxes ===
        self.lbl_course = Label(self.root, text="📘 Courses Offered\n[ 0 ]", font=("Segoe UI", 17),
                                bd=5, relief=RIDGE, bg="#d84607", fg="white")
        self.lbl_course.place(x=740, y=800, width=250, height=80)

        self.lbl_Student = Label(self.root, text="👤 Total Students\n[ 0 ]", font=("Segoe UI", 17),
                                 bd=5, relief=RIDGE,bg="#d84607", fg="white")
        self.lbl_Student.place(x=1010, y=800, width=250, height=80)

        self.lbl_Result = Label(self.root, text="📊 Total Results\n[ 0 ]", font=("Segoe UI", 17),
                                bd=5, relief=RIDGE, bg="#d84607", fg="white")
        self.lbl_Result.place(x=1280, y=800, width=250, height=80)

        self.lbl_teacher = Label(self.root, text="Total Teachers\n[ 0 ]", font=("Segoe UI", 17),
                                 bd=5, relief=RIDGE, bg="#d84607", fg="white")
        self.lbl_teacher.place(x=1550, y=800, width=250, height=80)

        # Call the method to count totals and update labels
        self.count_totals()

    def count_totals(self):
        try:
            conn = sqlite3.connect("rms.db")  # change DB path if needed
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM course")
            total_courses = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM student")
            total_students = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM result")
            total_results = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM teacher")
            total_teachers = cursor.fetchone()[0]

            # Update the labels
            self.lbl_course.config(text=f"📘 Courses Offered\n[ {total_courses} ]")
            self.lbl_Student.config(text=f"👤 Total Students\n[ {total_students} ]")
            self.lbl_Result.config(text=f"📊 Total Results\n[ {total_results} ]")
            self.lbl_teacher.config(text=f"👨‍🏫 Total Teachers\n[ {total_teachers} ]")

            conn.close()
        except Exception as e:
            print("Error counting totals:", e)



        # === Footer ===
        footer = Label(self.root, text="SRMS v1.0 | AcademicHub | Support: support@academichub.com",
                       font=("Segoe UI", 12), bg="#262626", fg="white")
        footer.pack(side=BOTTOM, fill=X)

        self.theme_buttons_visible = False

        # self.show_course_bar_chart()




        # === Logout | Exit clickable text on top-right ===
        logout_exit_label = Label(self.root, text="Logout   |   Exit", font=("Segoe UI", 15),
                                bg="#033054", fg="white", cursor="hand2")
        logout_exit_label.place(x=1700, y=7)  # Adjust x value as per your screen resolution

        logout_exit_label.bind("<Button-1>", self.handle_logout_exit)











    def add_menu_buttons(self):
        buttons = [
            ("Course", self.add_course),
            ("Student", self.add_student),
            ("Result", self.add_result),
            ("View Student Result", self.add_report),
            ("Subjects", self.add_subjects),
            ("Teachers", self.add_teacher),
            ("Fees", self.add_fees)
        ]
        positions = [50, 280, 510, 740, 970, 1200, 1430]

        for i, (label, cmd) in enumerate(buttons):
            Button(self.M_Frame, text=label, font=("Segoe UI", 13, "bold"),
                   bg="#003366", fg="white", cursor="hand2", command=cmd).place(x=positions[i], y=5, width=220, height=40)


    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win) #refresh_callback=self.show_course_bar_chart)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentClass(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ResultClass(self.new_win)

    def add_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ReportClass(self.new_win)

    def add_teacher(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = TeacherClass(self.new_win)

    def add_fees(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = FeesClass(self.new_win)


    def logout(self):
        if messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root):
            self.root.destroy()
            os.system("python login.py")

    def exit_(self):
        if messagebox.askyesno("Confirm", "Do you really want to exit?", parent=self.root):
            self.root.destroy()

    def handle_logout_exit(self, event):
        click_x = event.x
        if click_x < 50:  # Adjust this threshold based on font and spacing
            self.logout()
        else:
            self.exit_()


    def add_subjects(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SubjectsClass(self.new_win)

    # def show_course_bar_chart(self): 
    #     import matplotlib
    #     matplotlib.use("Agg")

    #     from matplotlib.figure import Figure
    #     from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    #     import sqlite3
    #     from tkinter import Canvas, Frame

    #     # Fetch data from database
    #     con = sqlite3.connect("rms.db")
    #     cur = con.cursor()
    #     cur.execute("SELECT name, duration FROM course")
    #     data = cur.fetchall()
    #     con.close()

    #     if not data:
    #         return

    #     course_names = [row[0] for row in data]
    #     durations = []
    #     for d in data:
    #         try:
    #             durations.append(int(d[1].split()[0]))
    #         except:
    #             durations.append(0)

    #     # Destroy previous chart if it exists
    #     if hasattr(self, 'chart_card_frame'):
    #         self.chart_card_frame.destroy()
    #     if hasattr(self, 'shadow_canvas'):
    #         self.shadow_canvas.destroy()

    #     # # === Rounded shadow frame ===
    #     # self.shadow_canvas = Canvas(self.root, width=750, height=320, bg="white", highlightthickness=0)
    #     # self.shadow_canvas.place(x=230, y=580)

    #     # def create_rounded_rect(canvas, x1, y1, x2, y2, r=25, **kwargs):
    #     #     points = [
    #     #         x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1,
    #     #         x2, y1, x2, y1 + r, x2, y1 + r, x2, y2 - r,
    #     #         x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2,
    #     #         x1 + r, y2, x1 + r, y2, x1, y2, x1, y2 - r,
    #     #         x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1
    #     #     ]
    #     #     return canvas.create_polygon(points, **kwargs, smooth=True)

    #     # create_rounded_rect(self.shadow_canvas, 0, 0, 750, 320, r=40, fill="#efebeb")

    #     # === Chart Frame ===
    #     self.chart_card_frame = Frame(self.root, bg="white", relief="solid",
    #                                 highlightbackground="#007bff", highlightthickness=2)
    #     self.chart_card_frame.place(x=265, y=650, width=720, height=280)

    #     # Create chart
    #     fig = Figure(figsize=(7.2, 2.6), dpi=100)
    #     ax = fig.add_subplot(111)

    #     # Bar chart with tight spacing
    #     bars = ax.bar(course_names, durations, width=0.9, color='#4CAF50', edgecolor='#388E3C', linewidth=1.5)

    #     # Fix margins on both sides
    #     ax.margins(x=0.01)  # Nearly remove horizontal padding
    #     ax.set_xlim(-0.5, len(course_names) - 0.5)

    #     # Axis labels and title
    #     ax.set_title("Course Duration Chart", fontsize=12, fontweight='bold', color="#007bff")
    #     ax.tick_params(axis='x', rotation=40, labelsize=8, labelcolor="#333333")
    #     ax.tick_params(axis='y', labelsize=10, labelcolor="#333333")
    #     ax.grid(axis='y', linestyle='--', alpha=0.7, color='#B0BEC5')

    #     # Tighter layout for full-width fill
    #     fig.subplots_adjust(left=0.05, right=0.97, top=0.88, bottom=0.3)


    #     # Embed chart in Tkinter
    #     self.bar_canvas = FigureCanvasTkAgg(fig, master=self.chart_card_frame)
    #     self.bar_canvas.draw()
    #     self.bar_canvas.get_tk_widget().place(x=0, y=0, width=710, height=235)










    # def show_student_percentage_pie_chart(self):
    #     con = sqlite3.connect(database="rms.db")
    #     cur = con.cursor()
    #     try:
    #         # Get course data
    #         cur.execute("SELECT cid, name FROM course")
    #         course_data = {cid: name for cid, name in cur.fetchall()}

    #         # Get student results
    #         cur.execute("SELECT name, course, per FROM result")
    #         data = cur.fetchall()

    #         if data:
    #             student_names = []
    #             percentages = []
    #             course_names = []
    #             for row in data:
    #                 student_name, course, per = row
    #                 try:
    #                     per = float(per)
    #                     student_names.append(student_name)
    #                     percentages.append(per)
    #                     course_names.append(str(course))
    #                 except ValueError:
    #                     continue

    #             # Destroy existing chart if already created
    #             if hasattr(self, 'student_pie_frame'):
    #                 self.student_pie_frame.destroy()
    #             if hasattr(self, 'pie_shadow_canvas'):
    #                 self.pie_shadow_canvas.destroy()

    #             # Shadow canvas (reduced size)
    #             self.pie_shadow_canvas = Canvas(self.root, width=520, height=320, bg="white", highlightthickness=0)
    #             self.pie_shadow_canvas.place(x=1000, y=180)
    #             self.pie_shadow_canvas.tag_raise("all")

    #             def create_rounded_rect(canvas, x1, y1, x2, y2, r=25, **kwargs):
    #                 points = [
    #                     x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1,
    #                     x2, y1 + r, x2, y1 + r, x2, y2 - r, x2, y2 - r, x2, y2,
    #                     x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2,
    #                     x1, y2, x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1
    #                 ]
    #                 return canvas.create_polygon(points, **kwargs, smooth=True)

    #             create_rounded_rect(self.pie_shadow_canvas, 0, 0, 520, 320, r=30, fill="#efebeb")

    #             # Chart frame (reduced size)
    #             self.student_pie_frame = Frame(self.root, bg="white", highlightbackground="#28a745", highlightthickness=2)
    #             self.student_pie_frame.place(x=1020, y=200, width=480, height=280)

    #             # Create the pie chart figure
    #             pie_fig = Figure(figsize=(4, 2.5), dpi=100)
    #             pie_ax = pie_fig.add_subplot(111)
    #             pie_fig.subplots_adjust(top=0.85, bottom=0.2, right=0.8)

    #             # Pie chart
    #             wedges, texts = pie_ax.pie(
    #                 percentages,
    #                 labels=None,
    #                 startangle=140,
    #                 wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    #             )

    #             # Legend
    #             legend_labels = [f"{student_names[i]} ({percentages[i]:.1f}%)" for i in range(len(student_names))]
    #             pie_ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9)

    #             # Add course names inside wedges if large enough
    #             for i, wedge in enumerate(wedges):
    #                 theta = np.pi / 180 * (wedge.theta1 + wedge.theta2) / 2
    #                 if wedge.theta2 - wedge.theta1 > 20:
    #                     radius = 0.6
    #                     x = radius * np.cos(theta)
    #                     y = radius * np.sin(theta)
    #                     pie_ax.text(
    #                         x, y,
    #                         course_names[i],
    #                         ha='center',
    #                         va='center',
    #                         fontsize=9,
    #                         fontweight='bold',
    #                         color='white'
    #                     )

    #             # Set centered title
    #             pie_ax.set_title(
    #                 "Student Percentage Distribution",
    #                 fontsize=13,
    #                 fontweight='bold',
    #                 color="#28a745",
    #                 pad=5,
    #                 loc='center'
    #             )

    #             # Tight layout
    #             pie_fig.tight_layout()

    #             # Embed chart in Tkinter
    #             pie_canvas = FigureCanvasTkAgg(pie_fig, master=self.student_pie_frame)
    #             pie_canvas.draw()
    #             pie_canvas.get_tk_widget().pack(fill="both", expand=True)

    #         else:
    #             messagebox.showinfo("Info", "No data found in result table.")

    #     except Exception as ex:
    #         print("Error:", ex)
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}")





import sqlite3

def assign_teacher_to_course(teacher_name, course_name):
    con = sqlite3.connect("rms.db")
    cur = con.cursor()

    # Get teacher ID
    cur.execute("SELECT id FROM teacher WHERE name = ?", (teacher_name,))
    teacher = cur.fetchone()
    if not teacher:
        print(f"Teacher '{teacher_name}' not found.")
        return
    teacher_id = teacher[0]

    # Get course ID
    cur.execute("SELECT cid FROM course WHERE name = ?", (course_name,))
    course = cur.fetchone()
    if not course:
        print(f"Course '{course_name}' not found.")
        return
    course_id = course[0]

    # Insert into teacher_course table
    cur.execute("""
        INSERT OR IGNORE INTO teacher_course (teacher_id, course_id)
        VALUES (?, ?)
    """, (teacher_id, course_id))

    con.commit()
    con.close()
    print(f"✅ Assigned '{teacher_name}' to course '{course_name}'")









import sqlite3

def fetch_data(user_id=None): 
    con = sqlite3.connect("rms.db")
    cur = con.cursor()

    query = """
    SELECT 
        s.name AS student_name,
        s.email,
        s.course,
        c.duration,
        r.marks_ob,
        r.per,
        subj.topics,
        t.name AS teacher_name,        -- teacher name from teacher table
        f.total_fees || ' / Paid: ' || IFNULL(f.paid_amount, 0) AS fee_statement
    FROM 
        student s
    LEFT JOIN 
        course c ON s.course = c.name
    LEFT JOIN 
        result r ON s.roll = r.roll AND r.course = c.name
    LEFT JOIN 
        subjects subj ON subj.name = s.course
    LEFT JOIN 
        teacher t ON t.course = s.course    -- join teacher on course column matching student's course
    LEFT JOIN 
        fees f ON f.student_id = s.roll AND f.course_id = c.cid
    """

    if user_id is not None:
        query += " WHERE s.roll = ?"
        query += " ORDER BY s.name;"
        cur.execute(query, (user_id,))
    else:
        query += " ORDER BY s.name;"
        cur.execute(query)

    rows = cur.fetchall()
    con.close()
    return rows




def show_table(frame, user_id=None):
    import tkinter as tk
    from tkinter import ttk

    columns = ("Student Name", "Email", "Course", "Duration", "Marks", "Percentage", "Topics", "Teacher Name", "Fee Statement")


    # Apply ttk styling
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'), background="#003366", foreground="white")
    style.configure("Treeview", font=('Segoe UI', 10), rowheight=28)
    #style.map("Treeview", background=[("selected", "#63666A")])
    #style.configure("Custom.Treeview", background="white")

    # --- Search Bar Frame ---
    search_frame = tk.Frame(frame, pady=6)
    search_frame.pack(fill="x")

    search_var = tk.StringVar()
    course_var = tk.StringVar()
    result_var = tk.StringVar()

    tk.Label(search_frame, text="Search Student:", font=('Segoe UI', 12, 'bold' )).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=20)
    search_entry.pack(side="left", padx=5)

    tk.Label(search_frame, text="Filter by Course:", font=('Segoe UI', 12, 'bold')).pack(side="left", padx=5)
    course_entry = tk.Entry(search_frame, textvariable=course_var, width=20)
    course_entry.pack(side="left", padx=5)

    # Treeview with scrollbar

    tree_frame = tk.Frame(frame, bd=2, relief="sunken")  # sunken border around Treeview area
    tree_frame.pack(fill="both", expand=True)  # padding so border is visible

    # Vertical Scrollbar
    tree_scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    # Horizontal Scrollbar
    tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    # Treeview widget
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                        yscrollcommand=tree_scroll_y.set,
                        xscrollcommand=tree_scroll_x.set,
                        style="Custom.Treeview")

    tree.pack(fill="both", expand=True)

    # Configure scrollbars
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)


    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=170)

    tree.tag_configure('evenrow', background="#f2f2f2")
    tree.tag_configure('oddrow', background="#ffffff")

    tree.pack(fill="both", expand=True)

    # Function to populate table
    def update_table():
        rows = fetch_data(user_id)

        for item in tree.get_children():
            tree.delete(item)

        for index, row in enumerate(rows):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'

            row = list(row)

            # Format percentage column (index 5)
            per = row[5]
            if per is not None and str(per).strip() != '':
                try:
                    per_float = float(per)
                    row[5] = f"{per_float:.2f}"
                except ValueError:
                    row[5] = str(per)
            else:
                row[5] = "None"

            # Replace None or empty in other columns with "None"
            for i in range(len(row)):
                if i != 5:
                    if row[i] is None or str(row[i]).strip() == '':
                        row[i] = "None"

            #print(row)  # debug print

            tree.insert("", tk.END, values=row, tags=(tag,))






    # Function to filter data
    def filter_data():
        search_text = search_var.get().lower()
        course_text = course_var.get().lower()
        result_text = result_var.get().lower()

        rows = fetch_data(user_id)
        tree.delete(*tree.get_children())

        for index, row in enumerate(rows):
            row = list(row)
            
            name = row[0] if row[0] is not None else ""
            course = row[2] if row[2] is not None else ""
            marks = row[4]
            per = row[5]

            # Format percentage for filtering
            try:
                per_float = float(per)
                per_str = f"{per_float:.2f}"
            except (TypeError, ValueError):
                per_str = ""

            marks_str = str(marks) if marks is not None else ''

            # Check filter conditions
            if (search_text in str(name).lower()) and \
            (course_text in str(course).lower()) and \
            (result_text in per_str.lower() or result_text in marks_str.lower()):
                
                # Format percentage column
                if per is not None and per != '':
                    try:
                        row[5] = f"{float(per):.2f}"
                    except ValueError:
                        row[5] = per
                else:
                    row[5] = ""

                # Replace None or empty or whitespace-only strings with "None" except percentage column
                for i in range(len(row)):
                    if i != 5:
                        if row[i] is None or str(row[i]).strip() == '':
                            row[i] = "None"

                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                tree.insert("", tk.END, values=row, tags=(tag,))


    # Buttons
    tk.Button(search_frame, text="Filter", command=filter_data, bg="#003366", fg="white", font=('Segoe UI', 11, 'bold')).place(x=560, y=2, width=100, height=25)
    tk.Button( search_frame, text="Refresh", command=update_table, bg="#003366", fg="white", font=('Segoe UI', 11, 'bold')).place(x=670, y=2, width=100, height=25)


    # Deselect row on click
    def on_click(event):
        item = tree.identify_row(event.y)
        if item in tree.selection():
            tree.selection_remove(item)

    tree.bind("<Button-1>", on_click)

    update_table()  # Initial load




if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()
