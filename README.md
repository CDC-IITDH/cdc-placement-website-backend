python# CDC - Backend

---

### Setup

1. Download the Repository to your local machine <br>
2. Make Sure u have downloaded python from python.org or windows store.
3. Create a Virtual Environment in the [CDC_Backend](./) folder with this command below <br>
   `python -m venv venv`
3. Activate the environment with this command <br>
   `.\venv\Scripts\activate` (for WINDOWS) <br>
   `source ./venv/bin/activate` (for LINUX)
4. Install the dependencies <br>
   `pip install -r requirements.txt `
5. Ensure that you have the PostgreSQL installed on your machine and is running on PORT **5432** <br>
6. Make sure to give the correct database credentials in [settings.py](./CDC_Backend/CDC_Backend/settings.py)(https://www.youtube.com/watch?v=bE9h6aAky4s&t=193s)
7. Run these following commands below. (The same are there in setup.sh for linux users and setup.bat for windows users)
```cd  CDC_Backend
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
mkdir Storage
python manage.py makemigrations APIs
```



### Running the Application

1. Activate the environment with this command. <br>
   `.\venv\Scripts\activate` (for WINDOWS) <br>
   `source ./venv/bin/activate` (for LINUX) 
2. Start the application by running this command (_Run the command where [manage.py](./CDC_Backend/manage.py) is
   located_) <br>
   ` python manage.py runserver`

### Accessing the Admin Panel

1. You can access the admin panel by running the server and opening <http://localhost:8000/admin>
2. Run `python manage.py createsuperuser` to create a user to access the admin panel.
3. if there is an error due to time then sync your machine time .
4. Set up the Username and Password
5. You can log in and change the database values anytime.
6. Create your id as insitute Roll No for both admin and student .
7. if you are still getting an error ,open inspect and see in network 
And then recognize it
8.Check the client  link in dev.env in backend and  .env in frontend  is the same

 
 # Error
 1.make sure that your machine time and google time are same ,if not go to setting of date and time and sync this 
 2.make sure u have used  same id for both student and Admin that is your iitfh roll_no
 3. same client link in .env of frontend or constants.py of bakcend 
 
### Deploying

1. Add the hosted domain name in `ALLOWED_HOSTS` in [settings.py](./CDC_Backend/CDC_Backend/settings.py)
2. Update the `CORS_ORIGIN_WHITELIST` list and `CORS_ORIGIN_ALLOW_ALL` variable

### Starting the Email Server

Run the following command to start the email backend process <br>
`python manage.py process_tasks`

### API Reference

Check [here](./CDC_Backend/README.md) for Api Reference

For Documentation with Postman Collection,
click [here](https://documenter.getpostman.com/view/15531322/UVJfhuhQ#568ad036-ad0e-449a-a26f-4d86616b1393)
