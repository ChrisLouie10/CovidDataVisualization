import matplotlib.pyplot as plt
import covid_new_window as cnw
import copy


class CovidGraph:

    def connect_window(self, window):
        self.window = window

    def update_annot(self, ind):
        # ind["ind"] is a list of indexes for all points under the curser
        pos = self.sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        self.annot.set_text(self.annotate_string(
            self.names, self.y_axis * 1000, ind["ind"]))

    def annotate_string(self, val1, val2, indexes):
        string = ''
        for index in indexes:
            string = string + str(val1[index]) + ', ' + \
                str(val2[index]) + ', ' + \
                "{:.2f}%".format(
                    self.y_axis[index] / self.x_axis[index] * 100) + '\n'
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

    def onclick(self, event):
        self.current_indexes_pressed = []
        if event.inaxes == self.ax:
            cont, ind = self.sc.contains(event)
            if cont:
                self.current_indexes_pressed = ind['ind']
                self.window.print_current_state_positive(
                    self.current_indexes_pressed, self.names)
        return self.current_indexes_pressed

    def create_scatter_plot(self, x_axis, y_axis, names):
        self.names = names
        self.x_axis = copy.deepcopy(x_axis)
        self.y_axis = copy.deepcopy(y_axis)
        x_axis = [x/100000 for x in x_axis]
        y_axis = [y/1000 for y in y_axis]
        self.fig, self.ax = plt.subplots()
        self.sc = self.ax.scatter(x_axis, y_axis)

        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"))
        self.annot.set_visible(False)

        self.ax.set_xlabel('State Population (in 100,000 people)')
        self.ax.set_ylabel('Positive Cases (in 1000)')
        self.ax.set_title('Positive Cases In Each State')

        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        self.fig.canvas.mpl_connect("button_press_event", self.onclick)

        plt.show()
