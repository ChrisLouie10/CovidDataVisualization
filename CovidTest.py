import CovidNewWindow as cnw
import CovidGraph as cg
import CovidFuntions as cf

#main
root, new_window = cf.create_app_base()

data_list = cf.current_state_data_list_request()
pop_list = cf.population_data()

positive_state = []
population_state = []
names_state = []
cf.set_positive_population(positive_state, population_state, names_state, pop_list, data_list)

cf.print_current_state_positive_label(root, pop_list, data_list)

pos_pop_graph = cg.CovidGraph()
pos_pop_graph.connect_window(new_window)
pos_pop_graph.create_scatter_plot(population_state, positive_state, names_state, data_list)


root.mainloop()
