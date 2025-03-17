import faker
import string
import random
import csv
from encdyc import TextSecurity

# Set random seed for reproducibility
random.seed(42)  # You can use any integer value as the seed

##### Course Information #####
# Function to generate sequential course IDs
def generate_sequential_course_id(start, count, prefix="DATA"):
    return [f"{prefix}{start + i}" for i in range(count)]

# Generate random course names and descriptions
def generate_course_name_description():
    fake_courses = [
        ("Introduction to Artificial Intelligence", "Learn the basics of AI and machine learning."),
        ("Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming."),
        ("Software Engineering Principles", "Explore software development processes and methodologies."),
        ("Database Systems", "Discover database design and SQL for managing data."),
        ("Cybersecurity Basics", "Learn about security measures to protect data and systems."),
        ("Cloud Computing", "Understand the basics of cloud infrastructure and services."),
        ("Web Development", "Learn to build modern web applications with HTML, CSS, and JavaScript."),
        ("Mobile App Development", "Explore techniques for creating mobile applications."),
        ("Game Development", "Learn to design and develop video games."),
        ("Big Data Analytics", "Understand tools and techniques for analyzing large datasets."),
        ("Digital Marketing", "Learn online marketing strategies and analytics."),
        ("Project Management", "Master project planning and execution techniques."),
        ("Human-Computer Interaction", "Explore design principles for user interfaces."),
        ("Operating Systems", "Understand the principles and functions of operating systems."),
        ("Computer Networks", "Learn about network protocols and architectures."),
        ("Machine Learning", "Discover advanced techniques in supervised and unsupervised learning."),
        ("Quantum Computing", "An introduction to the principles of quantum computing."),
        ("Ethical Hacking", "Learn ethical hacking techniques to test and secure systems."),
        ("Blockchain Technology", "Explore the fundamentals of blockchain and its applications."),
        ("Robotics", "Learn the basics of robot design and programming."),
    ]
    return fake_courses

# Generate sequential courses and save to CSV
def save_courses_to_csv(filename, start_id, num_courses, prefix="DATA"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Course_id", "Course_name", "Description"])
        
        # Generate sequential course IDs
        course_ids = generate_sequential_course_id(start_id, num_courses, prefix)
        course_details = generate_course_name_description()
        
        for i in range(num_courses):
            course_id = course_ids[i]
            # Rotate through course details if more than available
            course_name, course_description = course_details[i % len(course_details)]
            writer.writerow([course_id, course_name, course_description])

# Save 20 courses starting from DATA200 to courses.csv
save_courses_to_csv("Course.csv", 200, 20, "DATA")
print("Courses saved to 'Course.csv'")

##### User Information #####
# Function to generate a random password
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))

# Roles and their respective counts
roles = {
    "admin": 5,
    "professor": 10,
    "student": 1100
}

# Initialize Faker instance
fake = faker.Faker()

# Set Faker seed for reproducibility using class method
faker.Faker.seed(42)  # Use the class method to set the seed

# Prepare data to be written to CSV
data = []
data_encrypted = []

for role, count in roles.items():
    for _ in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@myscu.edu"
        password = generate_random_password(12)
        password_encrypted = TextSecurity(5).encrypt(password)  # Encrypt the password
        data.append([email, password, role])
        data_encrypted.append([email, password_encrypted, role])

