import csv
import time
from professor import professors

##### Initialize data ######
# Use a dictionary (hash table) to store all the courses
courses = {}

##### Class Course #####
class Course:
   
    def __init__(self, course_id, course_name, description):
        self.course_id = course_id # Unique course ID
        self.course_name = course_name # Course name
        self.description = description # Course description
        
    def display_all_courses_records(self, sort_by="course_id"):
        """ Display all the courses details, sorted by specific field
        Parameters:
            sorted_by (str): The field to sort the course by
            -- Options: "course_id", "course_name"
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
            courses_list.sort(key=lambda x: x.course_id)
        elif sort_by == "course_name":
            courses_list.sort(key=lambda x: x.course_name)
        
        # Display the sorted courses
        print(f"\nDisplaying all courses records (sorted by {sort_by}):")
        for course in courses_list:
            print(f"Course ID: {course.course_id}, Course Name: {course.course_name}, Description: {course.description}")
            print("-" * 30)
        
    def display_chosen_course_records(self):
        """ Display the chosen course's details and measure lookup time"""
        course_id = input("Enter the course ID: ").strip()
        start_time = time.time() # Record the start time

        if course_id in courses: # Check if the course ID exists
            course = courses[course_id]
            print(f"Course ID: {course.course_id}, Course Name: {course.course_name}, Description: {course.description}")
        else:
            print(f"Course ID {course_id} not found.")
        
        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time
        print(f"Time taken to loopuo the course: {elapsed_time:.6f} seconds")
    
    def display_course_taught_by_professor_records(self, email_id):
        """ Display the courses taught by the professor"""
        professor_id = email_id
        professor_course_ids = professors[professor_id].courses
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
            if modify_course_id not in professor.courses:
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
        professor.courses.append(course_id)

        # Save the new course data to Course.csv
        with open("Course.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([course_id, course_name, description])

        # Update the professor's data in professors.csv
        with open("professors.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Find the professor and update their courses
        for row in rows:
            if row[0] == email_id:  # Assuming email_id is the first column
                row[3] = ",".join(professor.courses)  # Assuming courses are stored in the 4th column
                break

        # Write the updated data back to professors.csv
        with open("professors.csv", mode="w", newline="") as file:
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
            if course_id not in professor.courses:
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



