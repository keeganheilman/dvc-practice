
# This is the starter code from our webteam.
# You should feel free to change anything you need to change
import pickle

import pandas as pd


# This is the starter code from our webteam.
# You should feel free to change anything you need to change

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'  ## The web team will make this more secure in production
app.debug = True
Bootstrap(app)
#provide a list of form fields that your model will need
features = {'feature_name':'Displayname', 'feature_2':'Displayname2'}
class form(FlaskForm):
    pass
class feature_form(FlaskForm):
    """Create temp form."""
    for i in features:
        setattr(FlaskForm, i, StringField(features[i],[
            DataRequired()]))

model = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    form = feature_form()
    if form.validate_on_submit():
        user_submitted_features = {}
        for i in form:
            if i.name == 'csrf_token':
                continue
            user_submitted_features[i.name] = i.data
        # You can use the dictionary user_submitted_features and pass to your model.
        # you should do that here and return a sentence below.
        return render_template('results.html', msg = "This will be displayed with after a user submits your form, run your model and put something here")
    return render_template("form.html", form=form)


if __name__ == '__main__':
    app.run()




#Image Credit Anja Nachtweide
