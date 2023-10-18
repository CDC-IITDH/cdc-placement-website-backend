python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
echo "Environment setup complete"
cd CDC_Backend

python3 manage.py flush --no-input
python3 manage.py makemigrations APIs
python3 manage.py migrate
echo "Migrations complete"

python3 manage.py collectstatic --noinput

DIR="./Storage"
if [ -d "$DIR" ]; then
  ### Take action if $DIR exists ###
  echo "${DIR} Directory already exists"
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo "Creating ${DIR} Directory..."
  mkdir ${DIR}
  echo "${DIR} Directory Created"
fi

echo Do you want ceate credentials for super user (Y/N) ?
read create
create=${create^^}

if [ "$create" == "Y" ]; then
	### Take action if user want to create ###
	python3 manage.py createsuperuser
fi
