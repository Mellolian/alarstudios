import os

os.system('git clone https://github.com/Mellolian/alarstudios.git')
os.chdir(os.path.join(os.getcwd(), 'alarstudios'))
os.system('pip3 install pipenv')
os.system('pip3 install -r requirements.txt')
os.system('flask run')
