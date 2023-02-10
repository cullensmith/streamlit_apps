import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib as plt
import chart_style

from weather import get_cell as cell, get_forecast as get_f

# def style_chart():
#     chart_style.set_style()
#     print('style is set')
    

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
            plt.pyplot.grid(True)
            forecast = get_f15(coordinates[0],coordinates[1])

            fig, ax = plt.pyplot.subplots()
            chart_style.set_style(fig)

            temp = st.select_slider(label='Check Specific Hour:',options=forecast['startTime'], format_func=lambda x: x.strftime('%A %b %d: %I%p') )
            st.write(f"Forecasted Temp: {forecast[forecast.startTime == temp]['temperature'].iloc[0]}")

            ax.plot(forecast['temperature'],linewidth=1.5)
            read_temp = forecast[forecast.startTime == temp]['number'].iloc[0]
            ax.plot(forecast['temperature'][:read_temp], linewidth=2, color='#ff7b7b', zorder=2)
            ax.scatter(forecast[forecast.startTime == temp]['startTime'].iloc[0], forecast[forecast.startTime == temp]['temperature'].iloc[0],color='#ff6b6b', zorder=3)
            rfdates = plt.dates.DateFormatter('%a')
            ax.xaxis.set_major_formatter(rfdates)
            st.pyplot(fig)
        except KeyError as e:
            st.write('There was an error, please click the map again. Thanks')
if __name__ == '__main__':
    main()
