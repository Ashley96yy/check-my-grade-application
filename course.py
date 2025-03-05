import csv
import time

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

    def modify_course(self):
        """ Modify course by the professor """
        global course_data
        modify_course_id = input("Enter the course ID (letters + numbers) you want to modify: ").strip().upper()
        print(modify_course_id)
        modify_course_data = course_data[course_data.Course_id == modify_course_id]

        # Check if course exists
        if modify_course_data.empty:
            print(f"No data found for the course {modify_course_id}.")
            return
        
        else:
            print("Below is the details of the course to be modified:")
            print(tabulate(modify_course_data, headers='keys', tablefmt='pretty'))
            print("\n")
            print("1. Modify course ID")
            print("2. Modify course name")
            print("3. Modify the description of the course")
            choice = input("Enter your choice: ")
            if choice == "1":
                course_id_modified = input("Enter the course ID to be modified: ").strip().upper()

                # Modify course_id (Primary Key) info in Course.CSV file
                course_data.loc[course_data.Course_id == modify_course_id, "Course_id"] = course_id_modified
                course_data.to_csv("Course.csv", index=False)

                # Modify course_id (Foreign Key) info in Student.CSV file
                student_data.loc[student_data.Course_id == modify_course_id, "Course_id"] = course_id_modified
                student_data.to_csv("Student.csv", index=False)

                # Modify course_id (Foreign Key) info in Professor.CSV file
                professor_data.loc[professor_data.Course_id == modify_course_id, "Course_id"] = course_id_modified
                professor_data.to_csv("Professor.csv", index=False)

                print(f"Convert {modify_course_id} to {course_id_modified}.\nModify course ID successfully.")
            
            elif choice == "2":
                course_name_modified = input("Enter the course name to be modified: ").strip()
                original_course_name = course_data[course_data.Course_id == modify_course_id]["Course_name"].values[0]

                # Modify course name info in Course.CSV file
                course_data.loc[course_data.Course_id == modify_course_id, "Course_name"] = course_name_modified
                course_data.to_csv("Course.csv", index=False)

                print(f"Convert {original_course_name} to {course_name_modified}.\nModify course name successfully.")
            
            elif choice == "3":
                course_description_modified = input("Enter the description of the course which is to be modified: ").strip()
                original_course_description = course_data[course_data.Course_id == modify_course_id["Description"]].values[0]

                # Modify the description of the course in Course.CSV file
                course_data.loc[course_data.Course_id == modify_course_id, "Description"] == course_description_modified
                course_data.to_csv("Course.csv", index=False)

                print(f"Convert {original_course_description} to {course_description_modified}.\nModify the description of the course successfully.")

    def add_new_course(self):
        """ Add new course by the professor """
        global course_data
        course_id = capitalize_letters(input("Enter the new course ID (letters + numbers): ").strip())
        course_name = input("Enter the new course name: ").strip().title()
        description = input("Enter the description of the course: ").strip().capitalize()

        # check if course_id exists
        if course_id in course_data.Course_id.to_list():
            print("Course ID already exists.")
        else:
            # Add a new row
            new_course = pandas.DataFrame({
                "Course_id": [course_id],
                "Course_name": [course_name],
                "Description": [description]
            })
            # Add new data into the existing DataFrame
            course_data = pandas.concat([course_data, new_course], ignore_index=True)
            # Save to CSV file
            course_data.to_csv("Course.csv", index=False)
            print("New course added successfully!")
        
    def delete_course(self):
        """ Delete new course by the professor """
        global course_data 
        deleted_course_file = Path("deleted_Course.csv")

        course_id = capitalize_letters(input("Enter the new course ID (letters + numbers): ").strip())
        course_deleted = course_data[course_data.Course_id == course_id]
        
        # Check if course exists
        if course_deleted.empty:
            print(f"No data found for the deleted course {course_id}.")
            return
        
        else:
            # Check if the deleted_course_file exists
            if deleted_course_file.exists():
                deleted_course_data = pandas.read_csv("deleted_Course.csv")
                deleted_course_data = pandas.concat([deleted_course_data, course_deleted]).drop_duplicates()
            
            else:
                # If there is no the deleted_course_file, use course_deleted data to create a new DataFrame
                deleted_course_data = course_deleted

            # Save the deleted course to the CSV file
            deleted_course_data.to_csv("deleted_Course.csv", index=False)

            # Remove the deleted course from the original file
            course_data = course_data[course_data.Course_id != course_id]
            # Save to CSV file
            course_data.to_csv("Course.csv", index=False)

            print(f"The data of {course_id} has been deleted successfully!"
                        f"\nThe data of {course_id} saved to 'deleted_course_file.csv'.")


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