# Write data to Login_decrypted.csv
with open("Login_decrypted.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["User_id", "Password", "Role"])
    # Write data rows
    writer.writerows(data)
print("User information saved to 'Login_decrypted.csv'")

# Write data to Login.csv
with open("Login.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["User_id", "Password", "Role"])
    # Write data rows
    writer.writerows(data_encrypted)
print("User information saved to 'Login.csv'")

##### Student Information #####
# Function to assign random course IDs to students, ensuring each student has at least one course
def assign_courses_to_students(num_students, course_ids, min_students_per_course=20, min_courses=1, max_courses=5):
    student_courses = [[] for _ in range(num_students)]  # List to store courses for each student
    course_student_counts = {course_id: 0 for course_id in course_ids}  # Track how many students are assigned to each course
    
    # Ensure each student has at least one course
    for student_index in range(num_students):
        # Randomly assign at least one course to each student
        course_id = random.choice(course_ids)
        student_courses[student_index].append(course_id)
        course_student_counts[course_id] += 1
    
    # Ensure each course has at least `min_students_per_course` students
    for course_id in course_ids:
        while course_student_counts[course_id] < min_students_per_course:
            # Find a student who hasn't been assigned this course yet
            student_index = random.randint(0, num_students - 1)
            if course_id not in student_courses[student_index]:
                student_courses[student_index].append(course_id)
                course_student_counts[course_id] += 1
    
    # Assign additional courses to students
    for student_index in range(num_students):
        # Randomly decide how many additional courses this student will take
        num_additional = random.randint(min_courses - 1, max_courses - 1)
        # Randomly select additional courses
        additional_courses = random.sample(course_ids, min(num_additional, len(course_ids)))
        for course_id in additional_courses:
            if course_id not in student_courses[student_index]:
                student_courses[student_index].append(course_id)
                course_student_counts[course_id] += 1
    
    return student_courses

# Generate course IDs (assuming 20 courses starting from DATA200)
course_ids = generate_sequential_course_id(200, 20, "DATA")

# Assign courses to students
student_courses = assign_courses_to_students(roles["student"], course_ids, min_students_per_course=20)

# Prepare data for Student.csv
student_data = []
student_index = 0  # Separate index for student_courses
for i, user in enumerate(data):
    if user[2] == "student":  # Only consider students
        email = user[0]
        first_name = email.split(".")[0].capitalize()  # Extract first name from email
        last_name = email.split(".")[1].split("@")[0].capitalize()  # Extract last name from email
        assigned_courses = student_courses[student_index]  # Use student_index to access student_courses
        # Join assigned course IDs with a comma
        course_id_str = ", ".join(assigned_courses)
        student_data.append([email, first_name, last_name, course_id_str])
        student_index += 1  # Increment student_index

# Write data to Student.csv
with open("Student.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Email_address", "First_name", "Last_name", "Course_ids"])
    # Write data rows
    writer.writerows(student_data)
print("Student information saved to 'Student.csv'")

##### Professor Information #####
# Define professor ranks
professor_ranks = ["Assistant Professor", "Associate Professor", "Senior Professor"]

# Function to assign courses to professors, ensuring each course is taught by only one professor
def assign_courses_to_professors(num_professors, course_ids, min_courses=1, max_courses=3):
    professor_courses = [[] for _ in range(num_professors)]  # List to store courses for each professor
    all_courses = course_ids.copy()  # Create a copy of course_ids
    random.shuffle(all_courses)  # Shuffle the courses to assign them randomly

    # Assign at least one course to each professor
    for i in range(num_professors):
        if all_courses:
            assigned_course = all_courses.pop()  # Assign one course
            professor_courses[i].append(assigned_course)
        else:
            break  # No more courses to assign

    # Assign additional courses to professors
    for i in range(num_professors):
        # Randomly decide how many additional courses this professor will teach
        num_additional = random.randint(min_courses - 1, max_courses - 1)
        # Randomly select additional courses from the remaining courses
        additional_courses = random.sample(all_courses, min(num_additional, len(all_courses)))
        professor_courses[i].extend(additional_courses)
        # Remove the assigned courses from the pool of available courses
        for course in additional_courses:
            all_courses.remove(course)

    return professor_courses

# Assign courses to professors
professor_courses = assign_courses_to_professors(roles["professor"], course_ids)

# Prepare data for Professor.csv
professor_data = []
professor_index = 0  # Separate index for professor_courses
for i, user in enumerate(data):
    if user[2] == "professor":  # Only consider professors
        email = user[0]
        first_name = email.split(".")[0].capitalize()  # Extract first name from email
        last_name = email.split(".")[1].split("@")[0].capitalize()  # Extract last name from email
        rank = random.choice(professor_ranks)  # Randomly assign a rank
        assigned_courses = professor_courses[professor_index]  # Use professor_index to access professor_courses
        # Join assigned course IDs with a comma
        course_id_str = ", ".join(assigned_courses)
        professor_data.append([email, f"{first_name} {last_name}", rank, course_id_str])
        professor_index += 1  # Increment professor_index

# Write data to Professor.csv
with open("Professor.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Professor_id", "Professor_Name", "Rank", "Course_id"])
    # Write data rows
    writer.writerows(professor_data)
print("Professor information saved to 'Professor.csv'")

##### Grades Information #####
# Function to generate a grade based on the mark
def generate_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"

# Read Student.csv and extract email and course IDs
student_data = []
with open("Student.csv", mode="r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        email = row[0]
        course_ids = row[3].split(", ")  # Split course IDs into a list
        for course_id in course_ids:
            student_data.append([email, course_id])

# Calculate the maximum allowed number of F grades (5% of total students)
num_students = len(student_data)
max_f_count = int(num_students * 0.05)  # 5% of total students
current_f_count = 0  # Track the number of F grades assigned

# Generate random marks and grades
grades_data = []
for email, course_id in student_data:
    # If F count has reached the limit, generate a mark >= 60
    if current_f_count >= max_f_count:
        mark = random.randint(60, 100)  # Ensure mark is >= 60
    else:
        mark = random.randint(0, 100)  # Random mark between 0 and 100
    
    grade = generate_grade(mark)  # Generate grade based on mark
    
    # Update F count if the grade is F
    if grade == "F":
        current_f_count += 1
    
    grades_data.append([email, course_id, grade, mark])

# Write data to Grades.csv
with open("Grades.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Email_address", "Course_id", "Grades", "Marks"])
    # Write data rows
    writer.writerows(grades_data)

print(f"Grades saved to 'Grades.csv'. Total F grades: {current_f_count} (<= {max_f_count} allowed)")