
# This is the starter code from our webteam.
# You should feel free to change anything you need to change
import pickle

import pandas as pd


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'  ## The web team will make this more secure in production
app.debug = True
Bootstrap(app)

#provide a list of form fields that your model will need
features = {
    'mean_wind': 'Wind Speed (MPH)',
    'inches_precip': 'Precipitation (inches)',
}


class feature_form(FlaskForm):
    """Create temp form."""
    for i in features:
        setattr(FlaskForm, i, StringField(features[i],[
            DataRequired()]))


with open('models/trip_duration_predictor.pkl', 'rb') as stream:
    model = pickle.load(stream)


@app.route('/', methods=['GET'])
def index():
    prediction = '--'  # set a placeholder string for the pridiction value
    form = feature_form(request.args, meta={'csrf': False})

    if form.validate():
        user_submitted_features = {
           field.name: field.data for field in form
        }

        # create a DataFrame with the user's input
        user_df = pd.DataFrame(data=[user_submitted_features])

        # use the user_df to get a prediction, and clean it up for the interface
        prediction = round(model.predict(user_df)[0], 1)

    return render_template(
        "form.html", form=form,
        msg='Predicted Trip Duration: ' + str(prediction) + ' minutes')


if __name__ == '__main__':
    app.run()




#Image Credit Anja Nachtweide
