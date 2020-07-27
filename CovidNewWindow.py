from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np
import os


class Window:
    def __init__(self, Top):
        self.top = Top
        self.top.title('Cool App')
        self.top.iconbitmap(os.getcwd() + '\Images\profile_pic.ico')
        self.top.geometry("200x405")
        self.label_list = []
        self.limit = 5
    
    def print_current_state_positive(self, index_list, name_list, data_list):
        for label in self.label_list:
            label.grid_forget()
        self.label_list.clear()
        
        row_counter = 0
        column_counter = 0
        for counter, index in enumerate(index_list):
            if row_counter == self.limit:
                column_counter += 1
                row_counter = 0
            info_string = '{}:\n\tPositive cases: {}\n\tNegative cases: {}\n\tTotal Test Results: {}\n\tDeaths: {}'.format(name_list[index], 
                                                                                                                            str(data_list[index]['positive']), 
                                                                                                                            str(data_list[index]['negative']),
                                                                                                                            str(data_list[index]['total']),
                                                                                                                            str(data_list[index]['death'])
            )
            self.label_list.append(Label(self.top, text=info_string, justify=LEFT))
            self.label_list[counter].grid(sticky=W ,row=row_counter, column=column_counter)
            row_counter += 1

        self.top.geometry("{}x{}".format((column_counter + 1) * 200, self.limit * 81))
