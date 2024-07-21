import os
import customtkinter as ct
from tkinter import messagebox # for pop dialogs
from tkinter import filedialog # for opening folders
import csv_export
import tkinter as tk




class program_functions_component():
    def __init__(self):

        self.parent_folder = ""
        self.target_year = 0
        self.target_keyword = 0
        

    def check_inputs_is_valid(self):
        # print("parent folder",self.parent_folder)
        # print("target year",self.target_year)
        # print("keyword",self.target_keyword)


        if self.check_parent_folder_is_valid() == True:
            if self.check_target_year_is_valid() == False:
                return True
            else:
                return self.check_target_year_is_valid()
        else:
            return self.check_parent_folder_is_valid()
        

        
    def check_parent_folder_is_valid(self):
        try:
            parent_folder_items = os.listdir(self.parent_folder)
        except:
            return f"Pick a valid folder"
        # check i there is inside
        if parent_folder_items:
            for i in parent_folder_items:
                if "WakaNats" in i:
                    return True
                else:
                    continue
            # if no wakanats found
            return f"No WakaNats inside {self.parent_folder}"

        else:
            return f"no items inside {self.parent_folder}"



    def check_target_year_is_valid(self):
        # check if it is an int
        

        
        if self.target_year.isdigit():
            # get all available years
            all_available_years_folders = self.get_all_wakanats()
            
            all_available_years = []
            # get the year string only
            for i in all_available_years_folders:
                all_available_years.append(i[-4:]) # the last 4 strigs


            # check if input is inside the years
            if self.target_year in all_available_years:
                return True
            else:
                return f"The year {self.target_year} is not available"


        else:
            return f"{self.target_year} is not a year"



    # called internally only
    def get_all_wakanats(self):
        
        parent_folder_items = os.listdir(self.parent_folder)
        wakanats_folders = []

        # save the wakanats folders
        for i in parent_folder_items:
            if "WakaNats" in i:
                wakanats_folders.append(i)

        return wakanats_folders
        

    
    



    
    def get_target_year_files(self):
        year_path = self.parent_folder + "/WakaNats" + self.target_year
        year_files = os.listdir(year_path)
        
        if year_files:
            return year_files
        else:
            return f"{self.target_year} have no files inside"



    def find_lif_files(self,year_files):

        lif_files = []

        
        for i in year_files:
            if ".lif" in i:
                lif_files.append(i)
            else:
                continue
        
        # if there are lif files
        if lif_files:
            
            # if keyword specified
            if self.target_keyword:
                lif_files_with_keyword = []

                # find keyword on the lif files
                for i in lif_files:
                    if self.target_keyword in i:
                        lif_files_with_keyword.append(i)
                    else:
                        continue
                
                # if there are lif files with the keyword
                if lif_files_with_keyword:
                    return lif_files_with_keyword
                
                else:
                    return f"there are no lif files with the keyword {self.target_keyword}"
            else:
                # if keyword is not specified then just return the lif files
                return lif_files
        else:
            # if no lif files are found
            return f"No lif files are found in {self.target_year}"
    
        

    def read_n_categorize_file(self,lif_file):

        lif_teams = []


        with open(f'{self.parent_folder}/WakaNats{self.target_year}/{lif_file}', 'r') as file:
            lif_file_lines = file.readlines()

        # separate header
        header = lif_file_lines.pop(0)

        # remove the commas
        header_list_with_empty_items = header.split(",")

        # Filter out empty items using list comprehension
        cleaned_header = [item for item in header_list_with_empty_items if item]

        # check if inbalanced header
        if len(cleaned_header) != 6:
                return f"{lif_file} have an error on race information: {cleaned_header}."



        # separate body

        for line in lif_file_lines:
            
            # pass if there is DNS or DQ or Disqualified
            if "DQ" in line:
                continue
            if "DNS" in line:
                continue
            if "Disqualified" in line:
                continue

            # There are only 10 items on a body
            # remove the commas
            list_with_empty_items = line.split(",")

            # Filter out empty items using list comprehension
            cleaned_line = [item for item in list_with_empty_items if item]

            
            # check if inbalance line
            if len(cleaned_line) != 10:
                return f"{lif_file} have an error on team line: {line}."
            
            # categorize
            team_place = cleaned_line[0]
            team_name = cleaned_line[3]
            team_regional_association = cleaned_line[4]

            # check if valid
            if team_place.isdigit() == False:
                return f"{lif_file} have an error on team line: {line}."
            if team_name.isdigit() != False:
                return f"{lif_file} have an error on team line: {line}."
            if team_regional_association.isdigit() != False:
                return f"{lif_file} have an error on team line: {line}."
            
            


            lif_teams.append([team_place,team_name,team_regional_association])
        
        return lif_teams



    def get_all_scores(self,lif_files_contents_dir):
        
        regional_association_scores = {}

        for lif_file_name in lif_files_contents_dir:
            teams_list = lif_files_contents_dir[lif_file_name]

            for team in teams_list:
                team_place = team[0]
                team_name = team[1]
                team_regional_association = team[2]



                if int(team_place) == 1:
                    team_score = 8
                if int(team_place) == 2:
                    team_score = 7
                if int(team_place) == 3:
                    team_score = 6
                if int(team_place) == 4:
                    team_score = 5
                if int(team_place) == 5:
                    team_score = 4
                if int(team_place) == 6:
                    team_score = 3
                if int(team_place) == 7:
                    team_score = 2
                if int(team_place) > 7: # 8 and onwards
                    team_score = 1
                
                # print("team place", team_place, team_score, lif_file_name, team_name)

                # add to the dictionary
                if team_regional_association in regional_association_scores:
                    regional_association_scores[team_regional_association] += team_score
                else:
                    regional_association_scores[team_regional_association]  = team_score
        
        return regional_association_scores
                

    def sort_descending(self,regional_association_results):
        regional_association_results = dict(sorted(regional_association_results.items(), key=lambda item: item[1], reverse=True))
        return regional_association_results






















