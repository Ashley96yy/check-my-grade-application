import csv
import time
from course import Course, courses # Import the Course class and the courses dictionary

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

    def display_all_professors_records(self, sort_by="professor_id"):
        """ Display all the professors details, sorted by specific field
        Parameters:
            sorted_by (str): The field to sort the professor by
            -- Options: "student_id", "name"
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
            professors_list.sort(key=lambda x: x.professor_id)
        elif sort_by == "name":
            professors_list.sort(key=lambda x: x.name)
        
        # Display the sorted professors
        print(f"\nDisplaying all professors records (sorted by {sort_by}):")
        for professor in professors_list:
            print(f"Professor ID: {professor.professor_id}, Name: {professor.name}, Rank: {professor.rank}")
            for course in professor.courses:
                print(f"  Course ID: {course['course_id']}")
            print("-" * 30)
    
    def display_chosen_professor_records(self):
        """ Display the chosen professor's details and measure lookup time"""
        professor_id = input("Enter the professor ID: ").strip()
        start_time = time.time() # Record the start time

        if professor_id in professors: # Check if the professor ID exists
            professor = professors[professor_id]
            print(f"\nProfessor ID: {professor.professor_id}, Name: {professor.name}, Rank: {professor.rank}")
            for course in professor.courses:
                print(f"  Course ID: {course['course_id']}")
        else:
            print(f"Professor ID: {professor_id} not found.")

        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time # Calculate the elapsed time
        print(f"Time taken to lookup the professor: {elapsed_time:.6f} seconds")

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
        invalid_course_ids = [cid for cid in new_course_id_str if cid not in courses]
        if invalid_course_ids:
            print(f"The following course IDs do not exist: {', '.join(invalid_course_ids)}")
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

    def modify_professor_details(self):
        """ Delete a professor and his/her related course data from all files """
        professor_id = input("Enter the professor ID to modify: ").strip()
        if professor_id in professors:
            professor = professors[professor_id]
            print("1. Modify professor name")
            print("2. Modify professor rank")
            print("3. Modify course IDs")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                new_name = input("Enter the new name: ").strip()
                professor.name = new_name
                print("Name updated successfully.")
            elif choice == "2":
                new_rank = input("Enter the new rank: ").strip()
                professor.rank = new_rank
                print("Rank updated successfully.")
            elif choice == "3":
                new_course_id_str = input("Enter the new course IDs (comma-separated): ")
                professor.courses = [] # Clear existing courses
                professor.add_course(new_course_id_str)
                print("Course IDs updated successfully.")
            else:
                print("Invalid choice, please enter again.")
            
            # Save the data to CSV file
            Professor.save_professors_to_csv("Professor.csv")
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