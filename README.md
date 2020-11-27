

# CovidDataVizualization  

Small program that a chart Covid data taken from The COVID Tracking Project to see recent data.

![Program Display](/Images/ProgramDisplay.png)

The program creates three windows with different purposes.

The first window shows the current positive cases for each state/territory and the data of its last update at the bottom. Skipping the second graph for now, the third graph shows a chart of the current positive cases relative to state population. The line represents the countries average positive cases to population size. The graph is interactive, meaning hovering your mouse over parts of the graph shows the the name, positive cases, and percentage of positive cases for the state the mouse is hovering over. Clicking on points shows the current positive, negative, and total cases along with the number of deaths on the second window. The second window automatically adjusts to fit the size of the data. 

![Interactive Graph](/Images/InteractiveGraph.png)

The program uses The COVID Tracking Projects to obtain data. The data is taken in as a json object, then converted and stored into a sqlite database. The choice of sqlite over other databases is because the data is small an only needs runs with the program. Data is stored in three tables to use the least amount of space while keeping things organized. This means not repeating data, especially strings, using the least amount of tables. The thought process can be seen below.

![Database Diagram](/Images/DatabaseIdeas.png)

### To-Do List

Create graphs showing long-term data of a selected state.

Highlight state on graph showing in the new window .

Implement blitting.

Remove updating from happenning if all the data is there.