class gui_component():
    def __init__(self):   
        self.root = ct.CTk() # opens the customtkinter library
        self.root.geometry("700x600") # widthxheight
        

        # Constants (default)
        self.SCALE_CONSTANT = 1.5 # 1.5 is a suitable # scale constant for scaling the widget and the window
        self.FONT_BASE_CONSTANT = 50  # also increases the fonts size relative to the scale constant
        self.POINTS_REFFERENCE = {
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
        # widget colors
        self.PLACEHOLDER_COLOR = "#696E77"
        self.BORDER_WIDTH =2
        self.CORNER_COLOR = "#2A2C30"
        self.CORNDER_RADIUS = 5
        self.BACKGROUND_COLOR = "#111113"

        self.COLOR_THEME = "blue"
        self.SHOW_ERROR = True
        self.SAVE_TO_CSV = True
        self.APPEARANCE_MODE = "dark"

        # Parse settings











        # fonts
        self.title_font = ct.CTkFont(size=int(self.FONT_BASE_CONSTANT / self.SCALE_CONSTANT * self.SCALE_CONSTANT),weight="bold") # Creates a bold and big font for the title

        # window scaling
        ct.set_window_scaling(self.SCALE_CONSTANT * 0.4)  # Increase the widget size by scale constant
        ct.set_widget_scaling(self.SCALE_CONSTANT * 0.9)  # Increase window size by scale constant

        # theme
        ct.set_appearance_mode(self.APPEARANCE_MODE) # makes the UI light mode. There is dark,system,light.
        ct.set_default_color_theme(self.COLOR_THEME) # changes the theme. There is "blue" (standard), "green", "dark-blue"


        # maximize root
        self.root.rowconfigure(0,weight=1) # maximize the root window to only 1 row
        self.root.columnconfigure(0,weight=1) # maximize the root window to only 1 column
        

        # Homepage Variables
        self.processed_year_files = "" # variable if for all the year files count
        self.processed_year_filtered_files = "" # variable for all the final processed year files count
        self.current_loading_file = "" # current file being processed
        self.parent_path = "" # for the folder path

        # program functions instance
        self.program_functions  = program_functions_component()

        # starts homepage
        self.home_screen() # starts the homepage function


    
    def home_screen(self):
        self.remove_current_screen()

        # Creates homepage frame
        homepage_frame = ct.CTkFrame(self.root,fg_color=self.BACKGROUND_COLOR) # creates the homepage frame
        homepage_frame.grid(row=0,column=0,sticky="NSEW") # displays the homepage frame to the maximizes root window specified earlier

        # configure 2 rows
        # -- nav frame
        homepage_frame.rowconfigure(0,weight=0) 
        # -- body
        homepage_frame.rowconfigure(1,weight=1) 

        # -- maximizes the col 
        homepage_frame.columnconfigure(0,weight=1) 


        # nav bar frame
        nav_bar_frame = ct.CTkFrame(homepage_frame,corner_radius=self.CORNDER_RADIUS,border_color=self.CORNER_COLOR,border_width=self.BORDER_WIDTH,fg_color=self.BACKGROUND_COLOR,height=20)
        nav_bar_frame.grid(row=0, column=0,padx=20,pady=20)

        # for the settings button
        nav_bar_frame.columnconfigure(0,weight=1)
        # for the logs button
        nav_bar_frame.columnconfigure(1,weight=1)
        # for the Help button
        nav_bar_frame.columnconfigure(2,weight=1)

        # max the row
        nav_bar_frame.rowconfigure(0,weight=0)
    
        # Settings button
        settings_button = ct.CTkButton(nav_bar_frame,text="Settings",width=0,command=self.help_screen,fg_color="transparent") # maximize the button width to the text
        settings_button.grid(row=0,column=0,padx=10,pady=2) # displaces the help button on the 'north east'

        # Logs button
        logs_button = ct.CTkButton(nav_bar_frame,text="Logs",width=0,command=self.help_screen,fg_color="transparent") # maximize the button width to the text
        logs_button.grid(row=0,column=1,pady=2) # displaces the help button on the 'north east'

        # Help button
        help_button = ct.CTkButton(nav_bar_frame,text="Help",width=0,command=self.help_screen,fg_color="transparent") # maximize the button width to the text
        help_button.grid(row=0,column=2,padx=10,pady=2) # displaces the help button on the 'north east'





        # Body frame
        body_frame = ct.CTkFrame(homepage_frame, fg_color="transparent")
        body_frame.grid(row=1, column=0,sticky="nsew")

        body_frame.rowconfigure(0,weight=1)
        body_frame.columnconfigure(0,weight=1)

        # inner frame
        
        # inner frame
        inner_frame = ct.CTkFrame(body_frame,fg_color=self.BACKGROUND_COLOR) # Creates the inner frame for the input boxes, etc.
        inner_frame.grid(row=0,column=0) # maximizes it again


        # configure the inner frame: 2 rows 2 cols
        inner_frame.rowconfigure(0,weight=3) # all equal
        inner_frame.rowconfigure(1,weight=1) # all equal
        
        inner_frame.columnconfigure(0,weight=1) # column equal
        inner_frame.columnconfigure(1,weight=1) # column equal
        

        # title 
        title_label = ct.CTkLabel(inner_frame,text="Waka Ama leaderboard system",font=self.title_font) # Creates the title with its text
        title_label.grid(columnspan=2,row=0,column=0,padx=50,pady=50,sticky="nsew") # maximize the display on the its row with using sticky arguement and value "north south east west" 
        
        # open folder
        self.input_parent = ct.CTkEntry(inner_frame,
                                        placeholder_text_color=self.PLACEHOLDER_COLOR,
                                        fg_color="transparent",
                                        border_color=self.CORNER_COLOR,
                                        border_width=self.BORDER_WIDTH,
                                        corner_radius=self.CORNDER_RADIUS,
                                        width=300,
                                        placeholder_text="Type your parent folder locations") # Creates a button to open folder
        
        self.input_parent.grid(row=1,column=0,sticky="e") # displays the open folder
        

        # open folder
        self.parent_folder_button = ct.CTkButton(inner_frame,text="Open folder",command=self.pick_folder,width=50) # Creates a button to open folder
        self.parent_folder_button.grid(row=1,column=1,sticky="w",padx=10) # displays the open folder
        
    def year_details_screen(self):

        self.remove_current_screen()
        year_details_frame = ct.CTkFrame(self.root)
        year_details_frame.grid()

        
        # configure
        year_details_frame.rowconfigure(0,weight=0)
        year_details_frame.rowconfigure(1,weight=1)

        year_details_frame.columnconfigure(0,weight=1)
        
        # nav bar frame
        nav_bar_frame = ct.CTkFrame(year_details_frame,fg_color="transparent")
        nav_bar_frame.grid(row=1, column=0)

        # Back button
        back_button = ct.CTkButton(nav_bar_frame)
        back_button.grid(sticky="w",padx=30,pady=30)

        # body frame
        body_frame = ct.CTkFrame(year_details_frame)
        body_frame.grid(row=1,column=0)

        # configure
        body_frame.rowconfigure(0,weight=0)
        body_frame.rowconfigure(1,weight=0)
        body_frame.rowconfigure(2,weight=0)
        body_frame.rowconfigure(3,weight=0)
        body_frame.rowconfigure(4,weight=0)
        body_frame.rowconfigure(5,weight=0)

        # keyword input
        self.keyword_input = ct.CTkEntry(body_frame,placeholder_text="Type keyword") # Creates an input box for the keyword
        self.keyword_input.grid(row=1,column=0) # displays the keyword input box
        self.processed_keyword = self.keyword_input.get()

        # year input
        self.year_input = ct.CTkEntry(body_frame,placeholder_text="Type year") # Creates the year input box
        self.year_input.grid(row=2,column=0) # displays the year input box
        self.processed_year = self.year_input.get()

        # save to csv
        self.save_to_csv_var = tk.BooleanVar(value=self.SAVE_TO_CSV)
        self.save_to_csv_switch = ct.CTkSwitch(body_frame,text="Save to CSV",variable=self.save_to_csv_var) # Creates save to CSV switch
        self.save_to_csv_switch.grid(row=1,column=1) # displays save to csv switch

        # proceed
        proceed_button = ct.CTkButton(body_frame,text="Proceed",command=self.loading_screen) # Creates the proceed button
        proceed_button.grid(row=2,column=1) #displays the proceed button
        


    def loading_screen(self):
        
        self.remove_current_screen()

        # create the frame
        loading_frame = ct.CTkFrame(self.root) # creates the loading frame
        loading_frame.grid() # Displays the loading frame

        # create the title
        loading_title_label = ct.CTkLabel(loading_frame, text=f"Loading {self.year_input.get()} {self.keyword_input.get()}") # creates the loading title
        loading_title_label.grid() # displays the loading title message

        # create the current file loading
        self.loading_file_label = ct.CTkLabel(loading_frame, text=f"Processing {self.current_loading_file}") # creates the loading text message
        self.loading_file_label.grid() # displays the loading text message

        # add the loading 
        self.loading_progressbar = ct.CTkProgressBar(loading_frame) # Creates a loading bar
        self.loading_progressbar.grid() # displays the loading bar
        self.loading_progressbar.start() # starts the loading bar animation
        
        # loading process
        self.loading_process() # starts the loading process

        

    def help_screen(self):
        self.remove_current_screen()

        help_frame = ct.CTkFrame(self.root)
        help_frame.grid(row=0,column=0,sticky="nsew")

        home_button = ct.CTkButton(help_frame,text="Back",command=self.home_screen)
        home_button.grid()

        help_statement = ct.CTkLabel(help_frame,text="this is a help statement")
        help_statement.grid()


    def error(self,title,message):
        messagebox.showerror(title=title,message=message)

    def success(self,title,message):
        messagebox.showinfo(title=title,message=message)
    
    
    def loading_process(self):
        def process_file(index):
            if index < len(lif_files_from_year):
                lif_file_name = lif_files_from_year[index]
                self.loading_file_label.configure(text=f"Processing {lif_file_name}")
                lif_file_teams = self.program_functions.read_n_categorize_file(lif_file_name)
                if isinstance(lif_file_teams, list):
                    lif_files_contents_dir[lif_file_name] = lif_file_teams
                else:
                    # print(lif_file_teams)
                    self.error("file error", lif_file_teams)
                # Schedule the next file processing after 10 seconds
                self.root.after(10, process_file, index + 1)
            else:
                # All files processed, proceed with further steps
                regional_associations_results = self.program_functions.get_all_scores(lif_files_contents_dir)
                regional_associations_results = self.program_functions.sort_descending(regional_associations_results)
                # print(regional_associations_results)
                self.success("Program Finished", message="All regional associations successfully scored")


                # process finished
                self.loading_progressbar.stop() # stops the animation
                
                if self.save_to_csv_switch.get() == 1:
                    
                    csv_path = csv_export.export(regional_associations_results)

                    if  csv_path != False:
                        # print("Successful")
                        self.success("Saved successfully",message=f"CSV saved to {csv_path}")
                    else:
                        # print("Save to CSV error")
                        self.error("Save to CSV",message="Cannot save to CSV")
                    

                self.home_screen()
        

        self.program_functions.target_year = self.year_input.get()
        self.program_functions.parent_folder = self.parent_path
        self.program_functions.target_keyword = self.keyword_input.get()

        if self.program_functions.check_inputs_is_valid() == True:
            target_year_files = self.program_functions.get_target_year_files()
            if isinstance(target_year_files, list):
                lif_files_from_year = self.program_functions.find_lif_files(target_year_files)
                if isinstance(lif_files_from_year, list):
                    lif_files_contents_dir = {}

                    # Start processing the first file
                    process_file(0)


                else:
                    # print(lif_files_from_year)
                    self.error(title="lif files",message=lif_files_from_year)
                    self.home_screen()
            else:
                # print(target_year_files)
                self.error(title="year files", message=target_year_files)
                self.home_screen()
        else:
            # print(self.program_functions.check_inputs_is_valid())
            self.error(title="Invalid inputs", message=self.program_functions.check_inputs_is_valid())
            self.home_screen()


    



        



    def pick_folder(self):
        folder_path = filedialog.askdirectory()  # Open a folder selection dialog
        if folder_path: # checks if folder exists
                self.parent_path = folder_path
                self.year_details_screen()
        else: # if folder is not found
            self.error(title="folder error",message="pick a folder") # open error dialog. Folder error and the messaeg "Cannot open folder"
    
    
    def remove_current_screen(self): # creates a function for removing the current screen
        
        # removes the current frame
        if self.root.winfo_children(): # checks if there is widgets in the screen
            for widget in self.root.winfo_children(): # loops every widget
                if isinstance(widget, ct.CTkFrame): # finds only the frames
                    widget.grid_remove() # hides the frame

    def run(self):
        self.root.mainloop() # display the whole GUI
    



# starts program
gui = gui_component() # creates the gui component
gui.run() # calls the display function
