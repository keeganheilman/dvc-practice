import pandas as pd


def clean(input_file):
    df = pd.read_csv(
            input_file,
            parse_dates=['date'],
    )

    # round trip_duration_minutes
    df['trip_duration_minutes'] = df['trip_duration_minutes'].round(2)

    # create boolean column for weekday
    df['is_weekday'] = df['day_of_week_type'].apply(
        lambda x: x == 'WEEKDAY')

    df = df.drop(['day_of_week_type'], axis=1)

    return df


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_file', help='the raw trips without temp file (CSV)')
    parser.add_argument(
        'output_file', help='the clean trips without temp file (CSV)')
    args = parser.parse_args()

    clean = clean(args.input_file)
    clean.to_csv(args.output_file, index=False)
