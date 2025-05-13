from tkinter import *
from PIL import Image, ImageTk
from course import CourseClass
from student import StudentClass
from result import ResultClass
from report import ReportClass
from tkinter import messagebox
import os

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1910x1000+0+0")
        self.root.config(bg="white")

        # ===title=====
        title = Label(self.root, text="Student Result Management System", padx=10,font=("times new roman", 20, "bold"), bg="#033054", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)

        # ===Short Menus Frame===
        M_Frame = LabelFrame(self.root, text="Menus", font=("times new roman", 15), bg="white")
        M_Frame.place(x=265, y=70, width=1395, height=80)

        # ===Buttons with fixed manual positions===
        btn_course=Button(M_Frame, text="Course", font=("times new roman", 15, "bold"),bg="#0b5377", fg="white", cursor="hand2",command=self.add_course).place(x=45, y=5, width=180, height=40)
        btn_student=Button(M_Frame, text="Student", font=("times new roman", 15, "bold"),bg="#0b5377", fg="white", cursor="hand2", command=self.add_student).place(x=270, y=5, width=180, height=40)
        btn_result=Button(M_Frame, text="Result", font=("times new roman", 15, "bold"),bg="#0b5377", fg="white", cursor="hand2", command=self.add_result).place(x=495, y=5, width=180, height=40)
        btn_view=Button(M_Frame, text="View Student Result", font=("times new roman", 15, "bold"),bg="#0b5377", fg="white", cursor="hand2", command=self.add_report).place(x=720, y=5, width=180, height=40)
        btn_logout=Button(M_Frame, text="Logout", font=("times new roman", 15, "bold"),bg="#0b5377", fg="white", cursor="hand2", command=self.logout).place(x=945, y=5, width=180, height=40)
        btn_exit=Button(M_Frame, text="Exit", font=("times new roman", 15, "bold"),bg="#0b5377", fg="white", cursor="hand2", command=self.exit_).place(x=1170, y=5, width=180, height=40)


        #===Content Window===
        self.bg_image = Image.open("IMAGES/dash.png")
        self.bg_image = self.bg_image.resize((1000, 550), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.lbl_bg = Label(self.root, image=self.bg_image)
        self.lbl_bg.place(x=660, y=180, width=1000, height=550)

        #===update details===
        self.lbl_course = Label(self.root, text="Total Courses\n[ 0 ]", font=("times new roman", 20),bd=10, relief=RIDGE, bg="#e43b06", fg="white")
        self.lbl_course.place(x=660, y=780, width=300, height=100)

        self.lbl_Student = Label(self.root, text="Total Students\n[ 0 ]", font=("times new roman", 20),bd=10, relief=RIDGE, bg="#0676ad", fg="white")
        self.lbl_Student.place(x=1015, y=780, width=300, height=100)

        self.lbl_Result = Label(self.root, text="Total Results\n[ 0 ]", font=("times new roman", 20), bd=10, relief=RIDGE, bg="#038074", fg="white")
        self.lbl_Result.place(x=1360, y=780, width=300, height=100)


        #===Footer===
        footer = Label(self.root, text="SRMS-Student Result Management System\nContact us for any Technical Issue:87xxxxxx05",font=("times new roman", 12), bg="#262626", fg="white").pack(side=BOTTOM,fill=X)


    def add_course (self):
        self.new_win=Toplevel(self.root)
        self.new_obj=CourseClass(self.new_win)

    def add_student (self):
        self.new_win=Toplevel(self.root)
        self.new_obj=StudentClass(self.new_win)

    def add_result (self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ResultClass(self.new_win)

    def add_report (self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ReportClass(self.new_win)

    def logout(self):
        op=messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root)
        if op==True:
            self.root.destroy()
            os.system("python login.py")

    def exit_(self):
        op=messagebox.askyesno("Confirm", "Do you really want to exit?", parent=self.root)
        if op==True:
            self.root.destroy()
            
            


if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()
