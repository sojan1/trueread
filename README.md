pip install "fastapi[standard]"

pip install Jinja2

pip install requests
pip install sqlalchemy

uvicorn main:app --reload

 fastapi dev main.py
 docker build -t isaid-app .
 docker run -d -p 8000:80 --name trueread-container trueread-app     
 docker-compose up --build            
===========================

git config --global user.name "sojan1"         
git config --global user.email "sojanctherakom@gmail.com"     
git remote add origin https://github.com/sojan1/trueread.git       

git add .
git commit -m "Initial commit"   
git push origin master 

git add .
git commit -m "changed some pages to work layout"
git push origin master

---------------------------
In the System variables section, find and select the Path variable and click Edit. Click New and add the following line
C:\Program Files\PostgreSQL\17\bin

pg_dump -U postgres -d isaid > D:\projects\trueread\database_backup.sql

