from login_user import LoginUser
from course import Course, courses # Import the Course class and the courses dictionary
from student import Student, students # Import the Student class and the students dictionary
from professor import Professor, professors # Import the Professor class and the professors dictionary
from grades import Grades
import getpass
import shutil

def main_menu():

    while True:
        columns = shutil.get_terminal_size().columns
        print("=================================".center(columns))
        print("Welcome to CheckMyGrade APP!".center(columns))
        print("================================".center(columns))
        email_id = input("Enter your Email ID: ").strip()
        password = getpass.getpass("Enter you password: ")
        login = LoginUser(email_id, password)
        status, role = login.login()

        if not status:
            print("Login failed. Please try again.")
            continue
        
        # Main menu after successful login
        while True:
            print("\n")
            print("1. Go to main menu")
            print("2. Change password")
            print("3. Logout")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                if role == "admin":
                    admin_menu()
                elif role == "professor":
                    pass
                    # professor_menu(professor, grades)
                elif role == "student":
                    pass
                    # student_menu(student, grades)
            elif choice == "2":
                login.change_password()    
            elif choice == "3":
                login.logout()
                break
            else:
                print("Invalid choice, please enter again.") 

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Display Student Records")
        print("2. Display Professor Records")#sort
        print("3. Display Course Records")#sort
        print("4. Display Grades Records")#sort
        print("5. Add/Delete/Modify Student")
        print("6. Add/Delete/Modify Professor")
        print("7. Add/Delete/Modify Course")
        print("8. Add/Delete/Modify Grades")
        print("9. Generate Grade Report")
        print("10. Return to main menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n Display Student Records Menu:")
            print("1. Display all students details")
            print("2. Display chosen student details")
            print("3. Return to previous menu")
            sub_choice = input("Enter your choice: ").strip()

            if sub_choice == "1":
                sort_by = input("Enter the sort by (student_id, first_name, last_name): ").strip()
                students[list(students.keys())[0]].display_all_students_records(sort_by)

            elif sub_choice == "2":
                students[list(students.keys())[0]].display_chosen_student_records()

            elif sub_choice == "3":
                continue # Return to previous menu

            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "2": 
            print("\n Display Professor Records Menu:")
            print("1. Display all professors details")
            print("2. Display chosen professor details")
            print("3. Return to previous menu")
            sub_choice = input("Enter your choice: ").strip()

            if sub_choice == "1":
                sort_by = input("Enter the sort by (professor_id, name): ").strip()
                professors[list(professors.keys())[0]].display_all_professors_records(sort_by)

            elif sub_choice == "2":
                professors[list(professors.keys())[0]].display_chosen_professor_records()

            elif sub_choice == "3":
                continue # Return to previous menu
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "3": #sort
            print("\n Display Course Records Menu:")
            print("1. Display all courses details")
            print("2. Display chosen course details")
            print("3. Return to previous menu")
            sub_choice = input("Enter your choice: ").strip()

            if sub_choice == "1":
                sort_by = input("Enter the sort by (course_id, course_name): ").strip()
                courses[list(courses.keys())[0]].display_all_courses_records(sort_by)

            elif sub_choice == "2":
                courses[list(courses.keys())[0]].display_chosen_course_records()

            elif sub_choice == "3":
                continue # Return to previous menu
            
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "4": #sort
            print("\n Display Grades Records Menu:")
            print("1. Display all grades details")
            print("2. Display chosen grade details")
            print("3. Return to previous menu")
            sub_choice = input("Enter your choice: ").strip()

            if sub_choice == "1":
                pass
            elif sub_choice == "2":
                pass
            elif sub_choice == "3":
                break
            else:
                print("Invalid choice, please enter again.")

        elif choice == "5":
            print("\n Add/Delete/Modify Student Menu:")
            print("1. Add new student")
            print("2. Delete student")
            print("3. Modify student details")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass#修改学生iD，姓名，课程
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "6":
            print("\n Add/Delete/Modify Professor Menu:")
            print("1. Add new professor")
            print("2. Delete professor")
            print("3. Modify professor details")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass#修改教授ID，姓名，课程，职称，课程需确认是否在课程列表中
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "7":
            print("\n Add/Delete/Modify Course Menu:")
            print("1. Add new course")
            print("2. Delete course")
            print("3. Modify course details")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass#修改课程ID，名称，描述
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "8":#需要输入学生ID，课程ID
            print("\n Add/Delete/Modify Grades Menu:")
            print("1. Add new grade")#添加grade和mark
            print("2. Delete grade")
            print("3. Modify grade details")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "9":#展示成绩的同时，还需要统计所选课程数量、平均分，中位数、学生数量、最高分、最低分
            print("\n Generate Grade Report Menu:")
            print("1. Generate grade report for a student")
            print("2. Generate grade report for a professor")
            print("3. Generate grade report for a course")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "10":
            break

        else:
            print("Invalid choice, please enter again.")

