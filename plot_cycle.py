import pandas as pd
import os
import pathlib
import matplotlib.pyplot as plt

def plot_cycle(file, filename, graphs):
    """Plots charge/discharge capacity and coulombic effeciency vs cycle"""
    df = pd.read_csv(file, delimiter="\t")
    df = df.rename(columns={"RCap_Chg":"Charge","RCap_DChg":"Discharge"})
    graph_title = filename.split("_")[0]+ " cell stability"
    plt.style.use(['seaborn-colorblind', 'seaborn-paper'])
    df = df.drop(df[df['Charge'] == 0].index)  ### skipping values of charge and discharge that are 0 
    df = df.drop(df[df['Discharge'] == 0].index) # due to exporting issues (may be harmful!)
    graph = df.plot(x='Cycle ID', y=['Charge', 'Discharge'], marker="o", markersize=5, title=graph_title)
    graph.set_ylim(df['Charge'].min()*0.67, df['Discharge'].max()*1.1) # setting limits so that the graph fits better
    if "full" not in filename:
        df['Efficiency'] = df['Discharge']/df['Charge']/100
    df = df.drop(df[df['Efficiency'] < 0.2].index)
    df['Efficiency'].plot(x='Cycle ID', secondary_y=True, marker='o', markersize=5)
    graph.right_ax.set_ylim(0,df['Efficiency'].max()*1.1)
    graph.right_ax.set_ylabel('Coulombic Efficiency / %')
    graph.set_xlabel("Cycle / N")
    graph.set_ylabel("Q / mA h g$""^{-1}$")
    h1, l1 = graph.get_legend_handles_labels()
    h2, l2 = graph.right_ax.get_legend_handles_labels()
    graph.legend(h1+h2, l1+l2, loc=4)
    graph.get_figure().savefig(os.path.join(pathlib.Path().absolute(),filename)+'.png', dpi=600)

def csv_to_graph(file, graphs="all"):
    """Send csv's to respective renderers depending on type of data"""
    filename, file_extension = os.path.splitext(file) 
    if file_extension == '.csv': # extract data only from csv files
        if "cycle" in filename:
            plot_cycle(file, filename, graphs)
    else:
        print("Skipping non-csv file...")

def send_files_to_plotter(path):
    """Plot each file in path"""
    if path=="":
      path = os.listdir(pathlib.Path().absolute())
    for file in path:
        csv_to_graph(file, graphs="all")

current_path_contents = os.listdir(pathlib.Path().absolute()) # get files in current folder
send_files_to_plotter(current_path_contents)