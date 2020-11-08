
## Contributing Guidelines

You are **Awesome!** Thank you for your Interest in Contributing to this Project 🤗
For Contributions we strictly follow [Github Flow](https://guides.github.com/introduction/flow/).

## Contents
- Setting Up the Project
- Contributing


### Setting Up the Project
- The Project works seamlessly on Python version `3.8.6`
- `git clone https://github.com/Praful932/Kitabe.git` - Clone the Repo Directly
- `cd Kitabe/`
- `git checkout -b [branch_name]` - Create a new branch
- `pip install virtualenv` - If you don't have virtualenv already installed
- `virtualenv bookenv` - Create a new environment
- `source bookenv/Scripts/activate` - Activate the environment
- `pip install -r requirements.txt` - Install requirements
- `python manage.py migrate` - Make Migrations
- Open `BookRecSystem/settings.py`
- Set `SECRET_KEY = "RANDOM_KEY"`
- Set `ALLOWED_HOSTS = ['kitabe-app.herokuapp.com', '127.0.0.1']`
- `python manage.py runserver` - You're good to Go!!

#### Optional
- [Setting up Google Auth](https://django-allauth.readthedocs.io/en/latest/installation.html)
- [Setting up SMTP](https://youtu.be/-tyBEsHSv7w)
- [Creating Superuser](https://www.geeksforgeeks.org/how-to-create-superuser-in-django/)


### Contributing
- Please go through [Github Flow](https://guides.github.com/introduction/flow/), if not already. :)
- Take up an [Issue](https://github.com/Praful932/Kitabe/issues) or [Raise](https://github.com/Praful932/Kitabe/issues/new) one.
- Discuss your proposed changes.
- If your changes are approved, do the changes in branch `[branch_name]`.
- Run tests
- `flake8`, `python manage.py test` 
- Fix if any test fails.
- Still in branch `[branch_name].`
- **Stage and Commit only the required files.**
- `git push --set-upstream origin [branch_name]`
- You'll get a link to Create a Pull Request.
- That's it!