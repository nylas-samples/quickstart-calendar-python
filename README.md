# How to run

1. Install the dependencies

```bash
pip3 install Flask flask-session python-dotenv nylas
```

2. Create a .env file and add your env variables

```env
NYLAS_CLIENT_ID=""
NYLAS_API_KEY=""
NYLAS_API_URI="https://api.us.nylas.com"
EMAIL="<RECIPIENT_EMAIL_ADDRESS_HERE>"
```

3. In the Nylas dashboard, create a new application and set the Hosted Authentication callback URI to `http://localhost:5000/oauth/exchange`

3. Run the project

```bash
python quickstart-calendar-python.py
```

5. Open your browser and go to `http://localhost:5000/nylas/auth` and log in to an end user account

6. After authenticating an end user account, you can visit the following URLs to get a feel for some of what you can do with the Nylas Calendar API.

```text
http://localhost:5000/nylas/primary-calendar
http://localhost:5000/nylas/list-events
http://localhost:5000/nylas/create-event
```
