import pandas as pd
import numpy as np


def get_data(input_file):
    print('Importing data from %s...' % (input_file))
    df = pd.read_csv(input_file)
    return df


def join_data(df_1, df_2):
    print('Joining data...')
    # assert len(df_1) == len(df_2), "DataFrames do not contain the same number of individuals"
    df_joined = df_1.join(df_2.set_index('date'), on ='date')
    assert len(df_joined) == len(df_1), "Joined DataFrames do not match along all respondent_ids"
    return df_joined


# def clean_data(df):
#     print('Cleaning data...')
#     df['birthdate'] = df['birthdate'].apply(lambda bdate: str(bdate).zfill(8))
#     df['birthdate'] = pd.to_datetime(df['birthdate'], format='%m%d%Y')
#     assert all(df.columns == ['respondent_id','name', 'address', 'phone', 'job', 'company', 'birthdate']), "Incorrect column names in the Pandas DataFrame."
#     return df


def export_data(df, output_file):
    print('Exporting data to %s...' % (output_file))
    df.to_csv(output_file,date_format='%Y-%m-%d', index=False)
    return 0


if __name__ == '__main__':
    print('Starting script...')
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('weather_info_file', help='Weather Info File')
    parser.add_argument('trips_info_file', help='Trips Info File')
    parser.add_argument('output_file', help='Output File')
    args = parser.parse_args()

    df_1 = get_data(args.weather_info_file)
    df_2 = get_data(args.trips_info_file)

    df = join_data(df_1, df_2)    
    # df_clean = clean_data(df)

    if (export_data(df, args.output_file) == 0):
        print('Completed successfully.')





