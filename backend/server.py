from flask_api import FlaskAPI, request
from flask import request
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, firestore, db
import googlemaps
from googlemaps import places, geocoding
import json
import numpy as np

app = FlaskAPI(__name__)
fb = firebase.FirebaseApplication("https://eat-local-96903-default-rtdb.firebaseio.com/", None)
cred = credentials.Certificate("eat-local-96903-firebase-adminsdk-t0evo-3e364058cd.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://eat-local-96903-default-rtdb.firebaseio.com'
})

gmaps = googlemaps.Client('')


# def do():
#     ref = db.reference('/')
#     data = ref.get()
#     counter = 0
#     for rest in data:
#         if rest is not None:
#             address = rest['address']
#             geo = geocoding.geocode(gmaps, address)
#             lat = geo[0]['geometry']['location']['lat']
#             lng = geo[0]['geometry']['location']['lng']
#             nearby = places.places_nearby(gmaps, location=(lat, lng), radius=1, type="restaurant")
#             print(nearby['results'])
#
#
# do()


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
            valid.extend(get_by_name(name))
        if (food_types := args.get('food_types')) is not None:
            valid.extend(get_by_types(food_types))
        if (methods := args.get('methods')) is not None:
            valid.extend(get_by_method(methods))
        return valid


@app.route('/getnearby')
def get_nearby():
    args = request.args
    # if len(args) not in range(1,4):
    #    return {"error": "not enough arguments"}
    address = args.get('address')
    rad = args.get('radius')
    print("args:", args)
    geo = geocoding.geocode(gmaps, address)
    lat = geo[0]['geometry']['location']['lat']
    lng = geo[0]['geometry']['location']['lng']
    nearby = places.places_nearby(gmaps, location=(lat, lng), radius=1, type="restaurant")
    return nearby


def get_by_name(name: str) -> []:
    ref = db.reference('/').order_by_key()
    data = ref.get()
    valid = []
    for rest in data:
        if name.lower() in rest['name'].lower():
            valid.append(rest)
    return valid
def get_by_method(methods) -> []:
    ref = db.reference('/').order_by_key()
    data = ref.get()
    valid = []
    for rest in data:
        print(rest)
        if rest is not None:
            print(rest)
            if 'services' in rest.keys():
                if np.any(np.in1d([type.lower() for type in methods.split(",")],
                                  [re.lower() for re in rest['services']])):
                    valid.append(rest)
    return valid



def get_by_types(types) -> []:
    ref = db.reference('/').order_by_key()
    data = ref.get()
    valid = []
    for rest in data:
        if rest is not None:
            if np.any(np.in1d([type.lower() for type in types.split(",")],
                              [re.lower() for re in rest['food_type'].split(',')])):
                valid.append(rest)
    return valid


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
