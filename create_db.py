import sqlite3

def create_db():
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()

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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,dob text,contact text,admission text,course text,state text,city text,pin text,address text
        )
    """)
    
    con.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            course TEXT,
            marks_ob TEXT,
            full_marks TEXT,
            per TEXT
        )
    """)

    con.commit()

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

    # Checking values in each table
    def check_values():
        # Checking course table
        cur.execute("SELECT * FROM course")
        courses = cur.fetchall()
        print("Courses:")
        for course in courses:
            print(course)

        # Checking student table
        cur.execute("SELECT * FROM student")
        students = cur.fetchall()
        print("\nStudents:")
        for student in students:
            print(student)

        # Checking result table
        cur.execute("SELECT * FROM result")
        results = cur.fetchall()
        print("\nResults:")
        for result in results:
            print(result)

        # Checking employee table
        cur.execute("SELECT * FROM employee")
        employees = cur.fetchall()
        print("\nEmployees:")
        for employee in employees:
            print(employee)

    check_values()

    con.close()

create_db()
