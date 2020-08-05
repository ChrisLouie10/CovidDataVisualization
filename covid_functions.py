from tkinter import *
from PIL import ImageTk, Image
import requests
import json
import covid_new_window as cnw
from datetime import datetime
import os
import platform


# Creates two Top-level widgets and sets some default
# Returns both widgets
def create_app_base():
    root = Tk()
    root.title("Covid")
    root.iconbitmap(os.getcwd() + "\Images\profile_pic.ico")
    if platform.system() == "Darwin":
        root.geometry("500x500")
    else:
        root.geometry("420x480")

    top = Toplevel()
    new_window = cnw.Window(top)

    return (root, new_window)


# Returns a string of the current status of the Covid Tracking Project API
def covid_api_status():
    status = ""
    try:
        api_request = requests.get(
            "https://covidtracking.com/api/v1/status.json", timeout=3
        )
        api = json.loads(api_request.content)
        status = api["buildTime"]
        status = status.replace("T", " ").rstrip(".442Z") + "\n"
        return status
    except Exception as e:
        return "Error Occured"


# Prints the current positive values for each state
# widget is the Tkinter widget the current values will be printed to
# name_list is a list of all the states
# pos_list is the list of positive values for each state
def print_current_state_positive_label(widget, name_list, pos_list):
    row_counter = 0
    col_counter = 0
    label_list = []
    title = Label(widget, text="Positive Cases in Each State").grid(
        row=0, column=0, columnspan=3
    )
    for counter, (name_state, data_state) in enumerate(zip(name_list, pos_list)):
        info_string = name_state + ": " + str(data_state)
        Label(widget, text=info_string).grid(row=row_counter + 1, column=col_counter)
        row_counter += 1
        if row_counter == 19:
            row_counter = 0
            col_counter += 1
    last_update = Label(widget, text=covid_api_status())
    last_update.grid(row=27, column=0)
