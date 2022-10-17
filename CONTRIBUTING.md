## Contributing Guidelines

You are **Awesome!** Thank you for your Interest in Contributing to this Project 🤗
For Contributions we strictly follow [Github Flow](https://guides.github.com/introduction/flow/).

## Contents

- [Setting Up the Project](#user-content-setting-up-the-project)
- [Contributing](#user-content-contributing)

### Setting Up the Project

1. The Project works seamlessly on Python version `3.8.6`

2. (Optional) [Fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository) the Repository

3. Clone Your Forked copy/the original repo - `git clone https://github.com/[YOUR-USERNAME]/Kitabe.git`

4.  Navigate to the directory of project -  `cd Kitabe/`


5. (Optional) If you're intending to raise an MR else you can skip this step, Create a new branch -  `git checkout -b [branch_name]`

6. Install requirements from [poetry](https://python-poetry.org/docs/#installation) - `poetry install`
    - If you prefer the vanilla route `poetry export -f requirements.txt --output requirements.txt --without-hashes` skip to step (8)


7. Activate the environment -  `poetry shell`

8. Open `BookRecSystem/settings.py`

9. Make Migrations - `python manage.py migrate`

10. `python manage.py runserver` - You're good to Go!!

📝 Raise an issue/start a discussion if you face difficulties while setting up the repo, we'll try to resolve it asap
#### Optional

- [Setting up Google Auth](https://django-allauth.readthedocs.io/en/latest/installation.html)

- [Setting up SMTP](https://youtu.be/-tyBEsHSv7w)

- [Creating Superuser](https://www.geeksforgeeks.org/how-to-create-superuser-in-django/)

### Contributing

- Please go through [Github Flow](https://guides.github.com/introduction/flow/), if not already. :)

- Take up an [Issue](https://github.com/Praful932/Kitabe/issues) or [Raise](https://github.com/Praful932/Kitabe/issues/new) one.

- Discuss your proposed changes & Get assigned.

- If your changes are approved, do the changes in branch `[branch_name]`.

- Run tests

- `flake8`, `python manage.py test`

- Fix if any test fails.

- Still in branch `[branch_name].`

- **Stage and Commit only the required files.**

- `git push origin [branch_name] -u`

- Browse [here](https://github.com/Praful932/Kitabe) and create a PR from your branch with the appropriate required details.

- If your PR is accepted, it is automatically deployed once merged. :)

- That's it!

**Tip**: To keep your Fork Repo all branches updated with Upstream use [this](https://upriver.github.io/).
