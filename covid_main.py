import covid_new_window as cnw
import covid_graph as cg
import covid_functions as cf
import covid_database as cd

# main
root, new_window = cf.create_app_base()
cd.update_database()

positive_state = cd.positive_today()
print(positive_state)
population_state = cd.state_population()
print(population_state)
names_state = cd.state_names()
print(names_state)

cf.print_current_state_positive_label(root, names_state, positive_state)

pos_pop_graph = cg.CovidGraph()
pos_pop_graph.connect_window(new_window)
pos_pop_graph.create_scatter_plot(population_state, positive_state, names_state)


root.mainloop()
