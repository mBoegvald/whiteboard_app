---
name: Miklas Bøgvald
---

# How to run project locally

#### To join the project follow the guide underneath

In this project you need python 3.7 or newer

1. To check your version write `python3 -V`

2. To create an environment named ibm-env write `python3 -m venv ibm-env`

3. Navigate to the directory where your environment is located and write `source ibm-env/bin/activate` to activate your environment

4. Install the required dependencies `(ibm-env) $ pip install -r requirements.txt`

5. Now the project can run `python manage.py runserver`

# What does this project do

#### This project has following features:

Create posts including embedded videos.

Delete your own posts

Comment on posts

Create users (if you're loggeed in)

Toggle superuser status of other users (if you're a superuser) - Don't remove superuser rights for everyone :D

Password resets (link will come in the terminal, but the functionality to send mails is there if django_rq is imported)

###### Account logins (since you can't create accounts if not logged in at the moment):

User: admin
Password: admin
(currently superuser)

User: MB (needs to be capitalized)
Password miklas123
(Currently NOT superuser)
