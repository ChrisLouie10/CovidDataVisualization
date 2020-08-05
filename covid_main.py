import covid_new_window as cnw
import covid_graph as cg
import covid_functions as cf
import covid_database as cd

# main

# Create Tkinter widgets and Update database
root, new_window = cf.create_app_base()
cd.update_database()

# Show data/Create graphs

cf.print_current_state_positive_label(root, cd.state_names(), cd.positive_today())

pos_pop_graph = cg.CovidGraph()
pos_pop_graph.connect_window(new_window)
pos_pop_graph.create_scatter_plot(
    cd.state_population(), cd.positive_today(), cd.state_names()
)


root.mainloop()
