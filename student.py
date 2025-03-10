import csv
import time
from course import Course, courses # Import the Course class and the courses dictionary
from professor import Professor, professors # Import the Professor class and the professors dictionary
from grades import Grades, grades # Import the grades dictionary

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
    
    def display_all_students_records(self, sort_by="student_id"):
        """ Display all the students details, sorted by the specific field 
        Parameters:
            sorted_by (str): The field to sort the students by
            -- Options: "student_id", "first_name", "last_name"
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
            students_list.sort(key=lambda x: x.student_id)
        elif sort_by == "first_name":
            students_list.sort(key=lambda x: x.first_name)
        elif sort_by == "last_name":
            students_list.sort(key=lambda x: x.last_name)

        # Display the sorted students records
        print(f"\nDisplaying all students records (sorted by {sort_by}):")
        for student in students_list:
            print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
            for course in student.courses:
                print(f"  Course ID: {course['course_id']}")
            print("-" * 30)

    def display_chosen_student_records(self):
        """ Display the chosen student's details and measure lookup time"""
        student_id = input("Enter the student ID: ").strip()
        start_time = time.time() # Record the start time

        if student_id in students: # Check if the student ID exists
            student = students[student_id]
            print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
            for course in student.courses:
                print(f"  Course ID: {course['course_id']}")
        else:
            print(f"Student ID: {student_id} not found.")
        
        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time # Calculate the elapsed time
        print(f"Time taken to lookup student information: {elapsed_time:.6f} seconds")
    
    def display_professor_student_records(self, email_id, sorted_by="student_id"):
        """ Display the professor's students' details, sorted by student ID 
        Parameters:
            sorted_by (str): The field to sort the students by
            -- Options: "student_id", "first_name", "last_name"
        """
        # Validate the sorted_by field
        if sort_by not in ["student_id", "first_name", "last_name"]:
            print("Invalid field to sort by. Sorting by student_id by default.")
            sort_by = "student_id"
        
        # Get the professor's courses
        professor = professors[email_id]
        professor_courses = professor.courses
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
                students_in_course.sort(key=lambda x: x.student_id)
            elif sort_by == "first_name":   
                students_in_course.sort(key=lambda x: x.first_name)
            elif sort_by == "last_name":
                students_in_course.sort(key=lambda x: x.last_name)
            # Display the sorted students records
            print(f"\nDisplaying all students records for course {course_id} (sorted by {sort_by}):")
            for student in students_in_course:
                print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
        
        # Convert the students dictionary to a list of students for sorting
        students_list = list(students.values())

        # Sort the students based on the specific field
        if sort_by == "student_id":
            students_list.sort(key=lambda x: x.student_id)
        elif sort_by == "first_name":
            students_list.sort(key=lambda x: x.first_name)
        elif sort_by == "last_name":
            students_list.sort(key=lambda x: x.last_name)

        # Display the sorted students records
        print(f"\nDisplaying all students records (sorted by {sort_by}):")
        for student in students_list:
            print(f"Student ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
            for course in student.courses:
                print(f"  Course ID: {course['course_id']}")
            print("-" * 30)

    def check_my_grades(self, email_id):
        """ Check the student's grades for all courses or a specific course """
        while True:
            print("1. Check grades for all courses you took.")
            print("2. Check grades for a specific course you took.")
            choice = input("Enter you choice: ").strip()
            if choice == "1":
                print(f"Grades for {students[email_id].first_name} {students[email_id].last_name}:")
                for course in students[email_id].courses:
                    student_grade = grades[(email_id, course)].grades
                    print(f"  Course ID: {course}, Grade: {student_grade}")

            elif choice == "2":
                course_id = input("Enter the course ID: ").strip()
                for course in students[email_id].courses:
                    if course == course_id:
                        student_grade = grades[(email_id, course)].grades
                        print(f"Course ID: {course}, Grade: {student_grade}")
                        return
                    print(f"No grades found for course ID: {course_id}")
            else:
                print("Invalid choice. Please try again.")

    def check_my_marks(self, email_id):
        """ Check the student's marks for all courses or a specific course """
        while True:
            print("1. Check marks for all courses you took.")
            print("2. Check marks for a specific course you took.")
            choice = input("Enter you choice: ").strip()
            if choice == "1":
                print(f"Grades for {students[email_id].first_name} {students[email_id].last_name}:")
                for course in self.courses:
                    student_grade = grades[(email_id, course)].grades
                    student_mark = grades[(email_id, course)].marks
                    print(f"  Course ID: {course}, Grade: {student_grade}, Mark: {student_mark}")

            elif choice == "2":
                course_id = input("Enter the course ID: ").strip()
                for course in students[email_id].courses:
                    student_grade = grades[(email_id, course)].grades
                    student_mark = grades[(email_id, course)].marks
                    if course == course_id:
                        print(f"Course ID: {course}, Grade: {student_grade}, Mark: {student_mark}")
                        return
                    print(f"No grades found for course ID: {course_id}")
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
        
        # Add the new student to the students dictionary
        students[student_id] = Student(student_id, first_name, last_name)
        students[student_id].add_course(",".join(course_ids)) # Pass comma-separated string

        # Save the new student data to Student.csv
        self.save_students_to_csv(student_id, first_name, last_name, course_ids)

        # Save the grade data to Grades.csv
        for course_id in course_ids:
            grades = input(f"Enter the grade for course ID {course_id} (or leave blank if not available): ").strip()
            marks_input = input(f"Enter the mark for course ID {course_id} (or leave blank if not available): ").strip()
            marks = float(marks_input) if marks_input else None # Handle empty input
            self.save_grades_to_csv(student_id, course_id, grades, marks)

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
                writer.writerow(rows) # Write the remaining rows back to the file
            print(f"Student ID: {student_id} deleted successfully from Student.csv")
        except Exception as e:
            print(f"Error deleting student from Student.csv: {e}")
        
        # Delete the student's courses and grades from Grades.csv
        try:
            with open("Grades.csv", mode="w", newline="") as grades_file:
                reader = csv.reader(grades_file)
                rows = [row for row in reader if row[0] != student_id] # Filter out the student
            
            with open("Grades.csv", mode="w", newline="") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(rows) # Write the remaining rows back to the file
            print(f"Student ID: {student_id} deleted successfully from Grades.csv")
        except Exception as e:
            print(f"Error deleting student from Grades.csv: {e}")

    def modify_student_records(self):
        """ Modify a student's first name, last name, or course_ids"""
        student_id = input("Enter the student ID of the student you want to modify: ").strip()
        if student_id in students:
            student = students[student_id]
            print("1. Modify student's frist name.")
            print("2. Modify student's last name.")
            print("3. Mofidy student's course ID.")
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
                sub_option = input("Enter you choice: ").strip()

                if sub_option == "1":
                    # Modify a course ID
                    old_course_id = input("Enter the course Id you want to modify: ").strip()
                    new_course_id = input("Enter the new course ID: ").strip()

                    # Check if the new course ID exists in courses
                    if new_course_id not in courses:
                        print(f"Course ID: {new_course_id} does not exist")
                        return
                    
                    # Check if the new course ID exists in student.courses
                    if new_course_id in student.courses:
                        print(f"Course ID {new_course_id} has existed in the student's course IDs list")
                        return
                    
                    # Find and update the course ID in the student's courses
                    for course in student.courses:
                        if course["course_id"] == old_course_id:
                            course["course_id"] = new_course_id
                            print(f"Course ID {old_course_id} updated to {new_course_id}")
                            break
                    else:
                        print(f"Course ID: {old_course_id} not found")
                        return
                    
                    # Update grades.csv
                    try:
                        with open("Grades.csv", mode="r") as grades_file:
                            reader = csv.reader(grades_file)
                            rows = [row for row in reader]
                        
                        with open("Grades.csv", "w", newline="") as grades_files:
                            writer= csv.writer(grades_file)
                            for row in rows:
                                if row[0] == student_id and row[1] == old_course_id:
                                    row[1] = new_course_id # Update the course ID
                                writer.writerow(row)

                    except Exception as e:
                        print(f"Error updating Grades.csv: {e}")
                
                elif sub_option == "2":
                    # Delete a course ID
                    if len(student.courses) <= 1:
                        print("Cannot delete the only course. A student must have at least one course.")
                        return

                    course_id_to_delete = input("Enter the course ID you want to delete: ").strip()

                    # Remove the course ID from the sutdent's courses
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
                    
                    except Exception as e:
                        print(f"Error deleting grades from Grades.csv: {e}")
                
                elif sub_option == "3":
                    # Add a new course ID
                    new_course_id = input("Enter the new cours ID: ").strip()

                    # Check if the new course ID exists in courses
                    if new_course_id not in courses:
                        print(f"Course ID: {new_course_id} does not exist.")
                        return
                    
                    # Add the new course ID to the student's courses
                    student.courses.append ({"course_id": new_course_id})
                    print(f"Course ID {new_course_id} added successsfully")

                    # Optionally, prompt for grade and mark and add to Grade.csv
                    grade = input(f"Enter the grade for course ID {new_course_id} (or leave blank if not available): ").strip()
                    mark_input = input(f"Enter the mark for course ID {new_course_id} (or leave blank if not available): ").strip()
                    mark = float(mark_input) if mark_input else None
                    self.save_grades_to_csv(student_id, new_course_id, grade, mark)

                else:
                    print("Invalid choice. Please try again.")
                    return
                
            else:
                print("Invalid choice. Please try again.")
            
            # Save changes to Student.csv
            try:
                with open("Student.csv", mode="w", newline="") as student_file:
                    writer = csv.writer(student_file)
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