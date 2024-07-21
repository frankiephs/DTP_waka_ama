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


    def HomeScreen(self):
        # initialize the screen
        self.current_frame = CT.CTkFrame(self.root)
        self.save_to_logfile("HomeScreen") # save to log file

        # initialize the grid 3 rows
        self.current_frame.rowconfigure(1,weight=1) # center is much bigger
        self.current_frame.columnconfigure(0, weight=1)  # make sure column stretches
        

        # creating nav bar frame
        nav_bar = CT.CTkFrame(self.current_frame) 
        nav_bar.grid(column=0, row=0, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.

        # initialize nav bar to two columns
        nav_bar.columnconfigure(0,weight=1)
        nav_bar.columnconfigure(1, weight=1)
        

        # nav bar help button
        help_button = CT.CTkButton(nav_bar,text="Help", command=lambda:self.show_screen(self.HelpScreen),font=self.default_font)
        help_button.grid(column=1, sticky="NE",padx=10,pady=10)

        
        # creating the body frame
        body_frame = CT.CTkFrame(self.current_frame)
        body_frame.grid(column=0, row=1, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.
        
        # initialize the body frame to have only maxed 1 cell
        body_frame.rowconfigure(0, weight=1)
        body_frame.columnconfigure(0, weight=1)

        # Create a group for the components
        body_inner_frame = CT.CTkFrame(body_frame, fg_color="transparent")
        body_inner_frame.grid(column=0, row=0, sticky="")

        # Title
        
        title_label = CT.CTkLabel(body_inner_frame,text="WAKA AMA",font=self.title_font)
        title_label.grid()

        # subtitle
        subtitle_label = CT.CTkLabel(body_inner_frame,text="Regional Association Scoring Program",font=self.heading_font)
        subtitle_label.grid()

        # Paragraph
        paragraph_label = CT.CTkLabel(body_inner_frame,text="Make sure it is a valid parent folder. Parent Folder should not contain non-folder items inside.",font=self.default_font)
        paragraph_label.grid()

        # Open Folder Button
        OpenFolder = CT.CTkButton(body_inner_frame, text="Open Folder", command=self.get_folder_path,font=self.heading_font)
        OpenFolder.grid(padx=20,pady=20)

        # Finalize the Screen
        self.current_frame.grid(row=0, column=0, sticky="NSEW")
    
    def get_folder_path(self):
        self.save_to_logfile("Get Golder Path")
        folder_path = filedialog.askdirectory()

        if folder_path:
            self.parent_path = folder_path
            self.show_screen(self.SelectYearsScreen,data=folder_path)  # Pass function reference without calling it
        else:
            messagebox.showwarning("Error while Processing", "Invalid File Folder\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
        
    def SelectYearsScreen(self, parent_path):

        # initialize the screen
        self.save_to_logfile("Select Years screen")
        self.current_frame = CT.CTkFrame(self.root)

        # initialize the grid 3 rows
        self.current_frame.rowconfigure(1,weight=1) # center is much bigger
        self.current_frame.columnconfigure(0, weight=1)  # make sure column stretches

        # creating nav bar frame
        nav_bar = CT.CTkFrame(self.current_frame) 
        nav_bar.grid(column=0, row=0, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.

        # initialize nav bar to two columns
        nav_bar.columnconfigure(0,weight=1)
        nav_bar.columnconfigure(1, weight=1)

        # adding nav bar back button
        Back_Button = CT.CTkButton (nav_bar, text = "Back",font=self.default_font,command=lambda: self.show_screen(self.HomeScreen))
        Back_Button.grid(column=0,row=0,sticky="NW",padx=10,pady=10)

        # creating the body frame
        body_frame = CT.CTkFrame(self.current_frame)
        body_frame.grid(column=0, row=1, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.

        # initialize the body frame to have only maxed 1 cell
        body_frame.rowconfigure(0, weight=1)
        body_frame.columnconfigure(0, weight=1)

        
        # Create a group for the components
        body_inner_frame = CT.CTkFrame(body_frame, fg_color="transparent")
        body_inner_frame.grid(column=0, row=0, sticky="")


        # Title
        title = CT.CTkLabel(body_inner_frame,text="Select year", font=self.title_font)
        title.grid()

        # Available years label
        available_years_label = CT.CTkLabel(body_inner_frame,text="Available Year/s", font=self.heading_font)
        available_years_label.grid()

        # Table Label
        headers_label = CT.CTkLabel(body_inner_frame,text="Year | Files",font=self.default_font)
        headers_label.grid()

        # fetch the children folders
        try:
            years_and_files = fr.file_read_c.return_years(parent_path)
        except:
            error = f"[Invalid folder] Select Another folder | {parent_path}"
            messagebox.showwarning("Error while Processing", f"{error}\n\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
            self.show_screen(self.HomeScreen)
            return
            

        
        # years & Files Table
        
        for i in years_and_files:
            year_label = CT.CTkLabel(body_inner_frame,text=f"{i} : {years_and_files[i]} file/s",font=self.default_font)
            year_label.grid()
        

        # creating bottom bar frame
        bottom_bar_frame = CT.CTkFrame(self.current_frame,border_width=3,corner_radius=0) 
        bottom_bar_frame.grid(column=0, row=2, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.

        # initialize nav bar to three columns
        bottom_bar_frame.columnconfigure(0,weight=1)
        bottom_bar_frame.columnconfigure(1, weight=1)
        bottom_bar_frame.columnconfigure(2, weight=1)

        # input configuration
        placeholder_color = "white"
        year_input_placeholder = "Enter year"
        filter_input_placeholder = "Enter filter keyword"


        
        bottom_contents_pady = 20

        # Years Input
        year_input = CT.CTkEntry(bottom_bar_frame,font=self.default_font, fg_color="grey",width=200,placeholder_text=year_input_placeholder, placeholder_text_color=placeholder_color)
        year_input.grid(column=0,row=0,pady=bottom_contents_pady,sticky="E")

        # Filter input
        filter_input = CT.CTkEntry(bottom_bar_frame,fg_color='grey',font=self.default_font,width=300,placeholder_text=filter_input_placeholder, placeholder_text_color=placeholder_color)
        filter_input.grid(column=1,row=0,pady=bottom_contents_pady)

        # Continue Button
        select_year_button = CT.CTkButton(bottom_bar_frame,text="Continue",font=self.heading_font,command= lambda : self.select_year(year_input,years_and_files, filter_input))
        select_year_button.grid(column=2,row=0,pady=bottom_contents_pady)


        # Finalize
        self.current_frame.grid(row=0, column=0, sticky="NSEW")


