from flask import Flask, render_template, request
from flask_wtf import form
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests

categories = ['Alcohol', 'American', 'Argentinian', 'Asian', 'Bakery', 'Bbq', 'Brazilian', 'Bread/pastries',
              'Breakfast', 'Burgers', 'Cajun', 'Chicken', 'Chinese', 'Coffee/tea', 'Convenience', 'Deli', 'Dessert',
              'European', 'French', 'German', 'Grocery', 'Hawaiian', 'Healthy', 'Ice cream', 'Indian', 'Irish',
              'Italian', 'Japanese', 'Juice', 'Latin american', 'Mexican', 'Middle eastern', 'Nepalese', 'Other',
              'Pasta', 'Pastries', 'Pizza', 'Plant-based', 'Salads', 'Sandwich', 'Sandwiches', 'Seafood', 'Soups',
              'Spanish', 'Steak', 'Subs', 'Sushi', 'Tea/coffee', 'Thai', 'Vegan', 'Vietnamese', 'Wine', 'Wings']

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        types = request.form.getlist('types')
        return render_template('main.html', categories=categories, restraunts=requests.get(f"http://localhost:5000/api?food_types={','.join(types)}").json())

    return render_template('main.html', categories=categories)



if __name__ == '__main__':
    app.run(debug=True, port=5001)
