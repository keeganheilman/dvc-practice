import json
import pickle

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


def train(trips):
    X = trips.drop(['trip_duration_minutes'], axis=1)
    X['is_weekday'] = X['is_weekday'].astype(str).astype('category')
    y = trips['trip_duration_minutes'].astype(int)

    numeric_features = [
        'mean_wind',
        'inches_precip',
    ]
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_features = [
        'is_weekday',
    ]
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', LinearRegression())])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1)

    model.fit(X_train, y_train)

    metrics = {
        'train_data': {
            'score': model.score(X_train, y_train),
            'mae': mean_absolute_error(y_train, model.predict(X_train)),
        },
        'test_data': {
            'score': model.score(X_test, y_test),
            'mae': mean_absolute_error(y_test, model.predict(X_test)),
        },
    }

    return metrics, model


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='cleaned trips data file (CSV)')
    parser.add_argument('output_file', help='trained model (PKL)')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='display metrics',
    )
    args = parser.parse_args()

    input_data = pd.read_csv(
        args.input_file,
        parse_dates=['date'],
    )

    metrics, model = train(input_data)

    if args.verbose:
        print(json.dumps(metrics, indent=2))

    with open(args.output_file, 'wb+') as out:
        pickle.dump(model, out)
