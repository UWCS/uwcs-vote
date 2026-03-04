# UWCS Vote

UWCS Vote is the voting portal for UWCS elections and general meetings.

## Installation

UWCS Vote is built and tested against Python 3.8/3.9, using Django as the web framework and PostgreSQL for the database.

### Environment Setup

1. Create a new virtual environment.  
   `python -m venv venv`
2. Activate the virtual environment
    - On Linux and macOS: `source venv/bin/activate`.
    - On Windows: `.\venv\Scripts\activate`.
3. Confirm the virtual environment has been activated.
    - On Linux and macOS: `which python`.  
      Expected output: `.../venv/bin/python`.
    - On Windows: `where.exe python`.  
      Expected output: `...\venv\Scripts\python.exe`.
4. Install dependencies.  
    `pip install -r requirements.txt`.
5. Ensure all settings in `settings.py` are up to date:
6. Create a database for UWCS Vote to run on.  
    On postgres:
    - `CREATE USER uwcs_vote WITH PASSWORD 'password';`
    - `CREATE DATABASE uwcs_vote WITH ONWER = uwcs_vote;`
7. Prepare the database by running migrations with `python manage.py migrate`.
8. Create a superuser for the site with `python manage.py createsuperuser`.
9. Create the configuration file(s) for the web server of your choosing (do not worry about this step if you are running locally).
    
## Running 

Start the web server. If you are running locally, you can use the command `python manage.py runserver`

## SSO Authentication Configuration

UWCS Vote uses django-allauth to operate a single sign-on system with the UWCS website (at the time of writing, this is Dextre). To set this up, follow these instructions:

1. Create an application within the Django admin in the UWCS website. Use the following settings as an example:
   1. Name: `UWCS Vote`
   2. User: click search and search for your user
   3. Redirect URLs: follow the format of `http(s)://yourdomain.com/accounts/uwcs/login/callback/`
   4. Client type: Public
   5. Authorisation grant type: Authorisation code
   6. Name: UWCS Vote
2. Edit the "example.com" site in the Django admin in UWCS Vote, with the domain as your domain (e.g. `localhost:8000`) and give it a useful label.
3. Create a "social application" in the Django admin in UWCS Vote.
   1. Provider: UWCS
   2. Name: UWCS Website
   3. Client id: copy from your new application
   4. Secret key: copy from your new application
   5. Sites: select the site with your domain

## Contributor Notes

- Errors installing Psycopg are likely due to missing dependencies to compile the library.
  It requires the `Python.h` header file, typically provided by a package called `python3-dev`.
  It also requires `libpq-fe.h`, typically contained in `libpq-dev`.
    - Alternately, it can be replaced with `psycopg-binary`.
- If you require anything created in the UWCS website (e.g. an OAuth Application), please speak to someone with superuser privileges (currently this is Josh or the Tech Officer)