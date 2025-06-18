import json

students = []
def sort_students():
    global sorted_students
    sorted_students = sorted(students, key=lambda student: student['name'])

admin_username = "sut.teacher"
admin_password = "1234567"

def save_file():
    file = open("students_file.json", "w")
    json.dump(students, file, indent=4)
    file.close()

def load_file():
    global students
    file = open("students_file.json", "r")
    students = json.load(file)
    file.close()

load_file()
sort_students()

def export_to_csv(choice):
    if choice == "1":
        file= open("all_students.csv", "w") 
        file.write("Student Name, Student ID, Courses: Grades\n")
        for student in sorted_students:
            courses = "; ".join([f"{course}: {details['grade']}" for course, details in student["courses"].items()])
            file.write(f"{student['name']}, {student['id']}, {courses}\n")
        print("All students' data exported to 'all_students.csv' successfully."),print("all_students.csv")
    elif choice == "2":
        student_id = input("\n-Enter student ID: ").strip()
        file = open("student_data.csv", "w")
        for student in students:
            if student["id"] == student_id:
                file.write("Student Name, Student ID, Courses: Grades\n")
                courses = "; ".join([f"{course}: {details['grade']}" for course, details in student["courses"].items()])
                file.write(f"{student['name']}, {student['id']}, {courses}\n")
                break 
            else:
                pass 
        file.close()
        file= open("student_data.csv", "r")
        if  file.read(1):
            print(f"Data for student ID {student_id} exported to 'student_data.csv' successfully."),print("student_data.csv")
        else:
             print(f"Student ID {student_id} not found.")  
        file.close()
    elif choice == "3":
        course_name = input("\n-Enter course name: ").strip().lower()
        file = open("course_data.csv", "w")
        for student in sorted_students:
            if course_name in student["courses"]:
                file.write("Student Name, Student ID, Grade\n")
                grade = student["courses"][course_name]["grade"]
                file.write(f"{student['name']}, {student['id']}, {grade}\n")
            else:
                pass
        file.close()
        file= open("course_data.csv", "r")
        if  file.read(1):
             print(f"Data for course '{course_name}' exported to 'course_data.csv' successfully."),print("course_data.csv")
        else:
            print(f"Course '{course_name}' does not exist for any student.")
        file.close()

    else:
        print("Invalid choice.")


def edit_students():
    while True:
        print("________________\nWhat do you want to edit in students?")
        print("1. Add student")
        print("2. Delete student")
        print("3. Back")
        choice4 = input("Enter your choice: ").strip()
        if choice4 == "1":
            student_id = input("---------\n-Enter student ID: ").strip()
            if not (len(student_id) == 9 and student_id.isdigit()):
                print("*Invalid ID. Student ID must contain only 9 numbers.")
                continue
            for student in students:
                if student["id"] == student_id:
                    print("Student already exists.")
                    x = input("Do you want to update this student (True or False)? ").strip().lower()
                    if x == "true":
                        new_name = input("Enter New name: ").strip().lower()
                        if not(new_name and new_name.replace(" ", "").isalpha()):
                            print("*Invalid name. The name must contain only letters and cannot be empty.")
                            continue
                        student["name"] = new_name
                        print("....Student updated successfully!\n----------------")
                        save_file()
                        sort_students()
                    break
            else:
                name = input("Enter student name: ").strip().lower()
                if not(name and name.replace(" ", "").isalpha()):
                    print("Invalid name. The name must contain only letters and cannot be empty.")
                    continue
                student = {"name": name, "id": student_id, "courses": {}}
                students.append(student)
                sort_students()
                save_file()
                print(f"\n....Student {name} added successfully.\n----------------")
        elif choice4 == "2":
            student_id = input("\n-Enter student ID: ").strip()
            for student in students:
                if student["id"] == student_id:
                    students.remove(student)
                    print(f"....Student with id={student_id} deleted successfully.\n----------------")
                    sort_students()
                    save_file()
                    break 
            else:
                print("*Student does not exist.")
        elif choice4 == "3":
            break
        else:
            print("*Invalid input. Try again.")


