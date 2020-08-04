from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np
import os
import platform
import covid_database as cd


class Window:
    def __init__(self, Top):
        self.top = Top
        self.top.title("Cool App")
        self.top.iconbitmap(os.getcwd() + "\Images\profile_pic.ico")
        self.top.geometry("200x405")
        self.label_list = []
        self.limit = 5
        self.positive = cd.positive_today()
        self.negative = cd.negative_today()
        self.total_test = cd.total_test_today()
        self.death = cd.death_today()

    def print_current_state_positive(self, index_list, name_list):
        if platform.system() == "Darwin":
            width = 255
            length = 90
        else:
            width = 200
            length = 81
        for label in self.label_list:
            label.grid_forget()
        self.label_list.clear()

        row_counter = 0
        column_counter = 0
        for counter, index in enumerate(index_list):
            if row_counter == self.limit:
                column_counter += 1
                row_counter = 0
            info_string = "{}:\n\tPositive cases: {}\n\tNegative cases: {}\n\tTotal Test Results: {}\n\tDeaths: {}".format(
                name_list[index],
                str(self.positive[index]),
                str(self.negative[index]),
                str(self.total_test[index]),
                str(self.death[index]),
            )
            self.label_list.append(
                Label(self.top, text=info_string, justify=LEFT))
            self.label_list[counter].grid(
                sticky=W, row=row_counter, column=column_counter
            )
            row_counter += 1

        self.top.geometry(
            "{}x{}".format((column_counter + 1) * width, self.limit * length)
        )
