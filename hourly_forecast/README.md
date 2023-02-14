# Generic Web Application
## link: [Hourly Forecast](https://hourly-forecast.streamlit.app)

## Purpose
- Show basic funcitonality of a standalone python web app that utilizes an API request to populate a customized matplotlib chart depending on user selection

## Usage
- Click anywhere on the map
- Sends a request to weather.gov using their API
- Parses the json response, storing results in a pandas dataframe 
- Populates a line chart depicting the hourly forecasted temperature
- Drag the slider to select a specfic hour within the forecast

## To Do
- Aesthetics are currently an afterthought and need to be cleaned up
- Include additional selection methods
- Filterable precipitation window 

## Main libraries
- Python
- Streamlit
- Pandas
- Requests
- Matplotlib
- Folium
