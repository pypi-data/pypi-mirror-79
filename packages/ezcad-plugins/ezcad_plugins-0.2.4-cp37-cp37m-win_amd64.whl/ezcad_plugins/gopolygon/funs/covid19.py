# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
https://opensource.com/article/20/4/python-map-covid-19
"""

import pandas as pd
try:
    import pycountry
except ImportError:
    print("WARNING cannot import pycountry")
# import plotly.express as px


def covid19(fn=None):
    if fn is None or fn == 'default':
        fn = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
    # fn = r"C:\Users\xinfa\Downloads\countries-aggregated.csv.txt"
    df = pd.read_csv(fn)

    # Replace country name for looking for ISO alpha-3 code
    replace = {
        "Burma": "Myanmar",
        "Korea, South": "Korea, Republic of",
        "Korea, North": "Korea, Democratic People's Republic of",
        "Congo (Brazzaville)": "Republic of the Congo",
        "Congo (Kinshasa)": "Congo, The Democratic Republic of the",
        "Laos": "Lao",
        "Taiwan*": "Taiwan",
    }
    df.Country = df.Country.replace(replace)

    list_countries = df['Country'].unique().tolist()
    # print(list_countries)  # Uncomment to see list of countries
    d_country_code = {}  # To hold the country names and their ISO
    for country in list_countries:
        try:
            country_data = pycountry.countries.search_fuzzy(country)
            # country_data is a list of objects of class pycountry.db.Country
            # The first item  ie at index 0 of list is best fit
            # object of class Country have an alpha_3 attribute
            country_code = country_data[0].alpha_3
            d_country_code.update({country: country_code})
        except:
            print('could not add ISO 3 code for ->', country)
            # If could not find country, make ISO code ' '
            d_country_code.update({country: ' '})
    # print(d_country_code)

    update = {
        'Nigeria': 'NGA',
        'Niger': 'NER',
        'Serbia': 'SRB',
        'Kosovo': 'UNK',
    }
    d_country_code.update(update)

    # create a new column iso_alpha in the df
    # and fill it with appropriate iso 3 code
    for k, v in d_country_code.items():
        df.loc[(df.Country == k), 'iso_alpha3'] = v

    # print(df.head)  # Uncomment to confirm that ISO codes added
    # fig = px.choropleth(data_frame=df,
    #                     locations="iso_alpha",
    #                     color="Confirmed",  # value in column 'Confirmed' determines color
    #                     hover_name="Country",
    #                     color_continuous_scale='RdYlGn',  # color scale red, yellow green
    #                     animation_frame="Date")
    # fig.show()

    return df


def main():
    df = covid19()
    print(df.shape)
    print(df[df.iso_alpha3 == 'CHN'].shape)
    df2 = df[df.Date == '2020-05-27']
    print(df2.shape)
    df3 = df2[df2.Confirmed != 0]
    print(df3.shape)


if __name__ == '__main__':
    main()
