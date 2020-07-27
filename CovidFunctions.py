from tkinter import *
from PIL import ImageTk, Image
import requests
import json
import CovidNewWindow as cnw
from datetime import datetime
import os

def create_app_base():
    root = Tk()
    root.title('Cool App')
    root.iconbitmap(os.getcwd() + '\Images\profile_pic.ico')
    root.geometry("400x500")

    top = Toplevel()
    new_window = cnw.Window(top)

    # scrollbar = Scrollbar(root)
    # scrollbar.pack(side=RIGHT, fill=Y)

    return (root, new_window)

def current_state_data_list_request():
    try:
        api_request_state_current = requests.get(
            "https://covidtracking.com/api/v1/states/current.json", timeout=3)
        api = json.loads(api_request_state_current.content)

        f = open("CovidData.txt", "w")
        f.write(json.dumps(api, indent=4))
        f.close()
    except Exception as e:
        print('Error...')

        f = open("CovidData.txt")
        api = json.loads(f.read())
        f.close()

    return api

def covid_api_status():
    status = ''
    try: 
        api_request = requests.get("https://covidtracking.com/api/v1/status.json", timeout=3)
        api = json.loads(api_request.content)
        status = api['buildTime']
        status = status.replace('T', ' ').rstrip('.442Z') + '\n'
        return status
    except Exception as e:
        return 'Error Occured'


def population_data():
    p = open("USPopulation.txt", 'r')
    pop_data = json.loads(p.read())
    return pop_data

def print_current_state_positive(root, api):
    print_info = ''
    for state in api:
        print_info += state['state'] + ": " + str(state['positive']) + "\n"
    print_info += covid_api_status()
    my_label = Label(root, text=print_info)
    my_label.pack()


def print_current_state_positive_label(widget, name_list, data_list):
    row_counter = 0
    col_counter = 0
    label_list = []
    title = Label(widget, text='Positive Cases in Each State').grid(
        row=0, column=0, columnspan=3)
    # title.grid(row=0, column=0)
    for counter, (name_state, data_state) in enumerate(zip(name_list, data_list)):
        info_string = name_state['state'] + ': ' + str(data_state['positive'])
        # label_list.append(Label(widget, text=info_string))
        # label_list[counter].grid(row=row_counter+1, column=col_counter)
        Label(widget, text=info_string).grid(
            row=row_counter+1, column=col_counter)
        row_counter += 1
        if row_counter == 19:
            row_counter = 0
            col_counter += 1
    last_update = Label(widget, text=covid_api_status())
    last_update.grid(row=27, column=0)


def set_positive_population(positive_state, population_state, names_state, pop_data, api):
    for population, positive in zip(pop_data, api):
        population_state.append(population['population'] / 100000)
        positive_state.append(positive['positive'] / 1000)
        names_state.append(population['state'])
        

