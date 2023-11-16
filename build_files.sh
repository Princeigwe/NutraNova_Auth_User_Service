echo "BUILD START"
pip install -r requirements.txt
pip install pyjwt
python3 manage.py makemigrations
python3 manage.py migrate
echo "BUILD END"