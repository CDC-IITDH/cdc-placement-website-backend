import random
from django.db.utils import IntegrityError
from APIs.models import Student

# To run this script run the following command:
# python manage.py runscript add_students --script-args <add_type> <num_of_stundents_to_add>

def run(*args):

    # Throw error if invalid number of arguments passed
    if not args:
        raise ValueError("Invalid number of arguments passed")
    
    if args[0] in ("manual", "man") :
        if not args:
            raise ValueError("Invalid number of arguments passed")
        
        for i in range(1, int(args[1])+1):
            student = Student.objects.create(
                id = input("Enter id: "),
                roll_no = input("Enter roll_no: "),
                name = input("Enter name: "),
                branch = input("Enter branch: "),
                phone_number = input("Enter phone_number: "),
                cpi = input("Enter cpi: "),
                degree = input("Enter degree: "),
                batch = input("Enter batch: ")

            )
            student.save()

    elif args[0] in ("auto", "automatic"):
        if not args:
            raise ValueError("Invalid number of arguments passed")
        
        for i in range(1, int(args[1])+1):
            try:
                student = Student.objects.create(
                    id = i-1,
                    roll_no = 220010000 + i,
                    name = "Student " + str(i),
                    branch = random.choice(["CSE", "EE", "MECH", "CHEM", "CIVIL", "EP", "BSMS", "MNC"]),
                    phone_number = random.randint(1000000000, 9999999999),
                    cpi = random.random()*10,
                    degree = "bTech",
                    batch = random.randint(2018, 2023)
                )
                student.save()
            except IntegrityError:
                pass
    
    elif args[0] in ("del", "delete"):
        # delete students with name starting with Student
        s = Student.objects.filter(name__startswith="Student")
        s.delete()

    else:
        raise ValueError("Invalid argument passed")

