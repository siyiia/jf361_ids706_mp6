import sqlite3
import pandas as pd
import os


# Function to connect to the database
def connect_db(db_name="student.db"):
    conn = sqlite3.connect(db_name)
    print(f"Connected to {db_name}")
    return conn


# Function to create a table (Create operation)
def create_table(conn, create_tables):
    try:
        for table_name, create_query in create_tables.items():
            conn.execute(create_query)
            print(f"Table {table_name} created successfully!")

    except sqlite3.Error as e:
        print(f"Error creating table: {e}")


# Inserting data into the tables
def insert_data(table_name, dataframe, conn):
    try:
        for _, row in dataframe.iterrows():
            placeholders = ", ".join(["?"] * len(row))
            columns = ", ".join(row.index)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            conn.execute(sql, tuple(row))
        print(f"Record inserted successfully of table {table_name}")
    except sqlite3.Error as e:
        print(f"Error inserting record: {e}")


def run_complex_query(conn):
    query = """
    SELECT 
        s.Gender,
        COUNT(s.student_id) AS num_students,
        SUM(sf.Hours_Studied) AS total_hours_studied,
        AVG(sf.Hours_Studied) AS avg_hours_studied,
        AVG(ap.Exam_Score) AS avg_exam_score
    FROM 
        Student s
    JOIN 
        StudyFactors sf ON s.student_id = sf.student_id
    JOIN 
        AcademicPerformance ap ON s.student_id = ap.student_id
    GROUP BY 
        s.Gender
    ORDER BY 
        avg_exam_score DESC;
    """

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    print(
        "Gender | num_students | total_hours_studied | avg_hours_studied | avg_exam_score"
    )
    print("-" * 80)
    for row in rows:
        print(
            f"{row[0]:<6} | {row[1]:<12} | {row[2]:<18} | {row[3]:<17.2f} | {row[4]:<14.2f}"
        )
    print("\nQuery executed and results fetched successfully!")


def main():
    # Load the CSV file
    file_path = "./StudentPerformanceFactors.csv"
    data = pd.read_csv(file_path)

    # Splitting data for each table
    student_data = data[["Gender", "Distance_from_Home"]]
    study_factors_data = data[["Hours_Studied", "Attendance", "Sleep_Hours"]]
    academic_performance_data = data[
        ["Previous_Scores", "Exam_Score", "Tutoring_Sessions"]
    ]

    # Add student_id to each table
    student_data.insert(0, "student_id", range(1, len(student_data) + 1))
    study_factors_data.insert(0, "student_id", range(1, len(study_factors_data) + 1))
    academic_performance_data.insert(
        0, "student_id", range(1, len(academic_performance_data) + 1)
    )

    # Create the tables
    create_tables = {
        "Student": """
        CREATE TABLE IF NOT EXISTS Student (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Gender VARCHAR(10),
            Distance_from_Home VARCHAR(10)
        );
        """,
        "StudyFactors": """
        CREATE TABLE IF NOT EXISTS StudyFactors (
            student_id INTEGER,
            Hours_Studied INT,
            Attendance INT,
            Sleep_Hours INT,
            FOREIGN KEY (student_id) REFERENCES Student(student_id)
        );
        """,
        "AcademicPerformance": """
        CREATE TABLE IF NOT EXISTS AcademicPerformance (
            student_id INTEGER,
            Previous_Scores INT,
            Exam_Score INT,
            Tutoring_Sessions INT,
            FOREIGN KEY (student_id) REFERENCES Student(student_id)
        );
        """,
    }

    db_name = "student.db"
    if os.path.exists(db_name):
        os.remove(db_name)

    conn = connect_db(db_name)
    create_table(conn, create_tables)

    insert_data("Student", student_data, conn)
    insert_data("StudyFactors", study_factors_data, conn)
    insert_data("AcademicPerformance", academic_performance_data, conn)

    run_complex_query(conn)

    conn.close()


if __name__ == "__main__":
    main()
