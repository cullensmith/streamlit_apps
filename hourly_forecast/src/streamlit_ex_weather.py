import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib as plt
import chart_style
import time
from weather import get_cell as cell, get_forecast as get_f


def get_f15(y,x):
    # retrieve the grid values from the custom weather module
    the_cell = cell(y,x)
    # using the values returned above call the function to retrieve the weather forecast data utilizing the site's api
    # convert the incoming json to a pandas dataframe for easier manipulation later
    forecast = pd.DataFrame(get_f(the_cell))
    forecast['startTime'] = pd.to_datetime(forecast.startTime)
    forecast.index = forecast.startTime
    return forecast

def construct_matplotlib_chart(coordinates, ctr):
    try:
        plt.pyplot.grid(True)
        forecast = get_f15(coordinates[0],coordinates[1])

        fig, ax = plt.pyplot.subplots()
        chart_style.set_style(fig)

        temp = st.select_slider(label='Drag the slider to target a specific time:',options=forecast['startTime'], format_func=lambda x: x.strftime('%A %b %d: %I%p') )
        st.write(f"Forecasted Temp: {forecast[forecast.startTime == temp]['temperature'].iloc[0]}")

        ax.plot(forecast['temperature'],linewidth=1.5)
        read_temp = forecast[forecast.startTime == temp]['number'].iloc[0]
        ax.plot(forecast['temperature'][:read_temp], linewidth=2, color='#ff7b7b', zorder=2)
        ax.scatter(forecast[forecast.startTime == temp]['startTime'].iloc[0], forecast[forecast.startTime == temp]['temperature'].iloc[0],color='#ff6b6b', zorder=3)
        rfdates = plt.dates.DateFormatter('%a')
        ax.xaxis.set_major_formatter(rfdates)
        st.pyplot(fig)
    except KeyError as e:
        ctr += 1
        if ctr < 4:
            # Sometimes the api gets hung up resuting in KeyError
            # In those cases return an error message
            time.sleep(2)
            construct_matplotlib_chart(coordinates, ctr)
        else:
            st.write('There was an error contacting the weather.gov server and it timed out, please click the map again.\nThanks!')

def main():
    ctr = 0
    st.write("Clicking on the map below will return a chart representing the locations hourly forecast for the next week. \n It's retrieving that information from weather.gov's API and is limited to the US at the moment.")
    st.write('- As this is just proof of concept the layout is an afterthough and the streamlit_folium package can be a bit tempermental')
    col1, col2 = st.columns(2)

    with col1:
        if 'coordinates' not in st.session_state:
            st.session_state['coordinates'] = (40.823740, -77.862548)

        map = folium.Map(location=[st.session_state.coordinates[0],st.session_state.coordinates[1]], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
        if 'themap' not in st.session_state:
            st.session_state.themap = st_folium(map, key='init', height=0)

        st.session_state.fg = folium.FeatureGroup(name = 'dots')
        st.session_state.fg.add_child(
            folium.CircleMarker(location=[st.session_state.coordinates[0],st.session_state.coordinates[1]],
                                radius=2,
                                weight=5)
            ).add_child(
            folium.CircleMarker(location=[map.location[0],map.location[1]],
                                radius=8,
                                weight=2)
            )

        try:
            if st.session_state.themap['last_clicked']:
                st.session_state.fg = folium.FeatureGroup(name = 'newdots')
                st.session_state.fg.add_child(
                    folium.CircleMarker(location=[st.session_state.themap['last_clicked']['lat'],st.session_state.themap['last_clicked']['lng']],
                                        radius=1.75,
                                        weight=5)
                    ).add_child(
                    folium.CircleMarker(location=[st.session_state.themap['last_clicked']['lat'],st.session_state.themap['last_clicked']['lng']],
                                        radius=8,
                                        weight=2)
                    )
        except TypeError:
            print(f"themap: {st.session_state.themap['last_clicked']['lat']}")
            print('came through as None')

        st.session_state.themap = st_folium(map,key='new',feature_group_to_add=st.session_state.fg, center=st.session_state.themap['last_clicked'], height=450)
        st_folium(map,key='new',feature_group_to_add=st.session_state.fg, center=st.session_state.themap['last_clicked'], height=0)

        try:
            coords = [st.session_state.themap['last_clicked']['lat'],st.session_state.themap['last_clicked']['lng']]
        except TypeError:
            coords = st.session_state['coordinates']
    with col2:
        construct_matplotlib_chart(coords, ctr)

if __name__ == '__main__':
    main()