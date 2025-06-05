import sqlite3

def reset_db():
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()

    # Employee Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            f_name TEXT NOT NULL,
            l_name TEXT,
            contact TEXT,
            email TEXT UNIQUE NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    con.commit()

    # Course Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
    """)
    con.commit()

    # Student Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            admission TEXT,
            course TEXT,
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
    """)
    con.commit()

    # Result Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            roll TEXT,
            name TEXT,
            course TEXT,
            marks_ob TEXT,
            full_marks TEXT,
            per TEXT,
            FOREIGN KEY(user_id) REFERENCES employee(eid)
        )
    """)
    con.commit()

    # Subject Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            time TEXT NOT NULL,
            topics TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES employee(eid)
        )
    """)
    con.commit()

    

        # Teacher Table

    # Create new table with corrected column order
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teacher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            qualification TEXT,
            experience TEXT,
            state TEXT,
            city TEXT,
            address TEXT,
            course TEXT
        )
    """)

    con.commit()
 
    print("Teacher table dropped and recreated successfully.")

    # Teacher_Course Table - to assign courses to teachers (many-to-many)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teacher_course (
            teacher_id INTEGER,
            course_id INTEGER,
            PRIMARY KEY (teacher_id, course_id),
            FOREIGN KEY (teacher_id) REFERENCES teacher(id),
            FOREIGN KEY (course_id) REFERENCES course(cid)
        )
    """)
    con.commit()

    # NEW TABLE: Enrollments
    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES student(roll),
            FOREIGN KEY (course_id) REFERENCES course(cid)
        )
    """)
    con.commit()

    #  NEW TABLE: Fees
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            total_fees INTEGER,
            paid_amount INTEGER,
            date_paid TEXT,
            status TEXT,
            FOREIGN KEY (student_id) REFERENCES student(roll),
            FOREIGN KEY (course_id) REFERENCES course(cid)
        )
    """)
    con.commit()
    

    # Print all tables in the database
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table[0])

    con.close()

if __name__ == "__main__":
    reset_db()
