pip3 install pipenv
pipenv shell
pip3 install -r requirements.txt
flask db init
flask db migrate
flsak db upgrade