def professor_menu():
    while True:
        print("\nProfessor Menu:")
        print("1. Display Professor Records")
        print("2. Display Course Records")
        print("3. Display Grades Records")
        print("4. Display Student Records")
        print("5. Modify My Details") #只能修改教授自己的个人信息
        print("6. Add/Delete/Modify Course")
        print("7. Add/Delete/Modify Grades")
        print("8. Generate Grade Report") #查看自己教授课程的成绩，分为全部课程和特定课程
        print("9. Return to main menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n Display Professor Records Menu:")
            print("1. Display my details")
            print("2. Display all professors details")#sort
            print("3. Display chosen professor details")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "2":#sort
            print("\n Display Course Records Menu:")
            print("1. Display the details of all courses which I teach")
            print("2. Display all courses details")
            print("3. Display chosen course details")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                break
            else:  
                print("Invalid choice, please enter again.")
        
        elif choice == "3":#sort
            print("\n Display Grades Records Menu:")
            print("1. Display the grades of all courses which I teach")
            print("2. Display the grades of chosen course which I teach")
            print("3. Return to previous menu")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                pass
            elif choice == "2":
                #课程ID，学生ID，grade，mark
                print("1. Display Average Mark")
                print("2. Display Median Mark")
                print("3. Display Highest Mark")
                print("4. Display Lowest Mark")
                print("5. Return to previous menu")
                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    pass
                elif choice == "2":
                    pass
                elif choice == "3":
                    pass
                elif choice == "4":
                    pass
                elif choice == "5":
                    pass
                else:
                    print("Invalid choice, please enter again.")
            elif choice == "3":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "4":#sort
            print("\n Display Student Records Menu:")
            print("1. Display the details of all students in my courses")
            print("2. Display all students details")
            print("3. Display chosen student details")
            print("4. Return to previous menu")
            sub_choice = input("Enter your choice: ").strip()

            if sub_choice == "1":
                pass

            elif sub_choice == "2":
                sort_by = input("Enter the sort by (student_id, first_name, last_name): ").strip()
                students[list(students.keys())[0]].display_all_students_records(sort_by)

            elif sub_choice == "3":
                students[list(students.keys())[0]].display_chosen_student_records()

            elif sub_choice == "4":
                continue # Return to previous menu

            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "5":
            pass

        elif choice == "6": #只能删除、修改自己教授的课程,一旦教授增加课程，代表默认上该课程
            print("\n Add/Delete/Modify Course Menu:")
            print("1. Add new course")
            print("2. Delete course")
            print("3. Modify course details")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass#修改课程ID，名称，描述
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "7":#需要输入学生ID，课程ID，需要注意是否有权限修改
            print("\n Add/Delete/Modify Grades Menu:")
            print("1. Add new grade")
            print("2. Delete grade")
            print("3. Modify grade details")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter again.")
        
        elif choice == "8":
            print("\n Generate Grade Report Menu:")
            print("1. Generate grade report for all my courses")
            print("2. Generate grade report for a specific course I taught")
            print("3. Return to previous menu")
        
        elif choice == "9":
            break

        else:
            print("Invalid choice, please enter again.")

def student_menu():
    while True:
        print("\nStudent Menu:")
        print("1. Display My Records")#显示学生的基本信息,不包括成绩
        print("2. Modify My Details")#只能修改自己的基本信息,不包括课程、成绩,课程因为已经获取分数，并不能增删
        print("3. Check My Grades")
        print("4. Check My Marks")
        print("5. Generate My Grade Report")#报告需展示学生平均分、最高分、最低分
        print("6. Discover Courses") #展示所有课程或者输入课程ID查看课程详情
        print("7. Discover Professors") #展示所有教授或者输入教授ID查看教授详情
        print("8. Return to main menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            pass

        elif choice == "2":
            pass

        elif choice == "3":
            pass

        elif choice == "4":
            pass

        elif choice == "5":
            pass

        elif choice == "6":
            print("\n Discover Courses Menu:")
            print("1. Display all courses")
            print("2. Display chosen course details")
            print("3. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                break
            else:
                print("Invalid choice, please enter again.")

        elif choice == "7":
            print("\n Discover Professors Menu:")
            print("1. Display all professors")
            print("2. Display chosen professor details")
            print("3. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                break
            else:
                print("Invalid choice, please enter again.")

        elif choice == "8":
            break

        else:
            print("Invalid choice, please enter again.")


if __name__ == "__main__":
    main_menu()