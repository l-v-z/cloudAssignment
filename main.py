import json

import streamlit as st
import requests

st.set_page_config(layout='wide')

st.title('Cloud Computing & SOA')
st.title('')
temp_unit = st.selectbox("Select Preferred Temperature Unit", ["Celsius", "Fahrenheit"])
st.title('')

def get_static_weather(city):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=48265ba00d3c3245c97646210e7623fb")
    return response.json()

def get_static_exchange_rate():
    response = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key=21587484e81c74956b8697fd7c5cf5c6&base=EUR&symbols=USD,GBP,JPY")
    return response.json()

# AWS Lambda Functions
def get_dynamic_weather(city):
    try:
        response = requests.get(f"https://h442krk5h1.execute-api.eu-north-1.amazonaws.com/weather?city={city}")

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def get_dynamic_exchange_rate(currencies):
    try:
        response = requests.get(f"https://nhe8p2mh75.execute-api.eu-north-1.amazonaws.com/exchange?currencies={currencies}")

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def convert_temperature(temp_k, unit):
    if unit == 'Celsius':
        return f"{temp_k - 273.15:.2f} °C"
    elif unit == 'Fahrenheit':
        return f"{(temp_k * 9/5) - 459.67:.2f} °F"
    else:
        return f"{temp_k} K"  # Default to Kelvin if unit is not recognized

def format_weather_data(weather_data, temp_unit):
    try:
        main = weather_data['main']
        weather = weather_data['weather'][0]
        description = weather['description'].capitalize()

        # Map of keywords to emojis
        emoji_map = {
            'sun': '☀️',
            'clear': '🌟',
            'cloud': '☁️',
            'rain': '🌧️',
            'thunder': '⚡',
            'snow': '❄️',
            'mist': '🌫️',
            'fog': '🌁'
        }

        weather_emoji = ''
        for keyword, emoji in emoji_map.items():
            if keyword in description.lower():
                weather_emoji = emoji
                break

        formatted_data = {
            'Temperature': convert_temperature(main['temp'], temp_unit),
            'Feels Like': convert_temperature(main['feels_like'], temp_unit),
            'Weather': f" {weather['main']} {weather_emoji} ",
            'Description': weather['description'].capitalize()
        }
        return formatted_data
    except KeyError:
        return "Invalid data format"

def format_exchange_rates(exchange_data):
    try:
        rates = exchange_data['rates']
        return {currency: rate for currency, rate in rates.items()}
    except KeyError:
        return "Invalid data format"

def get_available_currencies():
    response = requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=21587484e81c74956b8697fd7c5cf5c6")
    if response.status_code == 200:
        data = response.json()
        return list(data['rates'].keys())
    else:
        return ["Error fetching currencies"]

@st.cache_data
def load_city_list():
    with open('city.list.json', 'r', encoding='utf-8') as file:
        city_data = json.load(file)
        city_list = sorted((city['name'], city['country']) for city in city_data)
        formatted_city_list = [f"{name}, {country}" for name, country in city_list]
        return formatted_city_list

st.title('')
col1, col2, col3, col4 = st.columns(4)

with col1:
    static_city = 'Limassol'
    st.subheader(f"Weather in {static_city}")
    st.divider()
    weather_info = get_static_weather(static_city)
    formatted_weather = format_weather_data(weather_info, temp_unit)
    for key, value in formatted_weather.items():
        st.metric(label=key, value=value)

with col2:
    st.subheader("Exchange Rates against EUR")
    st.divider()
    exchange_rates = get_static_exchange_rate()
    formatted_rates = format_exchange_rates(exchange_rates)
    for currency, rate in formatted_rates.items():
        st.metric(label=f"EUR to {currency}", value=rate)

with col3:
    city_options = load_city_list()
    st.subheader(f"Weather in selected city")
    st.divider()
    selected_city = st.selectbox("Search for a city", [None] + city_options, index=0,
                                 format_func=lambda x: '' if x is None else x, key="dynamic_weather")
    if selected_city:
        dynamic_weather = get_dynamic_weather(selected_city)
        st.subheader(f"Weather in {selected_city}")
        formatted_dynamic_weather = format_weather_data(dynamic_weather, temp_unit)
        for key, value in formatted_dynamic_weather.items():
            st.metric(label=key, value=value)

with col4:
    currency_options = get_available_currencies()
    st.subheader(f"Exchange Rates against euro")
    st.divider()
    selected_currencies = st.multiselect("Select one or more currencies", currency_options,
                                         key="dynamic_exchange")
    currencies_string = ','.join(selected_currencies)

    if currencies_string:
        dynamic_exchange_rates = get_dynamic_exchange_rate(currencies_string)
        st.subheader("Dynamic Exchange Rates")
        formatted_dynamic_rates = format_exchange_rates(dynamic_exchange_rates)
        for currency, rate in formatted_dynamic_rates.items():
            st.metric(label=f"EUR to {currency}", value=rate)
