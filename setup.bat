
start /wait  python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt &^
echo Environment Setup Complete &^
timeout 3 > NUL &^
echo enter password for user postgres &^
createdb -h localhost -p 5432 -U postgres cdc &^
cd "CDC_Backend" &^

python manage.py flush --no-input &^
python manage.py makemigrations &^
python manage.py migrate &^
echo Migrations complete &^
cd .. &^
start .\superuser.bat &^
echo done successfully
