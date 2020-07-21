from tkinter import *
import CovidNewWindow as cnw
import CovidFuntions as cf

#main
root, new_window = cf.create_app_base()

api = cf.current_state_api_request()
pop_data = cf.population_data()

positive_state = []
population_state = []
names_state = []
cf.print_current_state_positive(root, api)
cf.set_positive_population(positive_state, population_state, names_state, pop_data, api)

new_window.create_scatter_plot(population_state, positive_state, names_state)


root.mainloop()
