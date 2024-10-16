# jf361_ids706_mp6
[![Python SQL CI](https://github.com/siyiia/jf361_ids706_mp6/actions/workflows/cicd.yml/badge.svg)](https://github.com/siyiia/jf361_ids706_mp6/actions/workflows/cicd.yml)

## Project Introduction
This project is to design a complex SQL query for a Database


## Project Requirments
- Design a complex SQL query involving joins, aggregation, and sorting
- Provide an explanation for what the query is doing and the expected results

## Project Preparation
1. Connect to `Databricks`
   1. create a new workspace, and copy `token number`, `Server hostname`, `HTTP path`.
      2. use the below code to connect to database
      ```python
      import os
      from dotenv import load_dotenv
      from databricks import sql
      load_dotenv()
      connection = sql.connect(server_hostname=os.getenv("SERVER_HOSTNAME"),
                              http_path=os.getenv("HTTP_PATH"),
                              access_token=os.getenv("DATABRICKS_KEY"))
      ```
2. Create necessary tables, `Student`, `StudyFactors`, `AcademicPerformance`
   1. The `Student` table stores basic information about each student, such as their unique ID, gender, and distance from home. This table serves as the foundation for associating each student with other study and performance data.
   2. The `StudyFactors` table stores information related to each student's study habits, including how much they study, how often they attend classes, and how many hours they sleep.
   3. The `AcademicPerformance` table stores details about each student's academic results, including their exam scores, previous academic performance, and any tutoring sessions they attended.
3. Add data from `csv` file to their corresponding tables

## Query Description
The code of query
   ```sql
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
   ```
**Explanation of the code**: 
The query retrieves information about students grouped by gender, **calculating the number of students, total hours studied,
average hours studied, and average exam scores** for each gender. It **joins the `Student`, `StudyFactors`, and `AcademicPerformance`
tables using the `student_id`** to gather this data, then groups the results by gender, **sorts the results by average exam score in descending order**, and displays the gender with the highest average exam score first.


| Gender | num_students | total_hours_studied  | avg_hours_studied | avg_exam_score |
|--------|--------------|----------------------|-------------------|----------------|
| Male   | 23           | 444                  | 19.30             | 67.70          |
| Female | 16           | 283                  | 17.69             | 65.12          |


## Screenshot of the Expected Results of Query
<p>
  <img width="600" src="screenshots/result.png" />
</p>
