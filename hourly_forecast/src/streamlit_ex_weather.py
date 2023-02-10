import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from weather import get_cell as cell, get_forecast as get_f


def display_map():
    map = folium.Map(location=[40.823740, -77.862548], zoom_start=12, scrollWheelZoom=False, tiles='CartoDB positron')
    st_map = st_folium(map, width=700, height=450)
    return st_map


def get_pos(lat,lng):
    return lat,lng

def get_f15(y,x):
    the_cell = cell(y,x)
    forecast = pd.DataFrame(get_f(the_cell))
    forecast['startTime'] = pd.to_datetime(forecast.startTime)
    forecast.index = forecast.startTime
    return forecast

def main():
    st.write('Hourly Forecast')
    map = display_map()

    if map['last_clicked'] is not None:
        coordinates = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
        try:
            forecast = get_f15(coordinates[0],coordinates[1])
            st.line_chart(forecast['temperature'], y = 'temperature')
            temp = st.select_slider(label='Check Specific Hour:',options=forecast['startTime'], format_func=lambda x: x.strftime('%A %b %d: %I%p') )
            st.write(f"forecasted temp: {forecast[forecast.startTime == temp]['temperature'].iloc[0]}")
        except KeyError:
            st.write('There was an error, please click the map again. Thanks')
if __name__ == '__main__':
    main()
