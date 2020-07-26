import matplotlib.pyplot as plt
import CovidNewWindow as cnw

class CovidGraph:

    def connect_window(self, window):
        self.window = window

    def update_annot(self, ind):

        # ind["ind"] is a list of indexes for all points under the curser

        pos = self.sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        #text = "{}, {}".format(" ".join([self.names[n] for n in ind["ind"]]),
        #                       " ".join(str([self.y_axis[n] for n in ind["ind"]])))
        #self.annot.set_text(text)
        self.annot.set_text(self.annotate_string(
            self.names, self.y_axis * 1000, ind["ind"]))
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
    
    def onclick(self, event):
        self.current_indexes_pressed = []
        if event.inaxes == self.ax:
            cont, ind = self.sc.contains(event)
            if cont: 
                self.current_indexes_pressed = ind['ind']
                self.window.print_current_state_positive(self.current_indexes_pressed, self.names, self.data_list)
        return self.current_indexes_pressed


    def create_scatter_plot(self, x_axis, y_axis, names, data_list):
        self.data_list = data_list
        self.names = names
        self.y_axis = y_axis
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
