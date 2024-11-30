import random
from django.db.utils import IntegrityError
from APIs.models import Student

from APIs.constants import BRANCHES, BATCH_CHOICES, DEGREE_CHOICES

# To run this script run the following command:
# python manage.py runscript add_students --script-args <add_type> <num_of_stundents_to_add>


def run(*args):

    # Throw error if invalid number of arguments passed
    if not args:
        raise ValueError("Invalid number of arguments passed")
    
    if args[0] in ("manual", "man") :

        if len(args) != 2 or not args[1].isdigit() or int(args[1]) < 1:
            raise ValueError("Invalid number of arguments passed")

        print("id\troll_no\tname\tbranch\tphone_number\tcpi\tdegree\tbatch")
        for i in range(1, int(args[1])+1):
            details = input()
            details = details.split(",")
            details = [i.strip() for i in details]
            details = [int(details[0]), int(details[1]), details[2], details[3], 
                       int(details[4]), float(details[5]), details[6], details[7]]

            student = Student.objects.create(
                id = details[0],
                roll_no = details[1],
                name = details[2],
                branch = details[3],
                phone_number = details[4],
                cpi = details[5],
                degree = details[6],
                batch = details[7],

            )
            student.save()

    elif args[0] in ("auto", "automatic"):
        if len(args) != 2 or not args[1].isdigit() or int(args[1]) < 1:
            raise ValueError("Invalid number of arguments passed")
        
        for i in range(1, int(args[1])+1):
            try:
                student = Student.objects.create(
                    id = i-1,
                    roll_no = 220010000 + i,
                    name = "Student " + str(i),
                    branch = random.choice(BRANCHES),
                    phone_number = random.randint(1000000000, 9999999999),
                    cpi = random.random()*10,
                    degree = random.choice(DEGREE_CHOICES)[0],
                    batch = random.choice(BATCH_CHOICES)[0],
                )
                student.save()
            except IntegrityError:
                pass
    
    elif args[0] in ("del", "delete"):
        # delete students with name starting with Student
        s = Student.objects.filter(name__startswith="Stundent")
        s.delete()

    else:
        raise ValueError("Invalid argument passed")

