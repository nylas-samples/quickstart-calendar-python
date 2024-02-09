# Import your dependencies
from dotenv import load_dotenv
import os
from nylas import Client
from flask import Flask, request, redirect, url_for, session, jsonify
from flask_session.__init__ import Session
from nylas.models.auth import URLForAuthenticationConfig
from nylas.models.auth import CodeExchangeRequest
from datetime import datetime, timedelta

# Load your env variables
load_dotenv()

# Create the app
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize Nylas client
nylas = Client(
    api_key = os.environ.get("NYLAS_API_KEY"),
    api_uri = os.environ.get("NYLAS_API_URI"),
)

# Call the authorization page
@app.route("/oauth/exchange", methods=["GET"])
def authorized():
    if session.get("grant_id") is None:
        code = request.args.get("code")
        exchangeRequest = CodeExchangeRequest({"redirect_uri": "http://localhost:5000/oauth/exchange",
                                                                                  "code": code,
                                                                                  "client_id": os.environ.get("NYLAS_CLIENT_ID")})
        exchange = nylas.auth.exchange_code_for_token(exchangeRequest)
        session["grant_id"] = exchange.grant_id
        return redirect(url_for("login"))
        
# Main page
@app.route("/nylas/auth", methods=["GET"])
def login():
    if session.get("grant_id") is None:
        config = URLForAuthenticationConfig({"client_id": os.environ.get("NYLAS_CLIENT_ID"), 
                                                                      "redirect_uri" : "http://localhost:5000/oauth/exchange"})
        url = nylas.auth.url_for_oauth2(config)
        return redirect(url)
    else:
        return f'{session["grant_id"]}'

@app.route("/nylas/primary-calendar", methods=["GET"])
def primary_calendar():
    query_params = {"limit": 5} 
    try:
        calendars, _, _ = nylas.calendars.list(session["grant_id"], query_params)
        for primary in calendars:
            if primary.is_primary is True:
                session["calendar"] = primary.id
        return f'{session["calendar"]}'
    except Exception as e:
        return f'{e}'

@app.route("/nylas/list-events", methods=["GET"])
def list_events():
    query_params = {"calendar_id": session["calendar"], "limit": 5}
    events = nylas.events.list(session["grant_id"], query_params=query_params).data
    return jsonify(events)

@app.route("/nylas/create-event", methods=["GET"])
def create_event():
    now = datetime.now()
    now_plus_10 = now + timedelta(minutes = 10)
    start_time = int(datetime(now.year, now.month, now.day, now.hour, 
    now.minute, now.second).strftime('%s'))
    end_time = int(datetime(now.year, now.month, now.day, now_plus_10.hour, 
    now_plus_10.minute, now_plus_10.second).strftime('%s'))
    query_params = {"calendar_id": session["calendar"]}

    request_body = {
        "when": { 
            "start_time": start_time,
            "end_time": end_time,       
        },
        "title": "Your event title here"
    }

    try:
        event = nylas.events.create(session["grant_id"], 
        query_params = query_params, request_body = request_body)
        return jsonify(event)
    except Exception as e:
        return f'{e}'

# Run our application
if __name__ == "__main__":
    app.run()
