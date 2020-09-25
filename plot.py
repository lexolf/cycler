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
    graph.set_ylim(df['Charge'].min()-0.33*df['Charge'].min(), df['Discharge'].max()+0.1*df['Discharge'].max())
    if "full" not in filename:
        df['Efficiency'] = df['Discharge']/df['Charge']/100
    df = df.drop(df[df['Efficiency'] < 0.2].index)
    df['Efficiency'].plot(secondary_y=True, marker='o', markersize=5)
    graph.right_ax.set_ylim(0,105)
    graph.right_ax.set_ylabel('Coulombic Efficiency / %')
    graph.set_xlabel("Cycle / N")
    graph.set_ylabel("Q / mA h g$""^{-1}$")
    h1, l1 = graph.get_legend_handles_labels()
    h2, l2 = graph.right_ax.get_legend_handles_labels()
    graph.legend(h1+h2, l1+l2, loc=4)
    graph.get_figure().savefig(os.path.join(pathlib.Path().absolute(),filename)+'.png', dpi=600)


def plot_record(file, filename, graphs):
    """Plots GCD curves"""
    df = pd.read_csv(file, delimiter="\t")
    df = df.rename(columns={'Vol': 'Potential', 'Cur': 'Current', 'Cap': 'Capacity', 'CmpCap': 'Specific Capacity'})
    df_gcd = df[['Step ID', 'Current', 'Specific Capacity', 'Potential']]
    df_gcd['Potential'] = df_gcd['Potential']/1000
    rest_steps = df_gcd[df_gcd['Current'] == 0].index
    df_gcd.drop(rest_steps, inplace=True)
    steps = df_gcd['Step ID'].unique()
    plt.style.use(['seaborn-colorblind', 'seaborn-paper'])
    graph = plt.figure()
    ax = graph.gca() # getting axes so they work as intended when plotting curves
    graph_title = 'GCD Curves for cell ' + filename.split("_")[0]
    for step in steps: 
        df_step = df_gcd.loc[df['Step ID'] == step]
        df_step.plot(ax=ax, x='Specific Capacity', y='Potential', colormap="plasma", title=graph_title)
    ax.legend(['Stability'])
    ax.set_xlabel("Q / mA h g$""^{-1}$")
    ax.set_ylabel("E / V")
    ax.get_figure().savefig(os.path.join(pathlib.Path().absolute(),filename)+'.png', dpi=600)

def csv_to_graph(file, graphs="all"):
    """Send csv's to respective renderers depending on type of data"""
    filename, file_extension = os.path.splitext(file) 
    if file_extension == '.csv': # extract data only from csv files
        if "cycle" in filename:
            plot_cycle(file, filename, graphs)
        elif "record" in filename:
            plot_record(file, filename, graphs)
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