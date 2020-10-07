import pandas as pd
import os
import pathlib
import matplotlib.pyplot as plt

def plot_record(file, filename, graphs, interval, start, end):
    """Plots GCD curves"""
    if interval == "":
        interval = 1
    if start == "":
        start = 0
    if end == "":
        end = 100
    print("Plotting each " + str(interval) + " cycle of " + filename + " from " + str(start) + " to " + str(end) + " cycles.")
    df = pd.read_csv(file, delimiter="\t")
    df = df.rename(columns={'Vol': 'Potential', 'Cur': 'Current', 'Cap': 'Capacity', 'CmpCap': 'Specific Capacity'})
    df_gcd = df[['Step ID', 'Current', 'Specific Capacity', 'Potential']]
    df_gcd['Potential'] = df_gcd['Potential']/1000 # convert from mV to V 
    rest_steps = df_gcd[df_gcd['Current'] == 0].index # select rest steps
    df_gcd.drop(rest_steps, inplace=True) # drop rest steps
    steps = df_gcd['Step ID'].unique() ########  there are multiple cells with the same step like -2-2-2-...-4-4-4-...-6-6-6- (rest steps were dropped previously),
    ###########################################  thus only every second step remains, so here the steps are grouped to plot each curve separately
    plt.style.use(['seaborn-colorblind', 'seaborn-paper'])
    graph = plt.figure()
    ax = graph.gca() # getting axes so they work as intended when plotting curves
    graph_title = 'GCD Curves for cell ' + filename.split("_")[0]
    i = 0 # to reindex steps 
    for step in steps: 
        i = i + 1 # indexing steps starting with 1
        df_step = df_gcd.loc[df['Step ID'] == step]
        df_step['Step ID'] = i
        if df_step['Current'].iloc[0] > 0: # assigning type of step based on current value
            step_type = "Charge"
        elif df_step['Current'].iloc[0] < 0:
            step_type = "Discharge"
        df_step['Step Type'] = step_type
        if i == 1:                          # set the type of first step for grouping (we may start with both charge and discharge steps)
            starting_step_type = df_step['Step Type'].iloc[0]
        if df_step['Step ID'].iloc[0] >= start*2 and df_step['Step ID'].iloc[0] <= end*2: # limit what is the upper range of cycle number plotted; 
                                                                                        #doubled because each cycle contains 2 steps
            if df_step['Step Type'].iloc[0] == starting_step_type: # plotting curves of first step type
                if((df_step['Step ID'].iloc[0]-1)%interval == 0): # -1 to take into account that we start from 1, not 0
                    df_step.plot(ax=ax, x='Specific Capacity', y='Potential', colormap="plasma", title=graph_title)
            elif df_step['Step Type'].iloc[0] != starting_step_type: # plotting curves of second step type
                if((df_step['Step ID'].iloc[0]-2)%interval == 0): # -2 to take into account that the STEP belongs to the same CYCLE as previous STEP
                    df_step.plot(ax=ax, x='Specific Capacity', y='Potential', colormap="plasma", title=graph_title)
    ax.legend(['Stability'])
    ax.set_xlabel("Q / mA h g$""^{-1}$")
    ax.set_ylabel("E / V")
    ax.get_figure().savefig(os.path.join(pathlib.Path().absolute(),filename)+'.png', dpi=600)

def send_files_to_plotter(path):
    """Plot each file in path"""
    if path=="":
      path = os.listdir(pathlib.Path().absolute())
    for file in path:
        csv_to_graph(file, graphs="all")

def csv_to_graph(file, graphs="all"):
    """Send csv's to respective renderers depending on type of data"""
    filename, file_extension = os.path.splitext(file) 
    if file_extension == '.csv': # extract data only from csv files
        if "record" in filename:
            start = int(input("Enter the index of the first cycle to plot (press 'Enter' to use the default value 0)"))
            end = int(input("Enter the index of the last cycle to plot  (press 'Enter' to use the default value 100)"))
            interval = int(input("Enter the interval used for plotting cycles (press 'Enter' use the default value 1)"))
            plot_record(file, filename, graphs, interval, start, end)
    else:
        print("Skipping non-csv file...")

current_path_contents = os.listdir(pathlib.Path().absolute()) # get files in current folder
send_files_to_plotter(current_path_contents)