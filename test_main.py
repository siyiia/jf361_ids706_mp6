import unittest
import pandas as pd
import os
from main import connect_db, create_table, insert_data, run_complex_query

# Sample test data for the database
TEST_DATA = {
    "Student": pd.DataFrame(
        {
            "student_id": [1, 2],
            "Gender": ["Male", "Female"],
            "Distance_from_Home": ["Near", "Far"],
        }
    ),
    "StudyFactors": pd.DataFrame(
        {
            "student_id": [1, 2],
            "Hours_Studied": [20, 25],
            "Attendance": [80, 90],
            "Sleep_Hours": [6, 7],
        }
    ),
    "AcademicPerformance": pd.DataFrame(
        {
            "student_id": [1, 2],
            "Previous_Scores": [75, 80],
            "Exam_Score": [85, 88],
            "Tutoring_Sessions": [2, 3],
        }
    ),
}


class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = "test_student.db"
        if os.path.exists(cls.db_name):
            os.remove(cls.db_name)

        cls.conn = connect_db(cls.db_name)

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

        create_table(cls.conn, create_tables)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        if os.path.exists(cls.db_name):
            os.remove(cls.db_name)

    def test_insert_data(self):
        insert_data("Student", TEST_DATA["Student"], self.conn)
        insert_data("StudyFactors", TEST_DATA["StudyFactors"], self.conn)
        insert_data("AcademicPerformance", TEST_DATA["AcademicPerformance"], self.conn)

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Student;")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 2)

        cursor.execute("SELECT COUNT(*) FROM StudyFactors;")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 2)

        cursor.execute("SELECT COUNT(*) FROM AcademicPerformance;")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 2)

    def test_run_complex_query(self):
        try:
            run_complex_query(self.conn)
        except Exception as e:
            self.fail(f"run_complex_query() raised an exception {e}")


if __name__ == "__main__":
    unittest.main()
