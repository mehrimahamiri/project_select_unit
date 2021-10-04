import os
from colorama import Fore, Style, init
import hashlib
import time
import json
import sys
from prettytable import PrettyTable

files = ["db_st.json", "db_re.json", "db_te.json", "db_course.json"]
for i in files:
    if not os.path.exists(i):  # age in address mojod nabod
        json.dump({}, open(i, "w"))

clr = "clear" if sys.platform == "linux" else "cls"


class App:
    init()

    def __init__(self) -> None:
        self.menu_main_app = """
1-Sign in 
2-Sign up
3-Exit

Please enter your choice : """
        self.menu_in_up = """
1-Student 
2-Reception
3-Teacher
4-Back

please chose number : """
        self.logged_in = ""

    def run(self):
        self.main_menu()

    def main_menu(self):

        header = Fore.CYAN + "\n\nــــــــــــــــــــــــــ  Welcome to SELECT_UNIT  Demo  ــــــــــــــــــــــــــ" + Style.RESET_ALL
        print(header)

        print(self.menu_main_app, end="")
        while True:  # True==1
            choice = input("")
            if choice in ["1", "2", "3"]:  # methods should be called
                break
            else:
                os.system(clr)
                print(Fore.RED + f"\t\t\tYou must only select specified NUMBER")
                print(Fore.RED + '\t' * 4 + f"Please try again !" + Style.RESET_ALL)
                print(header, self.menu_main_app, end="")

        if choice in ["1", "2"]:
            self.sign_in_sign_up(choice)
        elif choice == "3":
            exit()

    # ======================================================================
    @staticmethod
    def print_header(user, username):
        login_msg = Fore.YELLOW + f" {user} ____________________ {username} _______________________  Logged in!" + Style.RESET_ALL
        print(login_msg)

    @staticmethod
    def get_course_list():
        course = json.load(open("db_course.json"))
        courses = course.get("courses") or []

        x = PrettyTable()
        x.field_names = ["id", "Course", "Capacity", "Remaining", "Unit", "Teacher"]
        for e, item in enumerate(courses, start=1):
            x.add_row([e] + list(item.values()))
        x = str(x).replace("+-", Style.BRIGHT + Fore.LIGHTGREEN_EX + "x-")
        x = str(x).replace("-+", "-+" + Style.RESET_ALL)
        x = str(x).replace("|", Style.BRIGHT + Fore.LIGHTGREEN_EX + "|" + Style.RESET_ALL)
        print(x)
        return courses

    @staticmethod
    def search_course_list(name=None):
        course_file = json.load(open("db_course.json"))
        courses = course_file.get("courses") or []
        f = list(filter(lambda course: course["course"] == name, courses))
        if len(f) > 0:
            x = PrettyTable()
            x.field_names = ["Course", "Capacity", "Remaining", "Unit", "Teacher"]
            for item in f:
                x.add_row(item.values())
            print(x)

        # x = PrettyTable()
        # x.field_names = ["Course","Capacity","Remaining","Unit","Teacher"]

    def student_menu(self):

        while True:
            choice = input(
                "\n\n1- Course list\n2- Course search\n3- View all units\n4 -Select lesson\n5- Exit\n\nPlease enter "
                "your choice: ")

            if choice in [str(i) for i in range(1, 6)]:
                os.system(clr)
                break
            else:
                os.system(clr)
                print(Fore.RED + f"\t\t\tYou must only select specified NUMBER")
                print(Fore.RED + '\t' * 4 + f"Please try again !" + Style.RESET_ALL)

        if choice == "1":
            self.get_course_list()
            self.student_menu()

        elif choice == "2":
            name = input('\nEnter The course name (q for Quit): ')
            if name == "q":
                os.system(clr)
            else:
                self.search_course_list(name)
            self.student_menu()
        elif choice == "3":
            print(Fore.YELLOW + Style.BRIGHT + f"ALl Units:{self.get_student_unit()}" + Style.RESET_ALL)
            self.student_menu()
        elif choice == "4":
            self.select_lesson()
        elif choice == "5":
            self.main_menu()

    def get_student_unit(self):
        data = json.load(open("db_st.json"))
        data2 = json.load(open("db_course.json"))

        units = 0
        for student in data['students']:
            if student['username'] == self.logged_in:
                if student.get("courses") and data2.get("courses"):
                    for course in student['courses']:
                        cs = list(filter(lambda x: x["course"] == course, data2['courses']))
                        if len(cs) > 0:
                            units += int(cs[0]['unit'])
        return units

    def select_lesson(self):
        last = self.get_course_list()
        units = self.get_student_unit()
        print(f"All Units: {units}")
        while 1:
            inp = input("Enter lesson id>>")
            os.system(clr)
            if inp in [str(i) for i in range(1, int(len(last)) + 1)]:
                break
            elif inp == "q":
                self.student_menu()
            else:
                print(Fore.RED + Style.BRIGHT + "NOT VALID" + Style.RESET_ALL)
                last = self.get_course_list()

        cn = last[int(inp) - 1]['course']
        if int(last[int(inp) - 1]['unit']) + units > 20:
            print(Style.BRIGHT + Fore.RED + f"You can't pick this course! your units : {units} and max units: 20")
            self.select_lesson()
        data = json.load(open("db_st.json"))
        for student in data['students']:
            if student['username'] == self.logged_in:
                if not student.get("courses"):
                    student['courses'] = []
                if cn not in student['courses']:
                    student['courses'].append(cn)
                    json.dump(data, open("db_st.json", "w"))

                    os.system(clr)
                    print(Fore.GREEN + Style.BRIGHT + f"Course `{cn}` added to your courses" + Style.RESET_ALL)
                    self.student_menu()

                else:
                    os.system(clr)
                    print(
                        Fore.RED + Style.BRIGHT + f"Course `{cn}` already is in your courses\nYour Courses:\
                        {' - '.join(student['courses'])}" + Style.RESET_ALL)
                    self.select_lesson()
                break

    def responsible_menu(self, ):

        while 1:
            choice = input(
                "\n\n1- Course list\n2- Course search\n3- View all units\n4- Add lessons\n5- Students List\n6- Student Search\n7- Select Course\n8- Exit\n\nPlease enter "
                "your choice: ")

            if choice in [str(i) for i in range(1, 9)]:
                break
            else:
                os.system(clr)
                print(Fore.RED + f"\t\t\tYou must only select specified NUMBER")
                print('\t' * 4 + f"Please try again !" + Style.RESET_ALL)

        if choice == "1":
            os.system(clr)
            self.get_course_list()
            self.responsible_menu()

        elif choice == "2":
            os.system(clr)
            name = input('\nEnter The course name (q for Quit): ')
            if name == "q":
                os.system(clr)
            else:
                self.search_course_list(name)
            self.responsible_menu()

        elif choice == "3":
            os.system(clr)
            self.responsible_menu()

        elif choice == "4":
            os.system(clr)
            level = 0
            db_course = {

            }
            while 1:
                if level == 0:
                    inp = input("Enter the course name : ")
                    db_course['course'] = inp
                elif level == 1:
                    inp = input("Enter the capacity : ")
                    db_course['capacity'] = inp
                elif level == 2:
                    inp = input("Enter the remaining : ")
                    db_course['remaining'] = inp
                elif level == 3:
                    inp = input("Enter the unit : ")
                    db_course['unit'] = inp
                elif level == 4:
                    inp = input("Enter the teacher : ")
                    db_course['teacher'] = inp
                if inp in ["", " ", None]:
                    os.system(clr)
                    print(Fore.RED + Style.BRIGHT + "This entry could not be empty!" + Style.RESET_ALL)
                    continue
                elif inp == "q":
                    print("Exiting")
                    break
                elif (level in [0, 4] and inp.isdigit()) or (level in [1, 2, 3] and not inp.isnumeric()):
                    print(Fore.RED + Style.BRIGHT + "Entered Value is not valid" + Style.RESET_ALL)

                else:
                    level += 1
                    if level == 5:
                        break
            os.system(clr)
            if level == 5:
                data = json.load(open("db_course.json"))
                if data.get("courses") is None:
                    data["courses"] = []
                data["courses"].append(db_course)
                json.dump(data, open("db_course.json", "w"))
                print(Fore.GREEN + Style.BRIGHT + "\n\t\tCourse was created successfully!!" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + Style.BRIGHT + "\n\t\tBack to Menu" + Style.RESET_ALL)
            self.responsible_menu()
        elif choice == "5":
            os.system(clr)
            self.students_list()
            os.system(clr)
            self.responsible_menu()
        elif choice == "6":
            self.search_student()
        elif choice == "7":
            self.select_course()
        elif choice == "8":
            os.system(clr)
            self.main_menu()

    @staticmethod
    def students_list():
        data = json.load(open("db_st.json"))
        x = PrettyTable()
        x.field_names = ["id", "username"]
        if data.get("students"):
            for student in data['students']:
                x.add_row([student['Id'], student['username']])
        print(x)
        input("Press Enter to Back...")

    def search_student(self):
        data = json.load(open("db_st.json"))
        x = PrettyTable()
        x.field_names = ["id", "username"]
        while 1:
            inp = input("Enter Student Name or Id>>")
            if inp == "q":
                self.responsible_menu()
            stu = list(filter(lambda x: x['Id'] == inp or x['username'] == inp, data.get('students', [])))
            try:
                x.add_row([stu[0]['Id'], stu[0]['username']])
                os.system(clr)
                print()
                print(x)
                self.responsible_menu()
            except IndexError:
                print(Fore.RED + Style.BRIGHT + "No Student found!" + Style.RESET_ALL)

    def select_course(self):
        data = json.load(open("db_course.json"))
        data2 = json.load(open("db_st.json"))
        x = PrettyTable()
        x2 = PrettyTable()
        x.field_names = ["id", "username"]
        x2.field_names = ["Course", "Capacity", "Remaining", "Unit", "Teacher"]

        while 1:
            inp = input("Enter course name>>")
            if inp == "q":
                self.responsible_menu()
            stu = list(filter(lambda x: x['course'].lower() == inp.lower(), data.get('courses', [])))
            try:
                x2.add_row(stu[0].values())
                cn = stu[0]['course']
                for student in data2.get("students",[]):
                    if cn in student.get("courses",[]):
                        x.add_row([student['Id'],student['username']])


                os.system(clr)
                print()
                print(Style.BRIGHT+Fore.CYAN+"Users has this course :"+Style.RESET_ALL)
                print(x)
                print(Style.BRIGHT+Fore.CYAN+"Course Information :"+Style.RESET_ALL)
                print(x2)
                input("Press Enter Key To Continue...")
                os.system(clr)

                self.responsible_menu()
            except IndexError:
                print(Fore.RED + Style.BRIGHT + "No Student found!" + Style.RESET_ALL)

    def sign_in_sign_up(self, number):

        header2 = Fore.CYAN + "\n\nـــــــــــــــــــــــــــــــ  SELECT_TYPE  ـــــــــــــــــــــــــــــــــ" + \
                  Style.RESET_ALL
        os.system(clr)
        print(header2)

        print(self.menu_in_up, end="")

        while 1:
            choice = input("")
            if choice in ["1", "2", "3", "4"]:
                os.system(clr)
                break
            else:
                os.system(clr)
                print(Fore.RED + f"\t\t\tYou must only select specified NUMBER")
                print(Fore.RED + f"\t\t\t\tPlease try again !" + Style.RESET_ALL)
                print(header2, self.menu_in_up, end="")

        if choice == "4":
            self.main_menu()
        elif number == '1':
            self.sign_in(choice)
        elif number == '2':
            self.sign_up(choice)
        
    def teacher_menu(self):
        while 1:
            choice = input(
                "\n\n1- Course list\n2- Course search\n3- View all units\n4- Add lessons\n5- Students List\n6- Student Search\n7- Select Course\n8- Exit\n\nPlease enter "
                "your choice: ")
            if choice in [str(i) for i in range(1, 9)]:
                break
            else:
                os.system(clr)
                print(Fore.RED + f"\t\t\tYou must only select specified NUMBER")
                print('\t' * 4 + f"Please try again !" + Style.RESET_ALL)
        if choice == "1":
            self.get_course_list()
        elif choice == "2":
            name = input('\nEnter The course name (q for Quit): ')
            if name == "q":
                os.system(clr)
            else:
                self.search_course_list(name)
            self.teacher_menu()
        elif choice == "7":
            self.select_course()

    # ======================================================================
    def sign_up(self, number):
        user_name = input("please enter username : ")
        password = input("please enter password : ")
        re_password = input("please repeat your password : ")

        if password == re_password:
            hp = hashlib.sha256(password.encode()).hexdigest()
            if number == "1":
                st_id = int(time.time())  # create number id from timer system
                db_st = {"Id": st_id,
                         "username": user_name,
                         "password": hp
                         }
                data = json.load(open("db_st.json"))
                if data.get("students") is None:
                    data["students"] = []
                data["students"].append(db_st)
                json.dump(data, open("db_st.json", "w"))
            elif number == "2":
                db_re = {
                    "username": user_name,
                    "password": hp
                }
                data = json.load(open("db_re.json"))
                if data.get("reception") is None:
                    data["reception"] = []
                data["reception"].append(db_re)
                json.dump(data, open("db_re.json", "w"))
            elif number == "3":
                db_te = {
                    "username": user_name,
                    "password": hp
                }
                data = json.load(open("db_te.json"))
                if data.get("teacher") is None:
                    data["teacher"] = []
                data["teacher"].append(db_te)
                json.dump(data, open("db_te.json", "w"))
            os.system(clr)
            print(Fore.GREEN + "\n\t\tYour account was created successfully!!" + Style.RESET_ALL)
            self.main_menu()
        else:
            print("passwords doesn't mach !")
            self.menu_in_up()


    def teacher_menu(self):
        print("1 - LIST\n2 - SEARCH\n3 - SELECTED\n4 - SELECT\n5 - STUDENTS")
        while 1:
            inp = input(">>")
            if inp in [str(i) for i in range(1, 6)]:
                self.teacher_menu()

    def sign_in(self, number):
        while 1:
            user_name = input("please enter username : ")
            if not user_name:
                os.system(clr)
                continue
            break
        while 1:
            password = input("please enter password : ")
            if not password:
                os.system(clr)
                print(f"please enter username : {user_name}")
                continue
            break

        hp = hashlib.sha256(password.encode()).hexdigest()
        failed = False
        if number == "1":
            data = json.load(open("db_st.json"))
            student = data.get("students") or []
            f = list(filter(lambda x: x["username"] == user_name and x["password"] == hp, student))
            if len(f) > 0:
                os.system(clr)
                self.print_header("Student", user_name)
                self.logged_in = user_name
                self.student_menu()
            else:
                failed = True
        elif number == "2":
            data = json.load(open("db_re.json"))
            reception = data.get("reception") or []
            f = list(filter(lambda x: x["username"] == user_name and x["password"] == hp, reception))
            if len(f) > 0:
                os.system(clr)
                self.print_header("Reception", user_name)
                self.logged_in = user_name
                self.responsible_menu()
            else:
                failed = True
        elif number == "3":
            data = json.load(open("db_te.json"))
            teacher = data.get("teacher") or []
            f = list(filter(lambda x: x["username"] == user_name and x["password"] == hp, teacher))
            if len(f) > 0:
                os.system(clr)
                self.teacher_menu()
            else:
                failed = True
        else:
            failed = "."
            print(".......")
        if failed is True:
            print("User or pass is wrong")


app = App()
app.run()
