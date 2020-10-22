
**Note**: Run all commands from the base directory of the project for this assignment.

## Setup

Begin by starting up the development web server with this command, in a terminal:

  - `python web/web.py`

If you get a "FileNotFoundError" error when you load the web app, you will need to run the DVC pipeline to generate thep prediction model. (This error is to be expected on your first run.)

  - `dvc repro`

With the prediction model in place. Stop the Flask server (Ctrl-C) and start it again ("flask run"). You should now get nice interface in the browser that will let you try different feature values and see the prediction from the model.

## Task

Your assignment is to update the pipeline and web application to add temperature data to the prediction model.

### 1. Examine original code

Start by examining the dvc.yml file to understand the pipeline in its original state. Then look at web/web.py to see how the form is defined. Note that the form fields are defined in the class "FeatureForm" and the property names in that class match the feature names in the prediction model.

### 2. Create combine_temp.py
Now create a new step in the pipeline by adding a script to the "scripts" directory, this new script should be named "combine_temp.py". It must take three arguments on the command line:

  - trips_without_temp_clean
  - temp_by_date
  - trips_with_all_weather

It will be called with this command:

  ```
  python3 scripts/combine_temp.py \
    data/trips_without_temp_clean.csv \
    data/temp_by_date.csv \
    data/trips_with_all_weather.csv
  ```

The script will take join the first two files based on date, then write the trips_with_all_weather file. This file will be very similiar to the trips_without_temp_clean file, the only difference is that it will include the temp_min and temp_max columns.

### 3. Update train_trip_duration_predictor.py

Update the train_trip_duration_predictor.py script to use the new features in the trips_with_all_weather file. Adding these features should improve the model's accuracy.

### 4. Update dvc.yaml

After combine_temp.py is working, update the DVC pipeline:

  1. Add a step to generate the data/trips_with_all_weather.csv
  2. Update the last step "train_trip_duration_predictor" to use the new version of train_trip_duration_predictor.py

Once this is done the command `dvc repro` should be using the new trips_with_all_weather and the updated train_trip_duration_predictor.py to train a new version of the model in trip_duration_predictor.pkl.

### 4. Add the temperature fields to the web application

With the new model in place, the web app will start giving you an error because the number of features that the application is trying to predict with no longer matches the number of features in the model.

Update the application to add the new fields. This should just be a matter of adding **temp_min** and **temp_max** properties to the FeatureForm class. (The new fields will look very similar to the mean_wind and inches_precip fields.)
