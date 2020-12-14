import pandas as pd
import os
import pathlib

# This script needs xlrd!

def record_to_csv(file, filename, mode):
    """Convert Record sheets to csv file"""
    excel_file = pd.read_excel(file, sheet_name=None) # read the file
    df = pd.DataFrame() # create DataFrame to store data
    for name, sheet in excel_file.items(): 
        sheet['sheet'] = name # for each sheet append a column entitled with sheet label
        if "Record__" in f'{name}': # if it is a record sheet, append it to the main DataFrame
            header = sheet.iloc[0]
            sheet.columns = header
            sheet = sheet[1:]              
            df = pd.concat([df, sheet], ignore_index=True, sort=False)
        elif "Record" in f'{name}': # if it is a single record sheet, append it to the main DataFrame
            header = sheet.iloc[0]
            sheet.columns = header
            sheet = sheet[1:]               
            df = pd.concat([df, sheet], ignore_index=True, sort=False)
        elif "record_" in f'{name}':
            df = pd.concat([df, sheet], ignore_index=True, sort=False)
        elif "record" in f'{name}': 
            df = pd.concat([df, sheet], ignore_index=True, sort=False)
        else:
            print("Skipping non-record sheet")
    df = df.rename(columns={'Voltage': 'Vol', 'Current': 'Cur', 'Capacity': 'Cap', 'Capacity Density': 'CmpCap'}) # would rather work further with the same format
    df.reset_index(inplace=True, drop=True) # reset index so that it is cumulative throughout merged sheets
    if "__" in filename:
        filename = filename[:filename.index("__")]
        if mode=="full":
            df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_record_full'+'.csv', mode='a', header=False, index=False, sep="\t") # save file
        if mode=="compact":
            df = df[['Cycle ID', 'Step ID', 'Time(H:M:S:ms)', 'RCap_Chg', 'RCap_DChg']]
            df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_cycle_compact'+'.csv', mode='a', header=False, index=False, sep="\t") # save file
        if mode=="ultracompact": 
            df = df[['CmpCap', 'Vol', 'Step ID']] # save only 'main' columns
            df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_record_ultracompact'+'.csv', mode='a', header=False, index=False, sep="\t") # save file
    else:
        if mode=="full":
            df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_record_full'+'.csv', index=False, sep="\t") # save file
        if mode=="compact":
            df = df[['Cycle ID', 'Step ID', 'Time(H:M:S:ms)', 'RCap_Chg', 'RCap_DChg']]
            df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_cycle_compact'+'.csv', index=False, sep="\t") # save file
        if mode=="ultracompact": 
            df = df[['CmpCap', 'Vol', 'Step ID']] # save only 'main' columns
            df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_record_ultracompact'+'.csv', index=False, sep="\t") # save file

    
def cycle_to_csv(file, filename, mode):
    """Convert Cycle sheet to csv file"""
    if file[-1] == "x":
        df = pd.read_excel(file, sheet_name='Cycle') # read the sheet 'Cycle' in case of xlsx
        header = df.iloc[0]  # get header from first row
        df = df[1:] # remove first row 
        df.columns = header # set headers for columns
    elif file[-1] == "s":
        xl = pd.ExcelFile(file)
        if 'cycle' in xl.sheet_names:
            df = pd.read_excel(file, sheet_name='cycle') # read the sheet 'cycle' in case of xls
            df = df.rename(columns={'Specific Capacity-Chg': 'RCap_Chg', 'Specific Capacity-Dchg': 'RCap_DChg', 'Chg/DChg Efficiency': 'Efficiency'}) # would rather work further with the same format
            if mode=="full":
                df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_cycle_full'+'.csv', index=False, sep="\t") # save file
            if mode=="compact":
                df = df[['Cycle ID', 'Cap_Chg', 'Cap_DChg', 'RCap_Chg', 'RCap_DChg']]
                df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_cycle_compact'+'.csv', index=False, sep="\t") # save file
            if mode=="ultracompact":
                df = df[['Cycle ID', 'RCap_Chg', 'RCap_DChg']]
                df.to_csv(os.path.join(pathlib.Path().absolute(),filename)+'_cycle_ultracompact'+'.csv', index=False, sep="\t") # save file
            

def xlsx_to_csv(file, mode):
    """Convert xlsx of cycler data to text file"""
    filename, file_extension = os.path.splitext(file) 
    if file_extension == '.xlsx' or file_extension == '.xls': # extract data only from xlsx files
        cycle_to_csv(file, filename, mode)
        # record_to_csv(file, filename, mode)
    else:
        print("Skipping non-xlsx file...")

def send_files_to_converter(path=""):
    """Convert each file in path"""
    if path=="":
      path = os.listdir(pathlib.Path().absolute())
    for file in path:
        xlsx_to_csv(file, "full")

current_path_contents = os.listdir(pathlib.Path().absolute()) # get files in current folder
send_files_to_converter(current_path_contents)