def add_courses():
    course_name = input("Enter course name: ").strip().lower()
    if not course_name:
        print("*Invalid course name. Course name cannot be empty.")
        return
    credit_hours = int(input(f"Enter the credit hours for '{course_name}': ").strip())
    if credit_hours <= 0:
        print("Credit hours must be a positive integer.")
        return
    while True:
        print("\nChoose students to add this course:")
        print("0. Add to all students")
        index = 1 
        for student in sorted_students:
            print(f"{index}. {student['name']} (ID: {student['id']})")
            index += 1  
        choice = input("-Enter choice(or 'end' to end adding course): ").strip().lower()
        if choice == "0":
            for student in students:
                if course_name not in student["courses"]:
                    student["courses"][course_name] = {"grade": None, "credit_hours": credit_hours}
            save_file()
            print(f"Course {course_name} added to all students.\n----------------")
            break
        elif choice == "end":
            print("Exiting the course adding process....\n----------------")
            break
        else:
            if choice.isdigit() and 1 <= int(choice) <= len(students):
                student = sorted_students[int(choice) - 1]
                if course_name not in student["courses"]:
                    student["courses"][course_name] = {"grade": None, "credit_hours": credit_hours} 
                    save_file()
                    sort_students()
                    print(f"...Course {course_name} added successfully to {student['name']}.\n________________")
                else:
                    print(f"Course {course_name} already exists for {student['name']}.\n________________")
            else:
                print("*Invalid input. Please enter a valid student choice.")


def update_courses():
    course_name = input("Enter course name: ").strip().lower()
    new_name = input("Enter new course name: ").strip().lower()
    if not new_name:
        print("*Invalid course name. Course name cannot be empty.")
        return
    students_with_course = [student for student in students if course_name in student["courses"]]
    if not students_with_course:
        print(f"Course '{course_name}' does not exist for any student.\n----------------")
        return
    for student in students_with_course:
        student["courses"][new_name] = student["courses"].pop(course_name)

    save_file()  
    print(f"...Course '{course_name}' updated to '{new_name}' successfully for {len(students_with_course)} students.\n----------------")
    

def delete_courses():
    course_name = input("Enter the course name to delete: ").strip().lower()
    if not course_name:
        print("*Invalid course name. Course name cannot be empty.")
        return
    while True:  
        print("\nChoose students to remove this course:")
        print("0. Remove from all students")
        index = 1
        for student in sorted_students:
            if course_name in student["courses"]:
                print(f"{index}. {student['name']} (ID: {student['id']})")
            index += 1

        choice = input("-Enter choice (or 'end' to end deleting course): ").strip().lower()
        if choice == "0":
            for student in students:
                if course_name in student["courses"]:
                    del student["courses"][course_name]  
            save_file()
            print(f"Course {course_name} removed from all students.\n----------------")
            break
        elif choice == "end":
            print("Exiting the course removal process...\n----------------")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(students):
            student = sorted_students[int(choice) - 1]
            if course_name in student["courses"]:
                del student["courses"][course_name]  
                save_file()
                sort_students()
                print(f"Course {course_name} removed from {student['name']}.\n________________")
            else:
                print(f"{student['name']} does not have this course.\n________________")
        else:
            print("*Invalid input. Please enter a valid student choice.")


def grade_to_points(grade):
    if grade >= 95:
        return 4.3
    elif grade >= 90:
        return 4.0
    elif grade >= 85:
        return 3.7
    elif grade >= 80:
        return 3.3
    elif grade >= 75:
        return 3.0
    elif grade >= 70:
        return 2.7
    elif grade >= 65:
        return 2.3
    elif grade >= 60:
        return 2.0
    elif grade >= 57:
        return 1.7
    elif grade >= 54:
        return 1.3
    elif grade >= 50:
        return 1.0
    else:
        return 0.0


def add_grades():
    student_id = input("Enter student ID: ").strip()
    if not (student_id.isdigit() and len(student_id) == 9):
        print("Invalid ID. Student ID must contain only 9 numbers")
        return
    for student in students:
        if student["id"] == student_id:
            course_name = input("Enter course name: ").strip().lower()
            if course_name in student["courses"]:
                grade = input(f"Enter {course_name} grade: ").strip()
                if not grade.replace('.', '').isdigit():
                    print("Invalid grade. Grade must be a number.")
                    return
                student["courses"][course_name]["grade"] = float(grade)
                save_file()
                print("Grade added successfully.")
                return
            else:
                print(f"*Course {course_name} doesn't exist.")
                return
    print("*Student ID not found.")


