import customtkinter as CT # External Library
import tkinter as tk # for GUI
from tkinter import filedialog # for getting files
from tkinter import messagebox # for warnings and info


# Internal modules
import file_read as fr # for file reading
import scoring # for scoring
import csv_export # for exporting
import datetime # for log dates
import help_screen # for help screen


class gui_c:
    def __init__(self, master):
        
        CT.set_appearance_mode("dark")
        self.root = master
        self.root.geometry("600x400")
        self.root.wm_state('zoomed')
        CT.set_default_color_theme("green")
        # expand the root
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.points_refference = {
        "1":8,
        "2":7,
        "3":6,
        "4":5,
        "5":4,
        "6":3,
        "7":2,
        "8":1,
        ">":1,
        }

        self.font_family = "Helvetica"

        self.title_font = (self.font_family,50,"bold") # 50
        self.heading_font = (self.font_family,30) #30
        self.default_font = (self.font_family,20) #20

        self.loading_delay = 1
        self.logs_path = "logs"
        
        self.selected_year = None
        self.ShowError = True
        self.error_list = []
        self.current_frame = None
        self.filter_case_sensitive = False
        
        # settings
        self.filter_keyword = None

        # Show the home frame initially
        self.HomeScreen()
        self.save_to_logfile("Opened Program")
    



