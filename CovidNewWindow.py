from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np


class Window:
    def __init__(self, Top):
        self.top = Top
        self.top.title('Cool App')
        self.top.iconbitmap('E:\Python\AppTutorial\Images\profile_pic.ico')
        self.top.geometry("400x400")

    def update_annot(self, ind):

        # ind["ind"] is a list of indexes for all points under the curser

        pos = self.sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        #text = "{}, {}".format(" ".join([self.names[n] for n in ind["ind"]]),
        #                       " ".join(str([self.y_axis[n] for n in ind["ind"]])))
        #self.annot.set_text(text)
        self.annot.set_text(self.annotate_string(
            self.names, self.y_axis, ind["ind"]))
        # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        # annot.get_bbox_patch().set_alpha(0.4)

    def annotate_string(self, val1, val2, indexes):
        string = ''
        for index in indexes:
            string = string + str(val1[index]) + ', ' + str(val2[index]) + '\n'
        string = string.rstrip("\n")
        return string

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.sc.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()

    def create_scatter_plot(self, x_axis, y_axis, names):
        self.names = names
        self.y_axis = y_axis
        self.fig, self.ax = plt.subplots()
        self.sc = self.ax.scatter(x_axis, y_axis)

        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"))
        self.annot.set_visible(False)

        self.ax.set_xlabel('State Population (in 100,000 people)')
        self.ax.set_ylabel('Positive Cases (in 1000)')
        self.ax.set_title('Positive Cases In Each State')

        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        plt.show()