def calculate_GPA(student_id):
    for student in students:
        if student["id"] == student_id:
            total_points = 0
            total_credit_hours = 0 
            if not student["courses"]:
                print(f"Student {student['name']} has no registered courses.")
                return
            for course, details in student["courses"].items():
                grade = details["grade"]
                if grade is None:
                    print(f"Student {student['name']} has not graded for the course: {course}.")
                    continue
                grade_points = grade_to_points(grade)
                credit_hours = details["credit_hours"]
                total_points += grade_points * credit_hours
                total_credit_hours += credit_hours
            if total_credit_hours == 0:
                print(f"Student {student['name']} has no valid credit hours for GPA calculation.")
                return
            gpa = total_points / total_credit_hours
            print(f"GPA for {student['name']} is: {round(gpa, 2)}")
            return
    print(f"No student found with ID {student_id}.")


def passed_and_failed(student):
    pass_grade = 50.0
    passed_courses = []
    failed_courses = []
    for course, details in student["courses"].items():
        grade = details["grade"]
        if grade is not None: 
            if grade >= pass_grade:
                passed_courses.append(course)
            else:
                failed_courses.append(course)
        else:
            print(f"Course {course} not graded yet.")
    if passed_courses :
        print("Passed Courses:", passed_courses)
    else:
        print("No passed courses.")
    if failed_courses:
        print("Failed Courses:", failed_courses)
    else:
        print("No failed courses.")


def teacher_user():
    while True:
        print("\n  << Teacher Menu >>  ")
        print("1. Edit student")
        print("2. Add courses")
        print("3. Update courses")
        print("4. Delete courses")
        print("5. Add grades")
        print("6. Calculate GPA")
        print("7. Export data to CSV")
        print("8. Exit")
        choice2 = input("Enter your choice: ").strip()
        if choice2 == "1":
            edit_students()
        elif choice2 == "2":
            add_courses()
        elif choice2 == "3":
            update_courses()
        elif choice2 == "4":
            delete_courses()
        elif choice2 == "5":
            add_grades()
        elif choice2 == "6":
            id = input("\nEnter the student ID to calculate GPA: ").strip()
            calculate_GPA(id)
        elif choice2 == "7": 
             print("\nChoose export option:")
             print("1. Export all students' data")
             print("2. Export data for a specific student by ID")
             print("3. Export all grades for a specific course") 
             x=input("Enter your choice: ").strip()  
             export_to_csv(x)
        elif choice2 == "8":
            print("Exiting Teacher Menu...")
            break
        else:
            print("Invalid input. Please try again.")


def student_user():
    student_id = input("\nEnter your ID: ").strip()
    if not (len(student_id) == 9 and student_id.isdigit()):
        print("Invalid ID. Student ID must contain exactly 9 digits.")
        return
    for student in students:
        if student["id"] == student_id:
            while True:
                print(f"\n   <<Hello {student['name']}>>")
                print("1. View your Courses")
                print("2. View Grades")
                print("3. Calculate GPA")
                print("4. View Passed and Failed Courses")
                print("5. View your data as CSV")
                print("6. Exit")
                choice3 = input("Enter your choice: ").strip()
                if choice3 == "1":
                    if student["courses"]:
                        print("\nCourses:", list(student["courses"].keys()))
                    else:
                        print("No courses registered yet.\n")
                elif choice3 == "2":
                    if student["courses"]:
                        print("\nGrades:")
                        for course, details in student["courses"].items():
                            grade = details["grade"] if details["grade"] is not None else "No grade yet"
                            print(f"    {course}: {grade}")
                    else:
                        print("No courses registered yet.\n")
                elif choice3 == "3":
                    calculate_GPA(student_id)
                elif choice3 == "4":
                    passed_and_failed(student)
                elif choice3 == "5":
                    export_to_csv("2")
                elif choice3 == "6":
                    print("Exiting Student Menu...\n")
                    return
                else:
                    print("Invalid input. Please try again.\n")
    print("Student ID not found.\n")


# Main Program
print("                  Welcome to SUT system                    ")
while True:
    print("1. Teacher Menu")
    print("2. Student Menu")
    print("3. Exit")
    choice = input("Enter your choice: ").strip()

    load_file()
    if choice == "1":
        username = input("--------------\nEnter username: ").strip(); password = input("Enter password: ").strip()
        if username == admin_username and password == admin_password:
            print("--------------\nLogin successful! Welcome to Teacher Module.")
            teacher_user()
        else:
            print("**Incorrect username or password.\n")
    elif choice == "2":
        student_user()
    elif choice == "3":
        print("Exiting system. Goodbye!\n")
        break
    else:
        print("Invalid choice. Try again.\n")



    

 