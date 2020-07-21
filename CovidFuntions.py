from tkinter import *
from PIL import ImageTk, Image
import requests
import json
import CovidNewWindow as cnw

def create_app_base():
    root = Tk()
    root.title('Cool App')
    root.iconbitmap('E:\Python\AppTutorial\Images\profile_pic.ico')
    root.geometry("400x850")

    top = Toplevel()
    new_window = cnw.Window(top)

    return (root, new_window)

def current_state_api_request():
    try:
        api_request = requests.get(
            "https://covidtracking.com/api/v1/states/current.json", timeout=3)
        api = json.loads(api_request.content)

        f = open("CovidData.txt", "w")
        f.write(json.dumps(api, indent=4))
        f.close()
    except Exception as e:
        print('Error...')

        f = open("CovidData.txt")
        api = json.loads(f.read())
        f.close()

    return api

def population_data():
    p = open("USPopulation.txt", 'r')
    pop_data = json.loads(p.read())
    p.close()
    return pop_data

def print_current_state_positive(root, api):
    print_info = ''
    for state in api:
        print_info += state['state'] + ": " + str(state['positive']) + "\n"

    my_label = Label(root, text=print_info)
    my_label.pack()

def set_positive_population(positive_state, population_state, names_state, pop_data, api):
    for population, positive in zip(pop_data, api):
        population_state.append(population['population'] / 100000)
        positive_state.append(positive['positive'] / 1000)
        names_state.append(population['state'])
        

