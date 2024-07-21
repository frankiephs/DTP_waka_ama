import tkinter as tk
from tkinter import filedialog
import csv


def export(regional_association_results):

    # Ask user for file location
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV files", "*.csv")])
    
    if file_path:

        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write header
            csv_writer.writerow(["Regional Association", "Score"])
            
            # Write data rows
            for association, score in regional_association_results.items():
                csv_writer.writerow([association, score])
        
        return file_path
    else:
        return False
    
        
    
    