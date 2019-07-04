import tkinter
from tkinter import *
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
import requests
import json
import ssl


# Test
# Test 1
def get_list(*args):
    global input_1, title1
    input_1 = e1.get()
    r = requests.get(f'https://www.metaweather.com/api/location/search/?query={input_1}')
    dict2 = json.loads(r.text)
    title1 = [d.get('title', None) for d in dict2]
    listbox.delete(0, END)
    for item in title1:
        listbox.insert(END, item)
    listbox.bind('<ButtonRelease-1>', select_item)

def select_item(event):
    index = listbox.curselection()[0]
    seltext = listbox.get(index)
    e1.delete(0, 50)
    e1.insert(0, seltext)

def retrieve_input():
    response = requests.get(f'https://www.metaweather.com/api/location/search/?query={input_1}')
    result = json.loads(response.text[1:-1])
    woeid = result.get("woeid")
    return woeid


def get_weather(woeid):
    global weather, max_temp, min_temp, date, w_image, weather1, max_temp1, min_temp1, date1, w_image1
    r1 = requests.get(f'https://www.metaweather.com/api/location/{woeid}/')
    result = json.loads(r1.text)
    weather_list = list()
    for weather in result['consolidated_weather']:
        weather_list.append(
        {
         'date': weather['applicable_date'],
         'weather': weather['weather_state_name'],
         'max_temp': weather['max_temp'],
         'min_temp': weather['min_temp'],
         'w_image': weather['weather_state_abbr']
         }
        )
    return weather_list

def execute_functions():
    woeid = retrieve_input()
    weather_list = get_weather(woeid)
    display_output(weather_list)
    weather_images(weather_list)


def weather_images(weather_list):
    context = ssl._create_unverified_context()
    row_i,column_i = 4,0
    for weather in weather_list:
        url = (f"https://www.metaweather.com/static/img/weather/png/64/{weather['w_image']}.png")
        img = urlopen(url, context=context)
        raw_data = img.read()
        img.close()
        image_w = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image_w)
        label = tkinter.Label(root, justify=tkinter.LEFT, image=photo)
        label.image = photo
        label.grid(row=row_i, column=column_i)
        column_i += 1
        if column_i > 2:
            column_i = 0
            row_i += 2
    label2 = tkinter.Label(root, height=5, width=10, text=(f"{input_1}"), font=(None, 25), anchor='w').grid(row=3, column=0)


def display_output(weather_list):
    row_i = 5
    column_i = 0
    for weather in weather_list:
        tkinter.Label(root, justify=tkinter.LEFT, height=10, width=30,text=(f"Date: {weather['date']}\nWeather Condition: {weather['weather']}\nMaximum Temperature: {str(int(weather['max_temp']))}\nMinimum Temperature: {str(int(weather['min_temp']))}")).grid(row=row_i, column=column_i)
        column_i += 1
        if column_i > 2:
            column_i = 0
            row_i += 3

root = tkinter.Tk()

myvar = tkinter.StringVar()
myvar.set('')

tkinter.Label(root, text = "Enter the City name").grid(row = 0)


e1 = tkinter.Entry(root, textvariable=myvar)
e1.grid(row = 0, column = 1)

listbox = tkinter.Listbox(root)
listbox.grid(row=0, column=3)

tkinter.Button(root, text = "Get Weather", command = execute_functions).grid(row = 1, column = 1)

root.title("Weather Application")
root.geometry("800x600")


myvar.trace('w', get_list)

root.mainloop()
