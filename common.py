import time
import statistics
import csv


##### Initialize data ######
# Use a dictionary (hash table) to store all the courses
courses = {}

##### Class Course #####
class Course:
   
    def __init__(self, course_id=None, course_name=None, description=None):
        self.course_id = course_id # Unique course ID
        self.course_name = course_name # Course name
        self.description = description # Course description
        
    def display_all_courses_records(self, sort_by="course_id", reverse=False):
        """ Display all the courses details, sorted by specific field
        Parameters:
            sorted_by (str): The field to sort the course by
            -- Options: "course_id", "course_name"
            reverse (bool): Whether to sort in reverse order (default: False)
        """

        if not courses:
            print("No courses records found.")
            return
        
        # Validate the sorted_by field
        if sort_by not in ["course_id", "course_name"]:
            print("Invalid field to sort by. Sorting by course_id by default.")
            sort_by = "course_id"
        
        # Convert the courses dictionary to a list of courses for sorting
        courses_list = list(courses.values())
        
        # Sort the courses by the specified field
        if sort_by == "course_id":
            courses_list.sort(key=lambda x: x.course_id, reverse=reverse)
        elif sort_by == "course_name":
            courses_list.sort(key=lambda x: x.course_name, reverse=reverse)
        
        # Display the sorted courses
        print(f"\nDisplaying all courses records (sorted by {sort_by}):")
        for course in courses_list:
            print(f"Course ID: {course.course_id}, Course Name: {course.course_name}, Description: {course.description}")
            print("-" * 80)
        
    def display_chosen_course_records(self):
        """ Display the chosen course's details and measure lookup time"""
        course_id = input("Enter the course ID: ").strip()
        start_time = time.time() # Record the start time

        if course_id in courses: # Check if the course ID exists
            course = courses[course_id]
            print("-" * 80) # Print a line for better readability
            print(f"Course ID: {course.course_id}, Course Name: {course.course_name}, Description: {course.description}")
            print("-" * 80) # Print a line for better readability
        else:
            print(f"Course ID {course_id} not found.")
        
        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time
        print(f"Time taken to loopuo the course: {elapsed_time:.6f} seconds")
    
    def display_course_taught_by_professor_records(self, email_id):
        """ Display the courses taught by the professor"""
        professor_id = email_id
        professor_course_ids = professors[professor_id].courses
        professor_course_ids = [course["course_id"] for course in professor_course_ids] # Get the list of course IDs taught by the professor
        print()
        for course_id in professor_course_ids:
            if course_id in courses:
                course = courses[course_id]
                print(f"Course ID: {course.course_id}, Course Name: {course.course_name}, Description: {course.description}")
            else:
                print(f"Course ID {course_id} not found.")

    def modify_course(self, role, email_id):
        """
        Modify course details.
        If role is "professor", check if the professor teaches the course before modification.

        Args:
            role (str): The role of the user ("admin" or "professor").
            email_id (str): The email ID of the user (used if role is "professor").
        """
        modify_course_id = input("Enter the course ID you want to modify: ").strip()

        # Check if the course ID exists in the courses dictionary
        if modify_course_id not in courses:
            print(f"Course ID {modify_course_id} not found.")
            return

        # If role is "professor", check if the professor teaches the course
        if role == "professor":
            if email_id not in professors:
                print(f"No professor found with email ID: {email_id}")
                return

            professor = professors[email_id]
            professor_course_ids = [course["course_id"] for course in professor.courses]
            if modify_course_id not in professor_course_ids:
                print(f"Professor {professor.name} does not teach Course ID {modify_course_id}. Modification not allowed.")
                return

        # Display current course details
        print("Current course details:")
        course = courses[modify_course_id]
        print(f"Course ID: {course.course_id}, Course Name: {course.course_name}, Description: {course.description}")

        # Prompt user for modification choice
        print("1. Modify course Name")
        print("2. Modify description")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            new_course_name = input("Enter the new course name: ").strip()
            course.course_name = new_course_name
            print(f"Course Name updated to {new_course_name}.")
        
        elif choice == "2":
            new_description = input("Enter the new description: ").strip()
            course.description = new_description
            print(f"Description updated to {new_description}.")
        
        else:
            print("Invalid choice. Please try again.")
            return

        # Save the updated course data to Course.csv
        try:
            with open("Course.csv", mode="r") as course_file:
                reader = csv.reader(course_file)
                rows = [row for row in reader]
            
            updated_rows = []
            for row in rows:
                if row[0] == modify_course_id:
                    row[1] = course.course_name
                    row[2] = course.description
                updated_rows.append(row)
            
            with open("Course.csv", mode="w", newline="") as course_file:
                writer = csv.writer(course_file)
                writer.writerows(updated_rows)
            print(f"Course {modify_course_id} updated successfully in Course.csv.")
        
        except Exception as e:
            print(f"Error updating course in Course.csv: {e}")
        
    def add_new_course(self):
        """ Add a new course """
        course_id = input("Enter the new course ID: ").strip()
        course_name = input("Enter the new course name: ").strip()
        description = input("Enter the description of the course: ").strip()

        # Check if the course ID already exists
        if course_id in courses:
            print("Course ID already exists.")
            return
        
        # Add the new course to the courses dictionary
        courses[course_id] = Course(course_id, course_name, description)

        # Save the new course data to Course.csv
        self.save_courses_to_csv(course_id, course_name, description)

        print(f"New course {course_id} added successfully.") 
    
    def add_new_course_professor(self, email_id):
        """
        Add a new course and assign it to the professor by default.
        Update the Course.csv and professors.csv files directly.

        Args:
            email_id (str): The email ID of the professor adding the course.
        """
        if email_id not in professors:
            print(f"No professor found with email ID: {email_id}")
            return

        course_id = input("Enter the new course ID: ").strip()
        course_name = input("Enter the new course name: ").strip()
        description = input("Enter the description of the course: ").strip()

        # Check if the course ID already exists
        if course_id in courses:
            print("Course ID already exists.")
            return

        # Add the new course to the courses dictionary
        courses[course_id] = Course(course_id, course_name, description)

        # Assign the course to the professor
        professor = professors[email_id]
        professor.courses.append({"course_id":course_id})

        # Save the new course data to Course.csv
        with open("Course.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([course_id, course_name, description])

        # Update the professor's data in professors.csv
        with open("Professor.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Find the professor and update their courses
        for row in rows:
            if row[0] == email_id:  
                professor_courses = [course["course_id"] for course in professor.courses]
                row[3] = ",".join(professor_courses)  
                break

        # Write the updated data back to professors.csv
        with open("Professor.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print(f"New course {course_id} added successfully and assigned to Professor {professor.name}.")

    def delete_course(self, role, email_id):
        """
        Delete a course and its related records from courses, Professor.csv, Student.csv, and Grades.csv.
        If role is "professor", check if the professor teaches the course before deletion.

        Args:
            role (str): The role of the user ("admin" or "professor").
            email_id (str): The email ID of the user (used if role is "professor").
        """
        course_id = input("Enter the course ID you want to delete: ").strip()

        # Check if the course ID exists in the courses dictionary
        if course_id not in courses:
            print(f"Course ID {course_id} not found.")
            return

        # If role is "professor", check if the professor teaches the course
        if role == "professor":
            if email_id not in professors:
                print(f"No professor found with email ID: {email_id}")
                return

            professor = professors[email_id]
            professor_course_ids = [course["course_id"] for course in professor.courses]
            if course_id not in professor_course_ids:
                print(f"Professor {professor.name} does not teach Course ID {course_id}. Deletion not allowed.")
                return

        # Delete the course from the courses dictionary
        del courses[course_id]
        print(f"Course ID {course_id} deleted from the memory successfully.")

        # Delete the course from the Course.csv file
        try:
            with open("Course.csv", mode="r") as course_file:
                reader = csv.reader(course_file)
                rows = [row for row in reader if row[0] != course_id]
            
            with open("Course.csv", mode="w", newline="") as course_file:
                writer = csv.writer(course_file)
                writer.writerows(rows)
            print(f"Course ID {course_id} deleted from Course.csv successfully.")
        
        except Exception as e:
            print(f"Error deleting course from Course.csv: {e}")
        
        # Delete the course from the Professor.csv file
        try:
            with open("Professor.csv", mode="r") as professor_file:
                reader = csv.reader(professor_file)
                rows = [row for row in reader]
            
            header = rows[0]  # Get the header row
            data_rows = rows[1:]  # Get the data rows

            # Remove the course ID from professors' course list
            updated_rows = []
            for row in data_rows:
                if row[3]:  # Check if the course_id column is not empty
                    course_ids = row[3].split(",")
                    course_ids = [cid for cid in course_ids if cid != course_id]
                    row[3] = ",".join(course_ids)
                updated_rows.append(row)
            
            with open("Professor.csv", mode="w", newline="") as professor_file:
                writer = csv.writer(professor_file)
                writer.writerow(header)  # Write the header row
                writer.writerows(updated_rows)  # Write the updated data rows
            print(f"Course ID {course_id} deleted from Professor.csv successfully.")

        except Exception as e:
            print(f"Error deleting course from Professor.csv: {e}")
        
        # Delete the course from the Student.csv file
        try:
            with open("Student.csv", mode="r") as student_file:
                reader = csv.reader(student_file)
                rows = [row for row in reader]
            
            header = rows[0]  # Get the header row
            data_rows = rows[1:]  # Get the data rows

            updated_rows = []
            for row in data_rows:
                if row[3]:  # Check if the course_id column is not empty
                    course_ids = row[3].split(",")
                    course_ids = [cid for cid in course_ids if cid != course_id]
                    row[3] = ",".join(course_ids)
                updated_rows.append(row)
            
            with open("Student.csv", mode="w", newline="") as student_file:
                writer = csv.writer(student_file)
                writer.writerow(header)
                writer.writerows(updated_rows)
            print(f"Course ID {course_id} deleted from Student.csv successfully.")
        except Exception as e:
            print(f"Error deleting course from Student.csv: {e}")
        
        # Delete the course from the Grades.csv file
        try:
            with open("Grades.csv", mode="r") as grades_file:
                reader = csv.reader(grades_file)
                rows = [row for row in reader if row[1] != course_id]
            
            header = rows[0]  # Get the header row
            data_rows = rows[1:]  # Get the data rows

            with open("Grades.csv", mode="w", newline="") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(header)
                writer.writerows(data_rows)
            print(f"Course ID {course_id} deleted from Grades.csv successfully.")

        except Exception as e:
            print(f"Error deleting course from Grades.csv: {e}")
        
    def save_courses_to_csv(self, course_id, course_name, description):
        """ Save the courses data to the CSV file """
        try:
            with open("Course.csv", mode="a") as course_file:
                writer = csv.writer(course_file)
                writer.writerow([course_id, course_name, description])

        except Exception as e:
            print(f"Error saving courses data to CSV: {e}")

##### Read the Course.csv file #####
def load_course_data():
    """ Load course data from the CSV file into the courses dictionary"""
    with open("Course.csv", mode="r") as course_file:
        reader = csv.reader(course_file)
        next(reader) # Skip the header row
        for row in reader:
            course_id, course_name, description = row
            courses[course_id] = Course(course_id, course_name, description)

# Load course data when the module is imported
load_course_data()




##### Initialize data #####
# Use a dictionary (hash table) to store all the students
students = {}

##### Class Student #####
class Student:

    def __init__(self, student_id=None, first_name=None, last_name=None):
        self.student_id = student_id # Unique student ID (primary key)
        self.first_name = first_name # Student's first name
        self.last_name = last_name # Student's last name
        self.courses = [] # List to store student's courses IDs
    
    def add_course(self, course_id_str):
        """ Add course IDs to the student's course list """
        course_ids = [cid.strip() for cid in course_id_str.split(",")] # Split the course IDs into a list
        for course_id in course_ids:
            self.courses.append({
                "course_id": course_id, # Add course ID to the list
            })
    
    def display_all_students_records(self, sort_by="student_id", reverse=False):
        """ Display all the students details, sorted by the specific field 
        Parameters:
            sorted_by (str): The field to sort the students by
            -- Options: "student_id", "first_name", "last_name"
            reverse (bool): Whether to sort in reverse order (default: False)
        """

        if not students: # Check if the students dictionary is empty
            print("No students records found.")
            return

        # Validate the sorted_by field
        if sort_by not in ["student_id", "first_name", "last_name"]:
            print("Invalid field to sort by. Sorting by student_id by default.")
            sort_by = "student_id"
        
        # Convert the students dictionary to a list of students for sorting
        students_list = list(students.values())

        # Sort the students based on the specific field
        if sort_by == "student_id":
            students_list.sort(key=lambda x: x.student_id, reverse=reverse)
        elif sort_by == "first_name":
            students_list.sort(key=lambda x: x.first_name, reverse=reverse)
        elif sort_by == "last_name":
            students_list.sort(key=lambda x: x.last_name, reverse=reverse)

        # Display the sorted students records
        print(f"\nDisplaying all students records (sorted by {sort_by}):")
        for student in students_list:
            print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
            for course in student.courses:
                print(f"  Course ID: {course['course_id']}")
            print("-" * 80)

    def display_chosen_student_records(self):
        """ Display the chosen student's details and measure lookup time"""
        student_id = input("Enter the student ID: ").strip()
        start_time = time.time() # Record the start time

        if student_id in students: # Check if the student ID exists
            student = students[student_id]
            print("-" * 80) 
            print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
            for course in student.courses:
                print(f"  Course ID: {course['course_id']}")
        else:
            print(f"Student ID: {student_id} not found.")
        
        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time # Calculate the elapsed time
        print(f"Time taken to lookup student information: {elapsed_time:.6f} seconds")
        print("-" * 80)
    
    def display_professor_student_records(self, email_id, sort_by="student_id", reverse=False):
        """ Display the professor's students' details, sorted by student ID 
        Parameters:
            sort_by (str): The field to sort the students by
            -- Options: "student_id", "first_name", "last_name"
            reverse (bool): Whether to sort in reverse order (default: False)
        """
        # Validate the sort_by field
        if sort_by not in ["student_id", "first_name", "last_name"]:
            print("Invalid field to sort by. Sorting by student_id by default.")
            sort_by = "student_id"
        
        # Get the professor's courses
        professor = professors[email_id]
        professor_courses = professor.courses
        professor_courses = [course["course_id"] for course in professor_courses]
        for course_id in professor_courses:
            print(f"\nCourse ID: {course_id}")

            # Get the students for the course
            students_in_course = []
            for student in students.values():
                student_course_ids = [course["course_id"] for course in student.courses]
                if course_id in student_course_ids:
                    students_in_course.append(student)
            if not students_in_course:
                print("No students found for this course.")
                continue
            # Sort the students based on the specific field
            if sort_by == "student_id":
                students_in_course.sort(key=lambda x: x.student_id, reverse=reverse) 
            elif sort_by == "first_name":   
                students_in_course.sort(key=lambda x: x.first_name, reverse=reverse)
            elif sort_by == "last_name":
                students_in_course.sort(key=lambda x: x.last_name, reverse=reverse)
            # Display the sorted students records
            print(f"\nDisplaying all students records for course {course_id} (sorted by {sort_by}):")
            for student in students_in_course:
                print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
        
        # Convert the students dictionary to a list of students for sorting
        students_list = list(students.values())

        # Sort the students based on the specific field
        if sort_by == "student_id":
            students_list.sort(key=lambda x: x.student_id, reverse=reverse)
        elif sort_by == "first_name":
            students_list.sort(key=lambda x: x.first_nam, reverse=reverse)
        elif sort_by == "last_name":
            students_list.sort(key=lambda x: x.last_name, reverse=reverse)

        # Display the sorted students records
        print(f"\nDisplaying all students records (sorted by {sort_by}):")
        for student in students_list:
            print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
            for course in student.courses:
                print(f"  Course ID: {course['course_id']}")
            print("-" * 80)

    def display_student_himself_records(self, email_id):
        """ Display the student's own details """
        student = students[email_id]
        print() # Print a blank line for better readability
        print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
        for course in student.courses:
            print(f"  Course ID: {course['course_id']}")

    def check_my_grades(self, email_id):
        """ Check the student's grades for all courses or a specific course """
        while True:
            print("1. Check grades for all courses you took.")
            print("2. Check grades for a specific course you took.")
            choice = input("Enter you choice: ").strip()

            if choice == "1":
                print() # Print a blank line for better readability
                print(f"Grades for {students[email_id].first_name} {students[email_id].last_name}:")
                student_courses = students[email_id].courses
                student_courses = [course["course_id"] for course in student_courses]
                for course in student_courses:
                    # Check if the grade record exists
                    if (email_id, course) in grades:
                        student_grade = grades[(email_id, course)].grade_input
                    else:
                        student_grade = "N/A"
                    print(f"  Course ID: {course}, Grade: {student_grade}")
                return

            elif choice == "2":
                course_id = input("Enter the course ID: ").strip()
                print() # Print a blank line for better readability
                print(f"Grades for {students[email_id].first_name} {students[email_id].last_name}:")
                student_courses = students[email_id].courses
                student_courses = [course["course_id"] for course in student_courses]
                if course_id not in student_courses:
                    print(f"Course ID {course_id} not found in your courses.")
                    return

                if (email_id, course_id) in grades:
                    student_grade = grades[(email_id, course_id)].grade_input
                else:
                    student_grade = "N/A"
                print(f"  Course ID: {course_id}, Grade: {student_grade}")
                return
                
            else:
                print("Invalid choice. Please try again.")

    def check_my_marks(self, email_id):
        """ Check the student's marks for all courses or a specific course """
        while True:
            print("1. Check marks for all courses you took.")
            print("2. Check marks for a specific course you took.")
            choice = input("Enter you choice: ").strip()
            if choice == "1":
                print()
                print(f"Grades for {students[email_id].first_name} {students[email_id].last_name}:")
                student_courses = students[email_id].courses
                student_courses = [course["course_id"] for course in student_courses]
                for course in student_courses:
                    # Check if the grade record exists
                    if (email_id, course) in grades:
                        student_grade = grades[(email_id, course)].grade_input
                        student_mark = grades[(email_id, course)].marks_input
                    else:
                        student_grade = "N/A"
                        student_mark = "N/A"
                    print(f"  Course ID: {course}, Grade: {student_grade}, Mark: {student_mark}")
                return

            elif choice == "2":
                course_id = input("Enter the course ID: ").strip()
                print()
                print(f"Grades for {students[email_id].first_name} {students[email_id].last_name}:")
                student_courses = students[email_id].courses
                student_courses = [course["course_id"] for course in student_courses]
                if course_id not in student_courses:
                    print(f"Course ID {course_id} not found in your courses.")
                    return
                
                if (email_id, course_id) in grades:
                    student_grade = grades[(email_id, course_id)].grade_input
                    student_mark = grades[(email_id, course_id)].marks_input
                else:
                    student_grade = "N/A"
                    student_mark = "N/A"
                print(f"  Course ID: {course_id}, Grade: {student_grade}, Mark: {student_mark}")
                return
            
            else:
                print("Invalid choice. Please try again.")

    def add_new_student(self):
        """ Add a new student """
        student_id = input("Enter the new student's student ID: ").strip()
        first_name = input("Enter the new student's first name: ").strip()
        last_name = input("Enter the new student's last name: ").strip()
        course_ids = input("Enter the course ID the new student took (comma-separated, e.g., DATA200,DATA201)): ").strip()
        
        # Split the input into individual course IDs
        course_ids = [cid.strip() for cid in course_ids.split(",")]

        # Check if the student ID already exists
        if student_id in students:
            print(f"Student ID: {student_id} already exists.")
            return
        
        # Check if all course_ids exist in courses
        invalid_courses_ids = [cid for cid in course_ids if cid not in courses]
        if invalid_courses_ids:
            print(f"Invalid course IDs: {', '.join(invalid_courses_ids)}")
            return

        # Save the grade data to Grades.csv
        for course_id in course_ids:
            grade_input = input(f"Enter the grade (A, B, C, D, F) for course ID {course_id} (or leave blank if not available): ").strip()
            marks_input = input(f"Enter the mark (0-100) for course ID {course_id} (or leave blank if not available): ").strip()

            # Check if the grade and marks are valid
            if grade_input and grade_input not in ["A", "B", "C", "D", "F", "N/A"]:
                print(f"Invalid grade for course ID {course_id}. Please enter a valid grade.")
                return
            
            if marks_input:
                try:
                    marks_input = int(marks_input)
                    if marks_input <0 or marks_input > 100:
                        print(f"Invalid mark for course ID {course_id}. Please enter a mark between 0 and 100.")
                        return
                except ValueError:
                    print(f"Invalid mark for course ID {course_id}. Please enter a valid number.")
                    return
            else:
                marks_input = None
            
            self.save_grades_to_csv(student_id, course_id, grade_input, marks_input) # Save the grade data to Grades.csv    
        
        # Add the new student to the students dictionary
        students[student_id] = Student(student_id, first_name, last_name)
        students[student_id].add_course(",".join(course_ids)) # Pass comma-separated string

        # Save the new student data to Student.csv
        self.save_students_to_csv(student_id, first_name, last_name, course_ids)

        print(f"New student {first_name} {last_name} added successfully.")  

    def delete_student(self):
        """ Delete a student and his/her related records from students, Student.csv, and Grades.csv """
        student_id = input("Enter the student ID of the student you want to delete: ").strip()
        
        # Check if the student ID exists in the students dictionary
        if student_id not in students:
            print(f"Student ID: {student_id} not found.")
            return
        
        # Delete the student from the students dictionary
        del students[student_id]
        print(f"Student ID: {student_id} deleted successfully from memory.")

        # Delete the student from Student.csv
        try:
            with open("Student.csv", mode="r") as student_file:
                reader = csv.reader(student_file)
                rows = [row for row in reader if row[0] != student_id] # Filter out the student
            
            with open("Student.csv", mode="w", newline="") as student_file:
                writer = csv.writer(student_file)
                writer.writerows(rows) # Write the remaining rows back to the file
            print(f"Student ID: {student_id} deleted successfully from Student.csv")
        except Exception as e:
            print(f"Error deleting student from Student.csv: {e}")
        
        # Delete the student's courses and grades from Grades.csv
        try:
            with open("Grades.csv", mode="r") as grades_file:
                reader = csv.reader(grades_file)
                rows = [row for row in reader if row[0] != student_id] # Filter out the student
            
            with open("Grades.csv", mode="w", newline="") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerows(rows) # Write the remaining rows back to the file
            print(f"Student ID: {student_id} deleted successfully from Grades.csv")
        except Exception as e:
            print(f"Error deleting student from Grades.csv: {e}")

    def modify_student_records(self, role, email_id):
        """
        Modify a student's first name, last name, or course IDs.
        If role is "student", the student can only modify their own information.

        Args:
            role (str): The role of the user ("admin" or "student").
            email_id (str): The email ID of the user (used if role is "student").
        """
        if role == "student":
            # Students can only modify their own records
            student_id = email_id  # Assuming email_id is the student ID
        else:
            # Admins can modify any student's records
            student_id = input("Enter the student ID of the student you want to modify: ").strip()

        if student_id not in students:
            print(f"Student ID {student_id} not found.")
            return

        student = students[student_id]
        print("1. Modify student's first name.")
        print("2. Modify student's last name.")
        print("3. Modify student's course IDs.")
        sub_choice = input("Enter your choice: ").strip()

        if sub_choice == "1":
            # Modify first name
            new_first_name = input("Enter the new first name: ").strip()
            student.first_name = new_first_name
            print("First name updated successfully.")

        elif sub_choice == "2":
            # Modify last name
            new_last_name = input("Enter the new last name: ").strip()
            student.last_name = new_last_name
            print("Last name updated successfully.")

        elif sub_choice == "3":
            # Modify course IDs
            print("Current course IDs:", ", ".join([course["course_id"] for course in student.courses]))
            print("1. Modify a course ID.")
            print("2. Delete a course ID.")
            print("3. Add a new course ID.")
            sub_option = input("Enter your choice: ").strip()

            if sub_option == "1":
                # Modify a course ID
                old_course_id = input("Enter the course ID you want to modify: ").strip()
                new_course_id = input("Enter the new course ID: ").strip()

                # Check if the new course ID exists in courses
                if new_course_id not in courses:
                    print(f"Course ID: {new_course_id} does not exist.")
                    return

                # Check if the new course ID already exists in student.courses
                if new_course_id in [course["course_id"] for course in student.courses]:
                    print(f"Course ID {new_course_id} already exists in the student's course IDs list.")
                    return

                # Find and update the course ID in the student's courses
                for course in student.courses:
                    if course["course_id"] == old_course_id:
                        course["course_id"] = new_course_id
                        print(f"Course ID {old_course_id} updated to {new_course_id}.")
                        break
                else:
                    print(f"Course ID: {old_course_id} not found.")
                    return

                # Update Grades.csv
                try:
                    with open("Grades.csv", mode="r") as grades_file:
                        reader = csv.reader(grades_file)
                        rows = [row for row in reader]

                    with open("Grades.csv", mode="w", newline="") as grades_file:
                        writer = csv.writer(grades_file)
                        for row in rows:
                            if row[0] == student_id and row[1] == old_course_id:
                                row[1] = new_course_id  # Update the course ID
                            writer.writerow(row)
                    print("Grades.csv updated successfully.")

                except Exception as e:
                    print(f"Error updating Grades.csv: {e}")

            elif sub_option == "2":
                # Delete a course ID
                if len(student.courses) <= 1:
                    print("Cannot delete the only course. A student must have at least one course.")
                    return

                course_id_to_delete = input("Enter the course ID you want to delete: ").strip()

                # Remove the course ID from the student's courses
                student.courses = [course for course in student.courses if course["course_id"] != course_id_to_delete]
                print(f"Course ID {course_id_to_delete} deleted successfully.")

                # Delete the corresponding grades from Grades.csv
                try:
                    with open("Grades.csv", mode="r") as grades_file:
                        reader = csv.reader(grades_file)
                        rows = [row for row in reader if not (row[0] == student_id and row[1] == course_id_to_delete)]

                    with open("Grades.csv", mode="w", newline="") as grades_file:
                        writer = csv.writer(grades_file)
                        writer.writerows(rows)
                    print("Grades.csv updated successfully.")

                except Exception as e:
                    print(f"Error deleting grades from Grades.csv: {e}")

            elif sub_option == "3":
                # Add a new course ID
                new_course_id = input("Enter the new course ID: ").strip()

                # Check if the new course ID exists in courses
                if new_course_id not in courses:
                    print(f"Course ID: {new_course_id} does not exist.")
                    return

                # Add the new course ID to the student's courses
                student.courses.append({"course_id": new_course_id})
                print(f"Course ID {new_course_id} added successfully.")

                # If role is "admin", prompt for grade and mark
                if role == "admin":
                    grade = input(f"Enter the grade for course ID {new_course_id} (or leave blank if not available): ").strip()
                    mark_input = input(f"Enter the mark for course ID {new_course_id} (or leave blank if not available): ").strip()
                    mark = int(mark_input) if mark_input else None
                    try:
                        with open("Grades.csv", mode="a", newline="") as grades_file:
                            writer = csv.writer(grades_file)
                            # Use "N/A" as a placeholder for missing grades and marks
                            grade = grade if grade else "N/A"
                            mark = mark if mark else "N/A"
                            writer.writerow([student_id, new_course_id, grade, mark])
                            
                    except Exception as e:
                        print(f"Error saving grades data to CSV: {e}")

                else:
                    # Students cannot input grades or marks
                    print("Students cannot input grades or marks. Please contact an administrator.")
                    grade = "N/A"
                    mark = "N/A"
                    try:
                        with open("Grades.csv", mode="a", newline="") as grades_file:
                            writer = csv.writer(grades_file)
                            writer.writerow([student_id, new_course_id, grade, mark])
                            
                    except Exception as e:
                        print(f"Error saving grades data to CSV: {e}")

            else:
                print("Invalid choice. Please try again.")
                return

        else:
            print("Invalid choice. Please try again.")
            return

        # Save changes to Student.csv
        try:
            with open("Student.csv", mode="w", newline="") as student_file:
                writer = csv.writer(student_file)
                # Write the header row
                writer.writerow(["Email_address", "First_name", "Last_name", "Course_ids"])
                for student in students.values():
                    # Convert course IDs to a comma-separated string
                    course_ids_str = ",".join([course["course_id"] for course in student.courses])
                    writer.writerow([student.student_id, student.first_name, student.last_name, course_ids_str])
            print("Student data saved to Student.csv successfully.")
        except Exception as e:
            print(f"Error saving student data to Student.csv: {e}")
        
    def save_students_to_csv(self, student_id, first_name, last_name, course_ids):
        """ Save the students data to the CSV file """
        try:
            with open("Student.csv", mode="a", newline="") as student_file:
                writer = csv.writer(student_file)
                # Convert course_ids list to a comma-separated string
                course_ids_str = ",".join(course_ids)
                writer.writerow([student_id, first_name, last_name, course_ids_str])
        
        except Exception as e:
            print(f"Error saving student data to CSV: {e}")
    
    def save_grades_to_csv(self, student_id, course_id, grades=None, marks=None):
        """ Save the grades data to the CSV file """
        try:
            with open("Grades.csv", mode="a", newline="") as grades_file:
                writer = csv.writer(grades_file)
                # Use "N/A" as a placeholder for missing grades and marks
                grades = grades if grades else "N/A"
                marks = marks if marks else "N/A"
                writer.writerow([student_id, course_id, grades, marks])
                
        except Exception as e:
            print(f"Error saving grades data to CSV: {e}")

##### Read the Student File ######
def load_student_data():
    """  Load student data from the CSV file into the students dictionary """
    try:
        with open("Student.csv", mode = "r") as student_file:
            reader = csv.reader(student_file)
            next(reader) # Skip the header row
            for row in reader:
                student_id, first_name, last_name, course_ids_str = row

                # if student not in students, create new Student object
                if student_id not in students:
                    students[student_id] = Student(student_id, first_name, last_name)
                
                # Add course and grades
                students[student_id].add_course(course_ids_str)
    except FileNotFoundError:
        print("Student.csv not found.")
    except Exception as e:
        print(f"Error loading student data: {e}")

# Load student data when the module is imported
load_student_data()




##### Initialize data #####
# Use a dictionary (harsh table) to store all the professors
professors = {}

##### Class Professor #####
class Professor:
   
    def __init__(self, professor_id=None, name=None, rank=None):
        self.professor_id = professor_id # Unique professor ID (primary key)
        self.name = name # Professor name
        self.rank = rank # Professor rank
        self.courses = [] # List to store professor's course IDs

    def add_course(self, course_id_str):
        course_ids = [cid.strip() for cid in course_id_str.split(",")]
        for course_id in course_ids:
            self.courses.append({
                "course_id": course_id, # Add course ID to the list
            })

    def display_all_professors_records(self, sort_by="professor_id", reverse=False):
        """ Display all the professors details, sorted by specific field
        Parameters:
            sort_by (str): The field to sort the professor by
            -- Options: "student_id", "name"
            reverse (bool): Whether to sort in reverse order (default: False)
        """

        if not professors:
            print("No professors records found.")
            return
        
        # Validate the sorted_by field
        if sort_by not in ["professor_id", "name"]:
            print("Invalid field to sort by. Sorting by professor_id by default.")
            sort_by = "professor_id"
        
        # Convert the professors dictionary to a list of professors for sorting
        professors_list = list(professors.values())
        
        # Sort the professors by the specified field
        if sort_by == "professor_id":
            professors_list.sort(key=lambda x: x.professor_id, reverse=reverse) 
        elif sort_by == "name":
            professors_list.sort(key=lambda x: x.name, reverse=reverse)
        
        # Display the sorted professors
        print(f"\nDisplaying all professors records (sorted by {sort_by}):")
        for professor in professors_list:
            print(f"Professor ID: {professor.professor_id}, Name: {professor.name}, Rank: {professor.rank}")
            for course in professor.courses:
                print(f"  Course ID: {course['course_id']}")
            print("-" * 80)
    
    def display_chosen_professor_records(self):
        """ Display the chosen professor's details and measure lookup time"""
        professor_id = input("Enter the professor ID: ").strip()
        start_time = time.time() # Record the start time

        if professor_id in professors: # Check if the professor ID exists
            professor = professors[professor_id]
            print("-" * 80)
            print(f"Professor ID: {professor.professor_id}, Name: {professor.name}, Rank: {professor.rank}")
            for course in professor.courses:
                print(f"  Course ID: {course['course_id']}")
        else:
            print(f"Professor ID: {professor_id} not found.")

        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time # Calculate the elapsed time
        print(f"Time taken to lookup the professor: {elapsed_time:.6f} seconds")
        print("-" * 80)

    def display_professor_himself(self, email_id):
        """ Display the professor's own details """
        professor_id = email_id
        if professor_id in professors:
            professor = professors[professor_id]
            print(f"\nProfessor ID: {professor.professor_id}, Name: {professor.name}, Rank: {professor.rank}")
            for course in professor.courses:
                print(f"  Course ID: {course['course_id']}")
        else:
            print(f"Professor ID: {professor_id} not found.")

    def add_new_professor(self):
        new_professor_id = input("Enter the new professor ID: ").strip()
        new_name = input("Enter the new professor name: ").strip()
        new_rank = input("Enter the new professor rank: ").strip()  
        new_course_id_str = input("Enter the new course IDs (comma-separated, or leave blank): ").strip()

        # Check if the professor ID already exists
        if new_professor_id in professors:
            print(f"Professor ID: {new_professor_id} already exists.")
            return
        
        # Check if all course IDs in courses (if provided)
        new_course_ids = [cid.strip() for cid in new_course_id_str.split(",")] if new_course_id_str else []
        invalid_course_ids = [cid for cid in new_course_ids if cid not in courses]
        if invalid_course_ids:
            print(f"The following course IDs do not exist: {', '.join(invalid_course_ids)}")
            return
        
        # Check if any course ID is already assigned to another professor
        assigned_courses = []
        for professor_id, professor in professors.items():
            for course in professor.courses:
                if course["course_id"] in new_course_ids:
                    assigned_courses.append(course["course_id"])
        if assigned_courses:
            print(f"The following course IDs are already assigned to another professor: {', '.join(assigned_courses)}")
            print("Please choose other courses.")
            return

        # Create new Professor object
        professors[new_professor_id] = Professor(new_professor_id, new_name, new_rank)
        if new_course_id_str:
            professors[new_professor_id].add_course(new_course_id_str)
        print(f"New professor {new_name} added successfully")

        # Save the data to CSV file
        Professor.save_professors_to_csv()

    def delete_professor(self):
        """ Delete a professor and his/her related course data from all files """
        professor_id = input("Enter the professor ID of the professor you want to delete: ").strip()
        
        # Check if the professor exists
        if professor_id not in professors:
            print(f"Professor ID: {professor_id} not found.")
            return
        
        # Get the course IDs associated with the professor
        course_ids_to_delete = [course["course_id"] for course in professors[professor_id].courses]

        # Delete the professor from the professors dictionary
        del professors[professor_id]
        print(f"Professor ID: {professor_id} deleted successfully from memory.")

        # Delete the professor from Professor.csv
        try:
            with open("Professor.csv", mode="r") as professor_file:
                reader = csv.reader(professor_file)
                rows = [row for row in reader if row[0] != professor_id]
            
            with open("Professor.csv", mode="w", newline="") as professor_file:
                writer = csv.writer(professor_file)
                writer.writerows(rows)
            print(f"Professor ID: {professor_id} deleted successfully from Professor.csv")
        
        except Exception as e:
            print(f"Error deleting professor from Professor.csv: {e}")
        
        # Delete related course data from Grades.csv
        try:
            with open("Grades.csv", mode="r") as grades_file:
                reader = csv.reader(grades_file)
                rows = [row for row in reader if row[1] not in course_ids_to_delete] # Filter out related courses
            
            with open("Grades.csv", mode="w", newline="") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerows(rows)
            print(f"Grades for courses {', '.join(course_ids_to_delete)} deleted from Grades.csv.")
        
        except Exception as e:
            print(f"Error deleting grades from Grades.csv: {e}")
        
        # Delete related course data from Student.csv
        try:
            with open("Student.csv", mode="r") as student_file:
                reader = csv.reader(student_file)
                rows = [row for row in reader]
            
            # Remove the course IDs from students' course lists
            updated_rows = []
            for row in rows:
                student_course_ids = row[3].split(",") if row[3] else []
                student_course_ids = [cid for cid in student_course_ids if cid not in course_ids_to_delete]
                row[3] = ",".join(student_course_ids)  # Update the course IDs
                updated_rows.append(row)

            with open("Student.csv", mode="w", newline="") as student_file:
                writer = csv.writer(student_file)
                writer.writerows(updated_rows)
            print(f"Course IDs {', '.join(course_ids_to_delete)} removed from Student.csv.")
        
        except Exception as e:
            print(f"Error updating Student.csv: {e}")
        
        # Delete related course data from Course.csv
        try:
            with open("Course.csv", mode="r") as course_file:
                reader = csv.reader(course_file)
                rows = [row for row in reader if row[0] not in course_ids_to_delete] # Filter out related courses

                with open("Course.csv", mode="w", newline="") as course_file:
                    writer = csv.writer(course_file)
                    writer.writerows(rows)
                print(f"Course IDs {', '.join(course_ids_to_delete)} deleted from Course.csv.")
        
        except Exception as e:
            print(f"Error deleting courses from Course.csv: {e}")
        
        # Remove the course ID from courses dictionary
        for course in course_ids_to_delete:
            if course in courses:
                del courses[course] 
                print(f"Course ID {course} removed from courses dictionary.")

    def modify_professor_details(self, professor_id=None):
        """ Modify a professor's name, rank, or course IDs."""
        if professor_id in professors:
            professor = professors[professor_id]
            print("1. Modify professor name")
            print("2. Modify professor rank")
            print("3. Modify course IDs")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                # Modify professor name
                new_name = input("Enter the new name: ").strip()
                professor.name = new_name
                print("Name updated successfully.")

            elif choice == "2":
                # Modify professor rank
                new_rank = input("Enter the new rank: ").strip()
                professor.rank = new_rank
                print("Rank updated successfully.")

            elif choice == "3":
                # Modify course IDs
                print("Current course IDs:", ", ".join([course["course_id"] for course in professor.courses]))
                print("1. Modify a course ID")
                print("2. Add a new course ID")
                print("3. Delete a course ID")
                sub_choice = input("Enter your choice: ").strip()

                if sub_choice == "1":
                    # Modify a course ID
                    old_course_id = input("Enter the course ID you want to modify: ").strip()
                    new_course_id = input("Enter the new course ID: ").strip()

                    # Check if the new course ID exists in courses
                    courses_list = list(courses.keys())
                    if new_course_id not in courses_list:
                        print(f"Course ID: {new_course_id} does not exist.")
                        return

                    # Check if the new course ID is already assigned to another professor
                    assigned_professors = []
                    for pid, prof in professors.items():
                        if pid != professor_id:  # Skip the current professor
                            for course in prof.courses:
                                if course["course_id"] == new_course_id:
                                    assigned_professors.append(pid)
                    if assigned_professors:
                        print(f"Course ID {new_course_id} is already assigned to the following professors: {', '.join(assigned_professors)}")
                        print("Please choose another course.")
                        return
                    
                    # Check if the new course ID already exists in the professor's courses
                    if new_course_id in [course["course_id"] for course in professor.courses]:
                        print(f"Course ID {new_course_id} already exists in the professor's course list.")
                        return
                    
                    # Find and update the course ID in the professor's courses
                    for course in professor.courses:
                        if course["course_id"] == old_course_id:
                            course["course_id"] = new_course_id
                            print(f"Couse ID {old_course_id} updated to {new_course_id} from memory.")
                            break

                        else:
                            print(f"Course ID: {old_course_id} not found.")
                
                elif sub_choice == "2":
                    # Add a new course ID
                    new_course_id = input("Enter the new course ID: ").strip()

                    # Check if the new course ID exists in courses
                    if new_course_id not in courses:
                        print(f"Course ID: {new_course_id} does not exist.")
                        return

                    # Check if the new course ID is already assigned to another professor
                    assigned_professors = []
                    for pid, prof in professors.items():
                        if pid != professor_id:
                            for course in prof.courses:
                                if course["course_id"] == new_course_id:
                                    assigned_professors.append(pid)
                    if assigned_professors:
                        print(f"Course ID {new_course_id} is already assigned to the following professors: {', '.join(assigned_professors)}")
                        print("Please choose another course.")
                        return
                    
                    # Check if the new course ID already exists in the professor's courses
                    if new_course_id in [course["course_id"] for course in professor.courses]:
                        print(f"Course ID {new_course_id} already exists in the professor's course list.")
                        return
                    
                    # Add the new course ID to the professor's courses
                    professor.courses.append({"course_id": new_course_id})
                    print(f"Course ID {new_course_id} added successfully.")
                
                elif sub_choice == "3":
                    # Delete a course ID
                    if len(professor.courses) <= 1:
                        print("Cannot delete the only course. A professor must have at lease one course.")
                        return

                    course_id_to_delete = input("Enter the course ID you want to delete: ")

                    # Remove the course ID from the professor's courses
                    professor.courses = [course for course in professor.courses if course["course_id"] != course_id_to_delete]
                    print(f"Course ID {course_id_to_delete} deleted from memory successfully.")

                    # Delete related data from Grades.csv
                    try:
                        with open("Grades.csv", mode="r") as grades_file:
                            reader = csv.reader(grades_file)
                            rows = [row for row in reader if row[1] != course_id_to_delete]

                        with open("Grades.csv", mode="w", newline="") as grades_file:
                            writer = csv.writer(grades_file)
                            writer.writerows(rows)
                        print(f"Grades for Course ID {course_id_to_delete} deleted from Grades.csv.")
                    
                    except Exception as e:
                        print(f"Error deleting grades from Grades.csv: {e}")

                    # Delete related data from Student.csv
                    try:
                        with open("Student.csv", mode="r") as student_file:
                            reader = csv.reader(student_file)
                            rows = [row for row in reader]

                        # Remove the course ID from students' course lists
                        updated_rows = []
                        for row in rows:
                            if row[3]:  # Check if the course_id column is not empty
                                course_ids = row[3].split(",")
                                course_ids = [cid for cid in course_ids if cid != course_id_to_delete]
                                row[3] = ",".join(course_ids)
                            updated_rows.append(row)

                        with open("Student.csv", mode="w", newline="") as student_file:
                            writer = csv.writer(student_file)
                            writer.writerows(updated_rows)
                        print(f"Course ID {course_id_to_delete} removed from Student.csv.")
                    except Exception as e:
                        print(f"Error updating Student.csv: {e}")
                    
                    # Delete related data from Course.csv
                    try:
                        with open("Course.csv", mode="r") as course_file:
                            reader = csv.reader(course_file)
                            rows = [row for row in reader if row[0] != course_id_to_delete]

                        with open("Course.csv", mode="w", newline="") as course_file:
                            writer = csv.writer(course_file)
                            writer.writerows(rows)
                        print(f"Course ID {course_id_to_delete} deleted from Course.csv.")
                    except Exception as e:
                        print(f"Error deleting course from Course.csv: {e}")
                    
                    # Remove the course ID from courses dictionary
                    if course_id_to_delete in courses:
                        del courses[course_id_to_delete] 
                        print(f"Course ID {course_id_to_delete} removed from courses dictionary.")

                else:
                    print("Invalid choice, please enter again.")
                    return
                
            else:
                print("Invalid choice, please enter again.")
                return
            
            # Save the data to CSV file
            Professor.save_professors_to_csv()
        else:
            print(f"Professor ID: {professor_id} not found.")

    def show_course_details_by_professors(self):
        if not self.courses:
            print("No courses found for this professor.")
            return
        print(f"Professor {self.name} teaches the following courses:")
        for course in self.courses:
            print(f"  Course ID: {course['course_id']}")
    
    def save_professors_to_csv():
        with open("Professor.csv", mode="w", newline="") as professor_file:
            writer = csv.writer(professor_file)
            writer.writerow(["Professor_id", "Professor_name", "Rank", "Course_id"])
            for professor in professors.values():
                course_ids = ",".join([course["course_id"] for course in professor.courses])
                writer.writerow([professor.professor_id, professor.name, professor.rank, course_ids])
        print(f"Professor data saved to Professor.csv successfully")

##### Read the Professor File ######
def load_professor_data():
    """ Load the professor data from the CSV file into the professors dictionary """
    with open("Professor.csv", mode = "r") as professor_file:
        reader = csv.reader(professor_file)
        next(reader) # Skip the header row
        for row in reader:
            professor_id, name, rank, course_id_str = row

            # if professor not in professors, create new Professor object
            if professor_id not in professors:
                professors[professor_id] = Professor(professor_id, name, rank)
            
            # Add course
            professors[professor_id].add_course(course_id_str)

# Load professor data when the module is imported
load_professor_data()



##### Initialize data #####
# Use a dictionary (hash table) to store all the grades, with (student_id, course_id) as the key
grades = {}

##### Class Grades #####
class Grades:

    def __init__(self, student_id=None, course_id=None, grade_input=None, marks_input=None):
        self.student_id = student_id # Unique student ID # Composite primary key (student_id, course_id)
        self.course_id = course_id # Unique course ID # Composite primary key (student_id, course_id)
        self.grade_input = grade_input # Grade input (A, B, C, D, F)
        self.marks_input = marks_input # Marks input (0-100)

    def display_all_grades_records(self, sort_by="name", reverse=False):
        """
        Display all the grades details, sorted by a specific field.

        Parameters:
            sort_by (str): The field to sort the grades by.
                Options: "name", "grades", "marks". Default is "name".
            reverse (bool): Whether to sort in reverse order. Default is False.
        """
        if not grades:
            print("No grades records found.")
            return

        # Validate the sort_by field
        if sort_by not in ["student_id", "grades", "marks"]:
            print("Invalid field to sort by. Sorting by student_id by default.")
            sort_by = "student_id"

        # Convert the grades dictionary to a list of grades for sorting
        grades_list = list(grades.values())

        # Sort the grades by the specified field
        if sort_by == "student_id":
            # Sort by student ID
            grades_list.sort(key=lambda grade: grade.student_id, reverse=reverse)
        elif sort_by == "grades":
            # Sort by grades (e.g., A, B, C)
            grades_list.sort(key=lambda grade: grade.grade_input, reverse=reverse)
        elif sort_by == "marks":
            # Sort by marks (numerical value)
            grades_list.sort(
                key=lambda grade: (
                    float('inf')  
                    if grade.marks_input.lower() in ['n/a', 'f', 'unknown', '']  
                    else float(grade.marks_input)  
                ),
                reverse=reverse
            )

        # Display the sorted grades
        print(f"\nDisplaying all grades records (sorted by {sort_by}):")
        for grade in grades_list:
            print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")
        
    def display_chosen_grade_records(self):
        """ Display the chosen grade's details and measure lookup time """
        student_id = input("Enter the student ID (or leave bland to see all students): ").strip()
        course_id = input("Enter the course ID (or leave blank to see all courses): ").strip()
        start_time = time.time() # Record the start time

        if student_id and course_id:
            # Case 1: Both student_id and course_id are provided
            if (student_id, course_id) in grades:
                grade = grades[(student_id, course_id)]
                print("-" * 80)
                print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")
                print("-" * 80)
            else:
                print("Grade not found.")
        
        elif student_id:
            # Case 2: Only student_id is provided
            found = False
            print("-" * 80)
            print(f"Displaying grades for Student ID: {student_id}")
            for key, grade in grades.items():
                if key[0] == student_id:
                    print(f"Course ID: {grade.course_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")
                    found = True
            if not found:
                print("No grades found for the student.")
        
        elif course_id:
            # Case 3: Only course_id is provided
            found = False
            for key, grade in grades.items():
                if key[1] == course_id:
                    print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")
                    found = True
            if not found:
                print("No grades found for the course.")
        
        else:
            # Case 4: Both student_id and course_id are not provided
            print("Please provide at least a student ID or course ID to lookup a grade.")

        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time
        print(f"Time taken to lookup the grade: {elapsed_time:.6f} seconds")

    def display_professor_grades(self, email_id, sort_by="student_id", reverse=False):
        """
        Display the grades for all courses taught by a professor, with optional sorting.

        Args:
            email_id (str): The email ID of the professor.
            sort_by (str): The sorting criteria. Options: "student_id", "grades", "marks". Default is "student_id".
            reverse (bool): Whether to sort in reverse order. Default is False.
        """
        if email_id not in professors:
            print(f"No professor found with email ID: {email_id}")
            return

        professor = professors[email_id]
        professor_course_ids = professor.courses
        professor_course_ids = [course["course_id"] for course in professor_course_ids]
        print(f"\nDisplaying grades for Professor {professor.name} (Professor ID: {email_id})")

        for course_id in professor_course_ids:
            print(f"\nCourse ID: {course_id}")
            course_grades = [grade for key, grade in grades.items() if key[1] == course_id]

            if not course_grades:
                print("No grades available for this course.")
                continue

            # Sort grades based on the specified criteria
            if sort_by == "student_id":
                # Sort by student ID
                course_grades.sort(key=lambda grade: grade.student_id, reverse=reverse)
            elif sort_by == "grades":
                # Sort by grades (e.g., A, B, C)
                course_grades.sort(key=lambda grade: grade.grade_input, reverse=reverse)
            elif sort_by == "marks":
                # Sort by marks (numerical value)
                course_grades.sort(key=lambda grade: int(grade.marks_input), reverse=reverse)

            # Display sorted grades
            for grade in course_grades:
                if grade.student_id not in students:
                    print(f"  Student ID: {grade.student_id} not found in students database.")
                    continue

                student = students[grade.student_id]
                print(f"  Student ID: {grade.student_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")

    def display_professor_chosen_grades(self, email_id, course_id, sort_by="student_id", reverse=False):
        """
        Display grades for a chosen course taught by a professor, with optional statistics.

        Args:
            email_id (str): The email ID of the professor.
            course_id (str): The ID of the course to display grades for.
            sort_by (str): The field to sort the grades by. Options: "student_id", "grades", "marks". Default is "student_id".
            reverse (bool): Whether to sort in reverse order. Default is False.
        """
        if email_id not in professors:
            print(f"No professor found with email ID: {email_id}")
            return

        professor = professors[email_id]
        professor_course_ids = professor.courses
        professor_course_ids = [course["course_id"] for course in professor_course_ids]
        print(professor_course_ids)
        if course_id not in professor_course_ids:
            print(f"Course ID {course_id} is not taught by Professor {professor.name}.")
            return

        # Get all grades for the chosen course
        course_grades = [grade for key, grade in grades.items() if key[1] == course_id]

        if not course_grades:
            print(f"No grades available for Course ID: {course_id}.")
            return

        # Validate the sort_by field
        if sort_by not in ["student_id", "grades", "marks"]:
            print("Invalid field to sort by. Sorting by student_id by default.")
            sort_by = "student_id"

        # Sort the grades by the specified field
        if sort_by == "student_id":
            # Sort by student name
            course_grades.sort(key=lambda grade: grade.student_id, reverse=reverse)
        elif sort_by == "grades":
            # Sort by grades (e.g., A, B, C)
            course_grades.sort(key=lambda grade: grade.grade_input, reverse=reverse) 
        elif sort_by == "marks":
            # Sort by marks (numerical value)
            course_grades.sort(key=lambda grade: int(grade.marks_input), reverse=reverse)

        # Display sorted grades
        print(f"\nDisplaying grades for Course ID: {course_id} (Taught by Professor {professor.name}, Sorted by {sort_by})")
        for grade in course_grades:
            if grade.student_id not in students:
                print(f"  Student ID: {grade.student_id} not found in students database.")
                continue

            student = students[grade.student_id]
            print(f"  Student ID: {grade.student_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")

        # Ask the user if they want to see statistics
        while True:
            user_input = input("\nDo you want to see statistics? (yes/no): ").strip().lower()
            if user_input in ["yes", "no"]:
                break
            print("Invalid input. Please enter 'yes' or 'no'.")

        if user_input == "yes":
            # Calculate statistics
            marks_list = [int(grade.marks_input) for grade in course_grades]
            print(type(marks_list)) 
            average_mark = sum(marks_list) / len(marks_list)
            median_mark = sorted(marks_list)[len(marks_list) // 2] if len(marks_list) % 2 != 0 else (
                sorted(marks_list)[len(marks_list) // 2 - 1] + sorted(marks_list)[len(marks_list) // 2]) / 2
            highest_mark = max(marks_list)
            lowest_mark = min(marks_list)

            print("\nChoose statistics to display:")
            print("1. Average Mark")
            print("2. Median Mark")
            print("3. Highest Mark")
            print("4. Lowest Mark")
            print("5. All of the above")

            while True:
                try:
                    choice = int(input("Enter your choice (1-5): "))
                    if 1 <= choice <= 5:
                        break
                    print("Invalid choice. Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # Display selected statistics
            if choice == 1:
                print(f"\nAverage Mark: {average_mark:.2f}")
            elif choice == 2:
                print(f"\nMedian Mark: {median_mark}")
            elif choice == 3:
                print(f"\nHighest Mark: {highest_mark}")
            elif choice == 4:
                print(f"\nLowest Mark: {lowest_mark}")
            elif choice == 5:
                print(f"\nAll Statistics:")
                print(f"1. Average Mark: {average_mark:.2f}")
                print(f"2. Median Mark: {median_mark}")
                print(f"3. Highest Mark: {highest_mark}")
                print(f"4. Lowest Mark: {lowest_mark}")
    
    def add_new_grade(self, role, email_id):
        # Add a grade for a student in a course by a professor or admin
        student_id = input("Enter the student ID: ").strip()
        course_id = input("Enter the course ID: ").strip()
        grade_input = input("Enter the grades (A, B, C, D, F, or N/A): ").strip()
        marks_input = input("Enter the marks (0-100, or N/A): ").strip()

        # Check if the student exists
        if student_id not in students:
            print("Student not found.")
            return
        
        # Check if the course exists
        if course_id not in courses:
            print("Course not found.")
            return
        
        # Check if the student is enrolled in the course
        if (student_id, course_id) not in grades:
            print("Student is not enrolled in the course.")
            return
        
        # Check if the student's current grades and marks are N/A
        current_grade = grades[((student_id, course_id))].grade_input
        current_marks = grades[((student_id, course_id))].marks_input
        if current_grade != "N/A" or current_marks != "N/A":
            print("The student already has a grade or marks for this course. Cannot overwrite. Please use modify grade function to update the grade.")
            return

        # Check if the grades are valid
        if grade_input not in ["A", "B", "C", "D", "F", "N/A"]:
            print("Invalid grades. Please enter A, B, C, D, F, or N/A.")
            return
        
        # Check if the marks are valid
        if marks_input != "N/A" and (not marks_input.isdigit() or int(marks_input) < 0 or int(marks_input) > 100):
            print("Invalid marks. Please enter a number between 0 and 100.")
            return
        
        # Check if the user has the right to add a grade
        if role == "professor":
            # Check if the professor is teaching the course
            professor = professors[email_id]
            professor_course_ids = professor.courses
            professor_course_ids = [course["course_id"] for course in professor_course_ids]
            if course_id not in professor_course_ids:
                print("You do not have the right to add a grade for this course.")
                return
            # Add the grade
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade modified successfully.")

        elif role == "admin":
            # Admin can add a grade for the course
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)
            
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade modified successfully.")

        else:
            print("You do not have the right to add a grade.")

    def delete_grade(self, role, email_id):
        # Delete a grade for a student in a course by a professor or admin
        student_id = input("Enter the student ID of the grade to be deleted: ").strip()
        course_id = input("Enter the course ID of the grade to be deleted: ").strip()
        if (student_id, course_id) not in grades:
            print("Grade not found.")
            return
        
        # Check if the user has the right to delete a grade
        if role == "professor":
            # Check if the professor is teaching the course
            professor = professors[email_id]
            professor_course_ids = professor.courses
            professor_course_ids = [course["course_id"] for course in professor_course_ids]
    
            if course_id not in professor_course_ids:
                print("You do not have the right to delete a grade for this course.")
                return
            
            # Delete the grade
            del grades[(student_id, course_id)]
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade deleted successfully.")
        
        elif role == "admin":
            # Admin can delete a grade for any course
            del grades[(student_id, course_id)]
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade deleted successfully.")

        else:
            print("You do not have the right to delete a grade.")

    def modify_grade(self, role, email_id):
        # Modify a grade for a student in a course by a professor or admin
        student_id = input("Enter the student ID of the grade to be modified: ").strip()
        course_id = input("Enter the course ID of the grade to be modified: ").strip()
        if (student_id, course_id) not in grades:
            print("Grade not found.")
            return
        # Check if the user has the right to modify a grade
        if role == "professor":
            # Check if the professor is teaching the course
            professor = professors[email_id]
            professor_course_ids = professor.courses
            professor_course_ids = [course["course_id"] for course in professor_course_ids]
    
            if course_id not in professor_course_ids:
                print("You do not have the right to modify a grade for this course.")
                return
            
            # Modify the grade
            grade_input = input("Enter the new grades (A, B, C, D, F): ").strip()
            marks_input = input("Enter the new marks (0-100): ").strip()
            # Check if the grades are valid
            if grade_input not in ["A", "B", "C", "D", "F"]:
                print("Invalid grades. Please enter A, B, C, D, or F.")
                return
            # Check if the marks are valid  
            if not marks_input.isdigit() or int(marks_input) < 0 or int(marks_input) > 100:
                print("Invalid marks. Please enter a number between 0 and 100.")
                return
            # Modify the grade
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade modified successfully.")
        
        elif role == "admin":
            # Admin can modify a grade for any course
            grade_input = input("Enter the new grades (A, B, C, D, F): ").strip()
            marks_input = input("Enter the new marks (0-100): ").strip()
            # Check if the grades are valid
            if grade_input not in ["A", "B", "C", "D", "F"]:
                print("Invalid grades. Please enter A, B, C, D, or F.")
                return
            # Check if the marks are valid  
            if not marks_input.isdigit() or int(marks_input) < 0 or int(marks_input) > 100:
                print("Invalid marks. Please enter a number between 0 and 100.")
                return
            # Modify the grade
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade modified successfully.")
        else:
            print("You do not have the right to modify a grade.")

    def grade_report_student(self, role, email_id):
        """ Generate a grade report for a student by a professor, admin, or the student himself/herself """
        if role == "admin":
            # Admin can generate a grade report for any student
            student_id = input("Enter the student ID: ").strip()
            if student_id not in students:
                print("Student not found.")
                return
            
        elif role == "professor":
            # Professor can generate a grade report for any student in his/her courses
            student_id = input("Enter the student ID: ").strip()
            if student_id not in students:
                print("Student not found.")
                return
            
            professor_course_ids = professors[email_id].courses
            professor_course_ids = [course_id for course_id in professor_course_ids]
            # Check if the student is enrolled in any of the professor's courses
            student_course_ids = students[student_id].courses
            student_course_ids = [course_id for course_id in student_course_ids if course_id in professor_course_ids]
            if not student_course_ids:
                print("Student is not enrolled in any of your courses.")
                return
            
        elif role == "student":
            # Student can only see their own grades
            student_id = email_id

        else:
            print("You do not have the right to generate a grade report.")
            return
        
        student = students[student_id]
        student_first_name = student.first_name
        student_last_name = student.last_name
        student_course_ids = student.courses
        student_course_ids = [course['course_id'] for course in student_course_ids]

        print(f"\nGrade Report for {student_first_name} {student_last_name} (Student ID: {student_id})")
        
        # Display the student's courses and grades
        grade_list = []
        for course_id in student_course_ids:
            if (student_id, course_id) in grades:
                student_grade = grades[(student_id, course_id)].grade_input
                student_marks = grades[(student_id, course_id)].marks_input
                print(f"  Course ID: {course_id}, Grade: {student_grade}, Marks: {student_marks}")
                print("-"*60)
                grade_list.append(float(student_marks))
            else:
                print(f"  Course ID: {course_id}, Grade: Not Available, Marks: Not Available")
        
        # Statistics
        if grade_list:
            print("\nStatistics:")
            print(f"  Total Courses Enrolled: {len(student_course_ids)}")
            print(f"  Average Grade: {statistics.mean(grade_list):.2f}")
            print(f"  Median Grade: {statistics.median(grade_list):.2f}")
            print(f"  Highest Grade: {max(grade_list)}")
            print(f"  Lowest Grade: {min(grade_list)}")
        else:
            print("No grades available for this student.")

    def grade_report_professor(self, role, email_id):
        """ Generate a grade report for a professor by an admin or the professor himself/herself """
        if role == "admin":
            # Admin can generate a grade report for any professor
            professor_id = input("Enter the professor ID: ").strip()
            if professor_id not in professors:
                print("Professor not found.")
                return
        
        elif role == "professor":
            # Professor can only see their own grades
            professor_id = email_id
        
        else:
            print("You do not have the right to generate a grade report.")
        
        professor_course_ids = professors[professor_id].courses
        professor_course_ids = [course["course_id"] for course in professor_course_ids]
        professor_name = professors[professor_id].name
        print(f"\nGrade Report for {professor_name} (Professor ID: {professor_id})")

        # Display the professor's courses and grades
        for course_id in professor_course_ids:
            print(f"\n  Course ID: {course_id}")
            course_grades = [grade for key, grade in grades.items() if key[1] == course_id]
            if not course_grades:
                print("    No grades available for this course.")
                continue
            marks_list = [float(grade.marks_input) for grade in course_grades]

        # Statistics
            print("\nStatistics:")
            print(f"  Total students graded: {len(marks_list)}")
            print(f"  Average Grade: {statistics.mean(marks_list):.2f}")
            print(f"  Median Grade: {statistics.median(marks_list):.2f}")
            print(f"  Highest Grade: {max(marks_list)}")
            print(f"  Lowest Grade: {min(marks_list)}")
    
    def grade_report_course(self, role, email_id):
        # Generate a grade report for a course by an admin or the professor teaching the course
        if role == "admin":
            # Admin can generate a grade report for any course
            course_id = input("Enter the course ID: ").strip()
            if course_id not in courses:
                print("Course not found.")
                return
            
        elif role == "professor":
            # Professor can only see their own grades
            professor = professors[email_id]
            professor_course_ids = professor.courses
            professor_course_ids = [course["course_id"] for course in professor_course_ids]
            course_id = input("Enter the course ID: ").strip()
            if course_id not in professor_course_ids:
                print("You do not have the right to generate a grade report for this course.")
                return
        
        else:
            print("You do not have the right to generate a grade report.")
            return
        
        course = courses[course_id]
        print(f"\nGrade Report for Course: {course.course_name} (Course ID: {course_id})")
        course_grades = [grade for key, grade in grades.items() if key[1] == course_id]
        if not course_grades:
            print("No grades available for this course.")
            return
        
        # Display the course's students and grades
        marks_list = []
        for grade in course_grades:
            student = students[grade.student_id]
            student_name = f"{student.first_name} {student.last_name}"
            print(f"  Student ID: {grade.student_id}, Name: {student_name}, Grade: {grade.grade_input}, Marks: {grade.marks_input}")
            marks_list.append(float(grade.marks_input))

        # Statistics
        print("\nStatistics:")
        print(f"  Total students graded: {len(marks_list)}")
        print(f"  Average Grade: {statistics.mean(marks_list):.2f}")
        print(f"  Median Grade: {statistics.median(marks_list):.2f}")
        print(f"  Highest Grade: {max(marks_list)}")
        print(f"  Lowest Grade: {min(marks_list)}")

##### Read the Grades CSV file #####
def load_grades_data():
    """ Load grades data from CSV file """
    with open("Grades.csv", "r") as grades_file:
        reader = csv.reader(grades_file)
        next(reader)
        for row in reader:
            student_id, course_id, grade_input, marks_input = row
            # Use (student_id, course_id) as the key
            key = (str(student_id), str(course_id))
            grades[key] = Grades(student_id, course_id, grade_input, marks_input)

# Load grades data when the module is imported
load_grades_data()


