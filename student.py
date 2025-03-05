import csv
import time

##### Initialize data #####
# Use a dictionary (hash table) to store all the students
students = {}

##### Class Student #####
class Student:

    def __init__(self, student_id, first_name, last_name):
        self.student_id = student_id # Unique student ID (primary key)
        self.first_name = first_name # Student's first name
        self.last_name = last_name # Student's last name
        self.courses = [] # List to store student's courses IDs
    
    def add_course(self, course_id_str):
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

    def check_my_grades(self):
        if not self.courses:
            print("No grades found.")
            return
        
        while True:
            print("1. Check grades for all courses you took.")
            print("2. Check grades for a specific course you took.")
            choice = input("Enter you choice: ").strip()
            if choice == "1":
                print(f"Grades for {self.first_name} {self.last_name}:")
                for course in self.courses:
                    print(f"  Course ID: {course['course_id']}, Grade: {course['grade']}")

            elif choice == "2":
                course_id = input("Enter the course ID: ").strip()
                for course in self.courses:
                    if course["course_id"] == course_id:
                        print(f"Course ID: {course['course_id']}, Grade: {course['grade']}")
                        return
                    print(f"No grades found for course ID: {course_id}")
            else:
                print("Invalid choice. Please try again.")

    def check_my_marks(self):
        if not self.courses:
            print("No marks found.")
            return
        
        while True:
            print("1. Check marks for all courses you took.")
            print("2. Check marks for a specific course you took.")
            choice = input("Enter you choice: ").strip()
            if choice == "1":
                print(f"Grades for {self.first_name} {self.last_name}:")
                for course in self.courses:
                    print(f"  Course ID: {course['course_id']}, Grade: {course['grade']}, Mark: {course['mark']}")

            elif choice == "2":
                course_id = input("Enter the course ID: ").strip()
                for course in self.courses:
                    if course["course_id"] == course_id:
                        print(f"Course ID: {course['course_id']}, Grade: {course['grade']}, Mark: {course['mark']}")
                        return
                    print(f"No grades found for course ID: {course_id}")
            else:
                print("Invalid choice. Please try again.")

    def add_new_student(self):
        student_id = input("Enter the new student's student ID: ").strip()
        first_name = input("Enter the new student's first name: ").strip()
        last_name = input("Enter the new student's last name: ").strip()
        course_id = input("Enter the course ID the new student took: ").strip()
        grade = input("Enter the grade of the course for the new student: ").strip()
        mark = float(input("Enter the mark of the course for the new student: ").strip())
        
        if student_id not in students:
            students[student_id] = Student(student_id, first_name, last_name)
            students[student_id].add_course(course_id, grade, mark)
            print(f"New student {first_name} {last_name} added successfully.")
        else:
            print(f"Student ID: {student_id} already exists.")

    def delete_new_student(self):
        student_id = input("Enter the student ID of the student you want to delete: ").strip()
        if student_id in students:
            del students[student_id]
            print(f"Student ID: {student_id} deleted successfully.")
        else:
            print(f"Student ID: {student_id} not found.")

    def update_student_record(self):
        #可以更新姓名、课程或成绩
        student_id = input("Enter the student ID of the student you want to update: ").strip()
        if student_id in students:
            student = students[student_id]
            print("1. Update student's frist name.")
            print("2. Update student's last name.")
            print("3. Update student's course ID.")
            print("4. Update student's grade.") # 只有教授可以改分数
            print("5. Update student's mark.") # 只有教授可以改分数
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                new_first_name = input("Enter the new first name: ").strip()
                student.first_name = new_first_name
                print("First name updated successfully.")
            elif choice == "2":
                new_last_name = input("Enter the new last name: ").strip()
                student.last_name = new_last_name
                print("Last name updated successfully.")
            elif choice == "3":
                course_id = input("Enter the course ID you want to update: ").strip()
                new_course_id = input("Enter the new course ID: ").strip()
                for course in student.courses:
                    if course["course_id"] == course_id:
                        course["course_id"] = new_course_id
                        print("Course ID updated successfully.")
                        return
                print(f"Course ID: {course_id} not found.")
            elif choice == "4":
                course_id = input("Enter the course ID you want to update: ").strip()
                new_grade = input("Enter the new grade: ").strip()
                for course in student.courses:
                    if course["course_id"] == course_id:
                        course["grade"] = new_grade
                        print("Grade updated successfully.")
                        return
                print(f"Course ID: {course_id} not found.")
            elif choice == "5":
                course_id = input("Enter the course ID you want to update: ").strip()
                new_mark = float(input("Enter the new mark: ").strip())
                for course in student.courses:
                    if course["course_id"] == course_id:
                        course["mark"] = new_mark
                        print("Mark updated successfully.")
                        return
                print(f"Course ID: {course_id} not found.")
            else:
                print("Invalid choice. Please try again.")
        else:
            print(f"Student ID: {student_id} not found.")

    def save_students_to_csv(self, filename):
        with open(filename, mode="w", newline="") as student_file:
            writer = csv.writer(student_file)
            writer.writerow(["Student ID", "First Name", "Last Name", "Course ID", "Grade", "Mark"])
            for student_id, student in students.items():
                for course in student.courses:
                    writer.writerow(student.student_id, student.first_name, student.last_name, course["course_id"], course["grade"], course["mark"])

##### Read the Student File ######
def load_student_data():
    """  Load student data from the CSV file into the students dictionary """
    with open("Student.csv", mode = "r") as student_file:
        reader = csv.reader(student_file)
        next(reader) # Skip the header row
        for row in reader:
            student_id, first_name, last_name, course_id = row

            # if student not in students, create new Student object
            if student_id not in students:
                students[student_id] = Student(student_id, first_name, last_name)
            
            # Add course and grades
            students[student_id].add_course(course_id)

# Load student data when the module is imported
load_student_data()