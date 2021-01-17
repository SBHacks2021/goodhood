from flask_api import FlaskAPI, request
from flask import request
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, firestore, db
import googlemaps
from googlemaps import places, geocoding
import json

app = FlaskAPI(__name__)
fb = firebase.FirebaseApplication("https://eat-local-96903-default-rtdb.firebaseio.com/", None)
cred = credentials.Certificate("eat-local-96903-firebase-adminsdk-t0evo-3e364058cd.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://eat-local-96903-default-rtdb.firebaseio.com'
})

gmaps = googlemaps.Client()


@app.route('/api')
def home():
    args = request.args
    ref = db.reference('/')
    data = ref.get()
    if len(args) == 0:
        return data
    else:
        valid = []
        if (name := args.get('name')) is not None:
            return get_by_name(name)



    return ""


@app.route('/getnearby')
def get_nearby():
    args = request.args
    # if len(args) not in range(1,4):
    #    return {"error": "not enough arguments"}
    address = args.get('address')
    radius = args.get('radius')
    print("args:", args)
    geo = geocoding.geocode(gmaps, address)
    lat = geo[0]['geometry']['location']['lat']
    lng = geo[0]['geometry']['location']['lng']
    nearby = places.places_nearby(gmaps, location=(lat, lng), radius=50000, type="restaurant")
    return nearby


def get_by_name(name):
    ref = db.reference('/').order_by_key()
    data = ref.get()
    valid = []
    for rest in data:
        if name.lower() in rest['name'].lower():
            valid.append(rest)
    return valid


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
