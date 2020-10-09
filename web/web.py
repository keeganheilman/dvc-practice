
# This is the starter code from our webteam.
# You should feel free to change anything you need to change
import pickle

import pandas as pd

from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# The web team will make this more secure in production.
app.config['SECRET_KEY'] = 'key'

app.debug = True
Bootstrap(app)


class FeatureForm(FlaskForm):
    mean_wind = FloatField('Wind Speed (MPH)', default=2)
    inches_precip = FloatField('Precipitation (inches)', default=0)
    is_weekday = SelectField(
        'Day Type',
        choices=[('weekday', 'Weekday'), ('weekend', 'Weekend')],
        default='weekday')


with open('../models/trip_duration_predictor.pkl', 'rb') as stream:
    model = pickle.load(stream)


@app.route('/', methods=['GET'])
def index():

    form = FeatureForm(request.args, meta={'csrf': False})
    if form.validate():
        user_submitted_features = {}
        for i in form:
            if i.name == 'is_weekday':
                user_submitted_features['is_weekday'] = i.data == 'weekday'
            else:
                user_submitted_features[i.name] = i.data

        user_df = pd.DataFrame(data=[user_submitted_features])
        user_df['is_weekday'] = user_df[
            'is_weekday'].astype(str).astype('category')

        prediction = round(model.predict(user_df)[0], 1)

    return render_template("form.html", form=form, prediction=prediction)


if __name__ == '__main__':
    app.run()

# Image Credit Anja Nachtweide
