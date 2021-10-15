# CDC - Backend

---

### Setup

1. Download the Repository to your local machine <br>
2. Create a Virtual Environment in the [CDC_Backend](./) folder with this command below <br>
   `python -m venv venv`
3. Activate the environment with this command <br>
   `.\venv\Scripts\activate`
4. Install the dependencies <br>
   `pip install -r requirements.txt `
5. Ensure that you have the PostgreSQL installed on your machine and is running on PORT **5432** <br>
6. Make sure to give the  correct database credentials in [settings.py](./CDC_Backend/CDC_Backend/settings.py)

### Running the Application

1. Activate the environment with this command. <br>
   `.\venv\Scripts\activate`
2. Start the application by running this command (_Run the command where [manage.py](./CDC_Backend/manage.py) is
   located_) <br>
   ` python manage.py runserver`

### Accessing the Admin Panel

1. You can access the admin panel by running the server and opening <http://localhost:8000/admin>
2. Run `python manage.py createsuperuser` to create a user to access the admin panel.
3. Set up the Username and Password
4. You can log in and change the database values anytime.

### Deploying

1. Add the hosted domain name in `ALLOWED_HOSTS` in [settings.py](./CDC_Backend/CDC_Backend/settings.py)
2. Update the `CORS_ORIGIN_WHITELIST` list and `CORS_ORIGIN_ALLOW_ALL` variable

### API Reference

Check [here](./CDC_Backend/README.md) for Api Reference
