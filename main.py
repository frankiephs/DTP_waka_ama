import os
import customtkinter as ct
from tkinter import messagebox # for pop dialogs
from tkinter import filedialog # for opening folders
import csv_export
import tkinter as tk
from CTkTable import *
import help_contents
import json

class ProgramFunctionsComponent():
    """
    A class that handles program logic and file processing for the Waka Ama Leaderboards system.
    """
    def __init__(self):
        """
        Initialize the program_functions_component with default values.
        """
        self.parent_folder = ''
        self.target_year = 0
        self.target_keyword = 0
    

    # loading process
    @staticmethod
    def loading_process(gui_instance):
        """
        Handle the loading process for the GUI.

        Args:
            gui_instance: The GUI instance to update during loading.
        """
        gui_instance.loading_file_label

        def process_file(index):

            """
            Process a single file from the list of LIF files.

            Args:
                index (int): The index of the file to process.
            """
            if index < len(lif_files_from_year):
                lif_file_name = lif_files_from_year[index]
                gui_instance.loading_file_label.configure(text=f'Processing {lif_file_name}')
                lif_file_teams = gui_instance.program_functions.read_n_categorize_file(lif_file_name,gui_instance)
                if isinstance(lif_file_teams, list):
                    lif_files_contents_dir[lif_file_name] = lif_file_teams
                else:
                    if gui_instance.settings_dict["SHOW_ERRORS_SETTINGS"] is True:
                        gui_instance.error('file error', lif_file_teams)
                # Schedule the next file processing after 10 seconds
                gui_instance.root.after(10, process_file, index + 1)
            else:
                # All files processed, proceed with further steps
                regional_associations_results = gui_instance.program_functions.get_all_scores(lif_files_contents_dir,gui_instance)
                regional_associations_results = gui_instance.program_functions.sort_descending(regional_associations_results)
                gui_instance.success('Program Finished', message='All regional associations successfully scored')


                # process finished
                gui_instance.loading_progressbar.stop() # stops the animation

                # export
                gui_instance.regional_associations_results = regional_associations_results
                    
                gui_instance.results_screen()
        

        gui_instance.program_functions.target_year = gui_instance.year_input.get()
        gui_instance.program_functions.parent_folder = gui_instance.parent_path
        gui_instance.program_functions.target_keyword = gui_instance.keyword_input.get()

        if gui_instance.program_functions.check_inputs_is_valid() is True:
            target_year_files = gui_instance.program_functions.get_target_year_files()
            if isinstance(target_year_files, list):
                lif_files_from_year = gui_instance.program_functions.find_lif_files(target_year_files)
                if isinstance(lif_files_from_year, list):
                    lif_files_contents_dir = {}

                    # Start processing the first file
                    process_file(0)


                else:
                    gui_instance.error(title='lif files',message=lif_files_from_year)
                    gui_instance.year_details_screen()
            else:
                gui_instance.error(title='year files', message=target_year_files)
                gui_instance.year_details_screen()
        else:
            gui_instance.error(title='Invalid inputs', message=gui_instance.program_functions.check_inputs_is_valid())
            gui_instance.year_details_screen()





    # data validation
    def check_inputs_is_valid(self):
        """
        Validate user inputs for parent folder and target year.

        Returns:
            bool or str: True if inputs are valid, otherwise an error message.
        """
        if self.check_parent_folder_is_valid() == True:
            if self.check_target_year_is_valid() == False:
                return True
            else:
                return self.check_target_year_is_valid()
        else:
            return self.check_parent_folder_is_valid()
        
    # parent folder validation
    def check_parent_folder_is_valid(self):
        """
        Check if the selected parent folder is valid and contains WakaNats folders.

        Returns:
            bool or str: True if valid, otherwise an error message.
        """
        try:
            parent_folder_items = os.listdir(self.parent_folder)
        except:
            return f'Pick a valid folder'
        # check i there is inside
        if parent_folder_items:
            for i in parent_folder_items:
                if 'WakaNats' in i:
                    return True
                else:
                    continue
            # if no wakanats found
            return f'No WakaNats inside {self.parent_folder}'

        else:
            return f'no items inside {self.parent_folder}'


    # year input validation
    def check_target_year_is_valid(self):
        """
        Validate the target year input.

        Returns:
            bool or str: True if valid, otherwise an error message.
        """
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
                return f'The year {self.target_year} is not available'


        else:
            return f'{self.target_year} is not a year'



    


    # fetching files
    def get_all_wakanats(self):
        """
        Get all WakaNats folders from the parent folder.

        Returns:
            list: A list of WakaNats folder names.
        """
        parent_folder_items = os.listdir(self.parent_folder)
        wakanats_folders = []

        # save the wakanats folders
        for i in parent_folder_items:
            if 'WakaNats' in i:
                wakanats_folders.append(i)

        return wakanats_folders
        
    def get_target_year_files(self):
        """
        Get all files for the target year.

        Returns:
            list or str: A list of files if found, otherwise an error message.
        """
        year_path = self.parent_folder + '/WakaNats' + self.target_year
        year_files = os.listdir(year_path)
        
        if year_files:
            return year_files
        else:
            return f'{self.target_year} have no files inside'


    # data filtering
    def find_lif_files(self,year_files):
        """
        Find LIF files in the given list of files, optionally filtering by keyword.

        Args:
            year_files (list): List of files for the target year.

        Returns:
            list or str: A list of LIF files if found, otherwise an error message.
        """

        lif_files = []

        
        for i in year_files:
            if '.lif' in i:
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
                    return f'there are no lif files with the keyword {self.target_keyword}'
            else:
                # if keyword is not specified then just return the lif files
                return lif_files
        else:
            # if no lif files are found
            return f'No lif files are found in {self.target_year}'
    
        
    # fetching and organizing
    def read_n_categorize_file(self,lif_file,gui_instance):
        """
        Read and categorize the contents of a LIF file.

        Args:
            lif_file (str): The name of the LIF file to process.
            gui_instance: The GUI instance for settings.

        Returns:
            list or str: A list of categorized teams if successful, otherwise an error message.
        """
        lif_teams = []


        with open(f'{self.parent_folder}/WakaNats{self.target_year}/{lif_file}', 'r') as file:
            lif_file_lines = file.readlines()

        # separate header
        header = lif_file_lines.pop(0)

        # remove the commas
        header_list_with_empty_items = header.split(',')

        # Filter out empty items using list comprehension
        cleaned_header = [item for item in header_list_with_empty_items if item]

        # check if inbalanced header
        if len(cleaned_header) != 6:
                return f'{lif_file} have an error on race information: {cleaned_header}.'



        # separate body

        for line in lif_file_lines:
            
            if gui_instance.settings_dict['DQ_SETTINGS'] is True:
                if 'DQ' in line:
                    continue
                if 'DNS' in line:
                    continue
                if 'Disqualified' in line:
                    continue

            # There are only 10 items on a body
            # remove the commas
            list_with_empty_items = line.split(',')

            # Filter out empty items using list comprehension
            cleaned_line = [item for item in list_with_empty_items if item]

            
            # check if inbalance line
            if len(cleaned_line) != 10:
                return f'{lif_file} have an error on team line: {line}.'
            
            # categorize
            team_place = cleaned_line[0]
            team_name = cleaned_line[3]
            team_regional_association = cleaned_line[4]

            # check if valid
            if team_place.isdigit() == False:
                return f'{lif_file} have an error on team line: {line}.'
            if team_name.isdigit() != False:
                return f'{lif_file} have an error on team line: {line}.'
            if team_regional_association.isdigit() != False:
                return f'{lif_file} have an error on team line: {line}.'
            
            


            lif_teams.append([team_place,team_name,team_regional_association])
        
        return lif_teams


    # Scoring
    def get_all_scores(self,lif_files_contents_dir,gui_instance):
        """
        Calculate scores for all regional associations based on team placements.

        Args:
            lif_files_contents_dir (dict): Dictionary containing processed LIF file contents.
            gui_instance: The GUI instance for settings.

        Returns:
            dict: A dictionary of regional associations and their scores.
        """
        regional_association_scores = {}

        for lif_file_name in lif_files_contents_dir:
            teams_list = lif_files_contents_dir[lif_file_name]

            for team in teams_list:
                team_place = team[0]
                team_name = team[1]
                team_regional_association = team[2]

                points_refference = gui_instance.settings_dict['POINTS_REFFERENCE_SETTINGS']
                last_num = int(list(points_refference.keys())[-2])
                morethan_point = list(points_refference.values())[-1]

                if int(team_place) > last_num:
                    team_score = morethan_point
                else:
                    team_score = points_refference[team_place]
                

                # add to the dictionary
                if team_regional_association in regional_association_scores:
                    regional_association_scores[team_regional_association] += team_score
                else:
                    regional_association_scores[team_regional_association]  = team_score
        
        return regional_association_scores
                
    # sorting
    def sort_descending(self,regional_association_results):
        """
        Sort the regional association results in descending order by score.

        Args:
            regional_association_results (dict): Dictionary of regional associations and scores.

        Returns:
            dict: Sorted dictionary of regional associations and scores.
        """
        regional_association_results = dict(sorted(regional_association_results.items(), key=lambda item: item[1], reverse=True))
        return regional_association_results
    

    
    def settings_fetch(self,gui_instance):
        """
        Fetch program settings from a file or use default settings.

        Args:
            gui_instance: The GUI instance for error handling.

        Returns:
            dict: A dictionary containing program settings.
        """
        default_settings = {
            'DQ_SETTINGS': 0,
            'POINTS_REFFERENCE_SETTINGS': {'1': 8, '2': 7, '3': 6, '4': 5, '5': 4, '6': 3, '7': 2, '8': 1, '>': 1},
            'SHOW_ERRORS_SETTINGS': True
        }

        try:
            with open('program.settings', 'r') as file:
                settings = json.load(file)
        except:
            gui_instance.error('Settings error','Cant fetch settings') 
            settings = default_settings
        return settings
    
    def settings_save(self, gui_instance):
        """
        Save program settings to a file.

        Args:
            gui_instance: The GUI instance for input and error handling.
        """
        DQ_SETTINGS = None
        POINTS_REFFERENCE_SETTINGS = None
        SHOW_ERRORS_SETTINGS = None
        
        # save entry
        try:
            data_str = gui_instance.entry.get()
            POINTS_REFFERENCE_SETTINGS = json.loads(data_str)  # Convert JSON string back to dictionary
            
            if gui_instance.show_errors_button.get() == 1:
                SHOW_ERRORS_SETTINGS = True
            else:
                SHOW_ERRORS_SETTINGS = False

            if gui_instance.dq_switch.get() == 1:
                DQ_SETTINGS = True
            else:
                DQ_SETTINGS = False

            
            # all the settings
            settings_dict = {
                'DQ_SETTINGS': DQ_SETTINGS,
                'POINTS_REFFERENCE_SETTINGS': POINTS_REFFERENCE_SETTINGS,
                'SHOW_ERRORS_SETTINGS': SHOW_ERRORS_SETTINGS
            }

            try:
                with open('program.settings', 'w') as file:
                    json.dump(settings_dict, file, indent=4)
                gui_instance.success('Saved','successfully saved. Program restart required')
            except:
                gui_instance.error('Settings error','Cant save the changes') 
        except:
            gui_instance.error('Invalid data','Invalid data')

        


        


    
    @staticmethod
    def save_to_csv(gui_instance):
        """
        Save the regional associations results to a CSV file.

        Args:
            gui_instance: The GUI instance containing results and for error handling.
        """
        
        csv_path = csv_export.export(gui_instance.regional_associations_results)

        if  csv_path != False:
            gui_instance.success('Saved successfully',message=f'CSV saved to {csv_path}')
        else:
            gui_instance.error('Save to CSV',message='Cannot save to CSV')







    # GUI component

class GuiComponent():
    """
    A class that handles the GUI components of the Waka Ama Leaderboards system.
    """
    def __init__(self):

        # window init
        self.root = ct.CTk() 
        self.root.geometry('2000x1000') 
        self.root.iconbitmap('icon.ico')
        self.root.title('Waka Ama Leaderboards system')

        # program functions instance
        self.program_functions  = ProgramFunctionsComponent()
        self.settings_dict = self.program_functions.settings_fetch(self)

        # Constants (default)

        # widget settings
        self.PLACEHOLDER_COLOR = '#696E77'
        self.BORDER_WIDTH =2
        self.BORDER_COLOR = '#2A2C30'
        self.CORNDER_RADIUS = 5
        self.BACKGROUND_COLOR = '#111113'

        # screen widgets constants
        self.INPUT_GROUP_PADDING = 20
        
        # window settings
        self.SCALE_CONSTANT = 1.5  # 1.5
        self.COLOR_THEME = 'blue'
        self.SHOW_ERROR = self.settings_dict['SHOW_ERRORS_SETTINGS']
        self.SHOW_DQ = self.settings_dict['DQ_SETTINGS']
        self.APPEARANCE_MODE = 'dark'

        # fonts
        self.FONT_BASE_CONSTANT = 50  # also increases the fonts size relative to the scale constant
        self.title_font = ct.CTkFont(size=int((self.FONT_BASE_CONSTANT / self.SCALE_CONSTANT) * self.SCALE_CONSTANT),weight='bold') # Creates a bold and big font for the title
        self.heading_font = ct.CTkFont(size=int(self.FONT_BASE_CONSTANT / self.SCALE_CONSTANT) - self.FONT_BASE_CONSTANT,weight='bold') # Creates a bold and big font for the title

        # scoring 
        self.POINTS_REFFERENCE = self.settings_dict['POINTS_REFFERENCE_SETTINGS']

        # setting class variables

        # window scaling
        ct.set_window_scaling(self.SCALE_CONSTANT * 0.4)  # Increase the widget size by scale constant
        ct.set_widget_scaling(self.SCALE_CONSTANT * 0.9)  # Increase window size by scale constant

        # theme
        ct.set_appearance_mode(self.APPEARANCE_MODE) # makes the UI light mode. There is dark,system,light.
        ct.set_default_color_theme(self.COLOR_THEME) # changes the theme. There is 'blue' (standard), 'green', 'dark-blue'


        # maximize root
        self.root.rowconfigure(0,weight=1) # maximize the root window to only 1 row
        self.root.columnconfigure(0,weight=1) # maximize the root window to only 1 column
        

        # Screen variables initialization

        # Homepage Variables
        self.processed_year_files = ''
        self.processed_year_filtered_files = ''
        self.current_loading_file = ''
        self.parent_path = '' 
        self.regional_associations_results = {}
        
        # reusable widget kwargs
        # Button
        self.SOLID_BUTTON_KWARGS = {'fg_color':'#3e63dd'}
        self.OUTLINE_BUTTON_KWARGS = {'fg_color':'transparent','border_color':'#4468de','border_width':0.3,'text_color':'#96a8f1'}
        
        # Frames
        self.MAIN_SCREEN_FRAME_KWARGS = {'master':self.root,'fg_color':self.BACKGROUND_COLOR}
        self.MATCH_PARENT_KWARGS = {'row':0, 'column':0,'sticky':'nsew'}
        self.SOLID_FRAME_KWARGS = {'fg_color':'#18191B','border_width':self.BORDER_WIDTH,'border_color':self.BORDER_COLOR,'corner_radius':self.CORNDER_RADIUS}
        self.NAV_BAR_FRAME_KWARGS = {'corner_radius':self.CORNDER_RADIUS,'border_color':self.BORDER_COLOR,'border_width':self.BORDER_WIDTH,'fg_color':self.BACKGROUND_COLOR}
        
        # nav bar buttons
        self.NAV_BUTTON_SELECTED = {'width':70,'fg_color':'white','text_color':'black'}
        self.NAV_BUTTON_UNSELECTED = {'width':70,'fg_color':'transparent','text_color':'white'}
        self.NAV_BAR_PADDING = {'pady':2,'padx':1}
        # input 
        self.INPUT_KWARGS = {'placeholder_text_color':self.PLACEHOLDER_COLOR,'fg_color':'transparent','border_color':self.BORDER_COLOR,'border_width':self.BORDER_WIDTH,'corner_radius':self.CORNDER_RADIUS,}
        
        # table
        self.TABLE_KWARGS = {'border_width':self.BORDER_WIDTH,
                             'border_color':self.BORDER_COLOR,
                             'corner_radius':self.CORNDER_RADIUS,
                             'header_color':'#1F2123',
                             'colors':[self.BACKGROUND_COLOR,self.BACKGROUND_COLOR]}




        
        

        # starts homepage
        self.home_screen() # starts the homepage function


        

        


    # screens
    def home_screen(self):
        """
        Initialize the GUI component with default settings and window setup.
        """
        self.remove_current_screen()

        # Creates homepage frame
        homepage_frame = ct.CTkFrame(**self.MAIN_SCREEN_FRAME_KWARGS) 
        homepage_frame.grid(row=0,column=0,sticky='NSEW') 
        homepage_frame.rowconfigure(0,weight=0) 
        homepage_frame.rowconfigure(1,weight=1) 
        homepage_frame.columnconfigure(0,weight=1) 

        # nav bar frame
        nav_bar_frame = ct.CTkFrame(homepage_frame,height=20,**self.NAV_BAR_FRAME_KWARGS)
        nav_bar_frame.grid(row=0, column=0,padx=20,pady=20)
        nav_bar_frame.columnconfigure(0,weight=0)
        nav_bar_frame.columnconfigure(1,weight=0)
        nav_bar_frame.columnconfigure(2,weight=0)
        nav_bar_frame.rowconfigure(0,weight=0)
    
        
        # Home button
        home_button = ct.CTkButton(nav_bar_frame,text='Home',**self.NAV_BUTTON_SELECTED) # maximize the button width to the text
        home_button.grid(row=0,column=0,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'

        # Settings button
        settings_button = ct.CTkButton(nav_bar_frame,text='Settings',command=self.settings_screen,**self.NAV_BUTTON_UNSELECTED) # maximize the button width to the text
        settings_button.grid(row=0,column=1,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'

        # Help button
        help_button = ct.CTkButton(nav_bar_frame,text='Help',command=self.help_screen,**self.NAV_BUTTON_UNSELECTED) # maximize the button width to the text
        help_button.grid(row=0,column=2,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'




        # Body frame
        body_frame = ct.CTkFrame(homepage_frame, fg_color='transparent')
        body_frame.grid(row=1, column=0,sticky='nsew')
        body_frame.rowconfigure(0,weight=1)
        body_frame.columnconfigure(0,weight=1)

        # inner frame
        inner_frame = ct.CTkFrame(body_frame,fg_color=self.BACKGROUND_COLOR) # Creates the inner frame for the input boxes, etc.
        inner_frame.grid(row=0,column=0,sticky='n') 
        inner_frame.rowconfigure(0,weight=2) 
        inner_frame.rowconfigure(1,weight=1) 
        inner_frame.columnconfigure(0,weight=1) 
        
        # title_group
        title_group = ct.CTkFrame(inner_frame,fg_color='transparent')
        title_group.grid(row=0,column=0,padx=50,pady=50,sticky='nsew')
        title_group.rowconfigure(0,weight=1)
        title_group.rowconfigure(0,weight=1)
        title_group.columnconfigure(0,weight=1)

        # title 
        title_label = ct.CTkLabel(title_group,text='Waka Ama leaderboard system',font=self.title_font) 
        title_label.grid() 
        
        # subtitle group
        subtitle_label = ct.CTkLabel(title_group,text='A program that scores your Waka Ama National results and saves to CSV',font=self.heading_font) 
        subtitle_label.grid() 

        # input group
        input_group = ct.CTkFrame(inner_frame,**self.SOLID_FRAME_KWARGS)
        input_group.grid(row=1,column=0,pady=40)
        input_group.rowconfigure(0,weight=1)
        input_group.columnconfigure(0,weight=1)
        input_group.columnconfigure(1,weight=1)
        input_group.columnconfigure(2,weight=1)


        # input parent path
        self.input_parent = ct.CTkEntry(input_group,**self.INPUT_KWARGS,width=300,placeholder_text="Type your parent folder's location") 
        self.input_parent.grid(row=0,column=0,sticky='e',pady=self.INPUT_GROUP_PADDING,padx=(self.INPUT_GROUP_PADDING,0)) # displays the open folder
        
        # open folder button
        self.parent_folder_button = ct.CTkButton(input_group,text='Open folder',command=self.pick_folder,width=50,**self.OUTLINE_BUTTON_KWARGS) # Creates a button to open folder
        self.parent_folder_button.grid(row=0,column=1,sticky='w',padx=10,pady=self.INPUT_GROUP_PADDING) # displays the open folder
        
        # Next button
        self.parent_folder_button = ct.CTkButton(input_group,text='Next',command=self.parent_path_submit,width=50,**self.SOLID_BUTTON_KWARGS) # Creates a button to open folder
        self.parent_folder_button.grid(row=0,column=2,sticky='w',padx=(10,self.INPUT_GROUP_PADDING),pady=self.INPUT_GROUP_PADDING) # displays the open folder
        










    def year_details_screen(self):
        """
        Display the screen for entering year details and selecting files.
        """
        self.remove_current_screen()

        year_details_frame = ct.CTkFrame(self.root,fg_color=self.BACKGROUND_COLOR)
        year_details_frame.grid(sticky='nsew')
        
        # configure
        year_details_frame.rowconfigure(0,weight=0)
        year_details_frame.rowconfigure(1,weight=1)
        year_details_frame.columnconfigure(0,weight=1)
        
        # nav bar frame
        nav_bar_frame = ct.CTkFrame(year_details_frame,fg_color='transparent')
        nav_bar_frame.grid(row=0, column=0,sticky='nsew')

        # Back button
        back_button = ct.CTkButton(nav_bar_frame,text='Back',width=0,**self.OUTLINE_BUTTON_KWARGS,command=self.home_screen)
        back_button.grid(sticky='w',padx=10,pady=10)

        # body frame
        body_frame = ct.CTkFrame(year_details_frame,fg_color='#18191B',border_width=self.BORDER_WIDTH,border_color=self.BORDER_COLOR,corner_radius=self.CORNDER_RADIUS)
        body_frame.grid(row=1,column=0)

        # configure
        body_frame.rowconfigure(0,weight=0)
        body_frame.rowconfigure(1,weight=0)
        body_frame.rowconfigure(2,weight=0)
        body_frame.rowconfigure(3,weight=0)
        body_frame.rowconfigure(4,weight=0)
        body_frame.rowconfigure(5,weight=0)

        # heading
        heading_label = ct.CTkLabel(body_frame,text='Input Details',font=self.heading_font)
        heading_label.grid(row=0,column=0,padx=30,pady=(30,10),sticky='w')

        # year label
        year_label = ct.CTkLabel(body_frame,text='Year')
        year_label.grid(row=1,column=0,sticky='w',padx=30)

        # year input
        self.year_input = ct.CTkEntry(body_frame,placeholder_text='Type year',placeholder_text_color=self.PLACEHOLDER_COLOR,border_width=self.BORDER_WIDTH,corner_radius=self.CORNDER_RADIUS,border_color=self.BORDER_COLOR,fg_color=self.BACKGROUND_COLOR) # Creates the year input box
        self.year_input.grid(row=2,column=0,padx=30,pady=(0,10),sticky='nsew') # displays the year input box
        self.processed_year = self.year_input.get()

        # keyword label
        keyword_label = ct.CTkLabel(body_frame,text='keyword')
        keyword_label.grid(row=3,column=0,padx=30,sticky='w')

        # keyword input
        self.keyword_input = ct.CTkEntry(body_frame,placeholder_text='Type keyword',placeholder_text_color=self.PLACEHOLDER_COLOR,border_width=self.BORDER_WIDTH,corner_radius=self.CORNDER_RADIUS,border_color=self.BORDER_COLOR,fg_color=self.BACKGROUND_COLOR) # Creates an input box for the keyword
        self.keyword_input.grid(row=4,column=0,padx=30,sticky='nsew') # displays the keyword input box
        self.processed_keyword = self.keyword_input.get()

        # table
        value = [['Year','File/s']]
        
        # [2020,300],[2021,300]

        table = CTkTable(body_frame, row=1, column=2, values=value,width=50,**self.TABLE_KWARGS)
        table.grid(row=1,column=1,rowspan=4,padx=30)
        
        available_years = self.program_functions.get_all_wakanats()
        
        for item in available_years:
            files_count = len(os.listdir(self.parent_path + f'/{item}'))
            table.add_row([item[-4:],files_count])


        # proceed
        proceed_button = ct.CTkButton(body_frame,text='Proceed',command=self.loading_screen,width=30,**self.SOLID_BUTTON_KWARGS) # Creates the proceed button
        proceed_button.grid(row=5,column=1,padx=30,pady=20,sticky='e') #displays the proceed button
        
    
    def loading_screen(self):
        """
        Displays the loading screen and the current progress
        """
        self.remove_current_screen()

        # create the frame
        loading_frame = ct.CTkFrame(**self.MAIN_SCREEN_FRAME_KWARGS) # creates the loading frame
        loading_frame.grid(**self.MATCH_PARENT_KWARGS) # Displays the loading frame
        loading_frame.rowconfigure(0,weight=1)
        loading_frame.columnconfigure(0,weight=1)


        # inner frame
        inner_frame = ct.CTkFrame(loading_frame,fg_color='transparent')
        inner_frame.grid()

        # create the title
        loading_title_label = ct.CTkLabel(inner_frame, text=f'Loading {self.year_input.get()} {self.keyword_input.get()}',font=self.heading_font) # creates the loading title
        loading_title_label.grid() # displays the loading title message

        # create the current file loading
        self.loading_file_label = ct.CTkLabel(inner_frame, text=f'Processing {self.current_loading_file}') # creates the loading text message
        self.loading_file_label.grid() # displays the loading text message

        # add the loading 
        self.loading_progressbar = ct.CTkProgressBar(inner_frame) # Creates a loading bar
        self.loading_progressbar.grid() # displays the loading bar
        self.loading_progressbar.start() # starts the loading bar animation
        
        # loading process
        self.program_functions.loading_process(self)

    def results_screen(self):
        """
        Display the results screen showing regional association scores.
        """
        self.remove_current_screen()

        results_screen_frame = ct.CTkFrame(self.root,fg_color=self.BACKGROUND_COLOR)
        results_screen_frame.grid(sticky='nsew')

        
        # configure
        results_screen_frame.rowconfigure(0,weight=0)
        results_screen_frame.rowconfigure(1,weight=1)

        results_screen_frame.columnconfigure(0,weight=1)
        
        # nav bar frame
        nav_bar_frame = ct.CTkFrame(results_screen_frame,fg_color='transparent')
        nav_bar_frame.grid(row=0, column=0,sticky='nsew')

        # Back button
        back_button = ct.CTkButton(nav_bar_frame,text='Back',width=0,command=self.home_screen,**self.OUTLINE_BUTTON_KWARGS)
        back_button.grid(sticky='w',padx=10,pady=10)

        # body frame
        body_frame = ct.CTkFrame(results_screen_frame,fg_color=self.BACKGROUND_COLOR)
        body_frame.grid(row=1,column=0,sticky='nsew')

        # maximize
        body_frame.rowconfigure(0,weight=1)
        body_frame.columnconfigure(0,weight=1)

        # create inner frame
        inner_frame = ct.CTkFrame(body_frame,fg_color=self.BACKGROUND_COLOR)
        inner_frame.grid(row=0,column=0)

        inner_frame.rowconfigure(0,weight=1)
        inner_frame.rowconfigure(1,weight=1)
        inner_frame.rowconfigure(2,weight=0)
        inner_frame.rowconfigure(3,weight=1)

        inner_frame.columnconfigure(0,weight=1)
        
        # heading
        heading_label = ct.CTkLabel(inner_frame,text='Regional Association Results',font=self.title_font)
        heading_label.grid(row=0,column=0,padx=30,pady=(30,0))

        # heading
        subheading_label = ct.CTkLabel(inner_frame,text=f'This is the regional association results of {self.year_input.get()} {self.keyword_input.get()}')
        subheading_label.grid(row=1,column=0,pady=(0,30))
        
        # table
        value = [['Place','Regional Association','Points']]

        for index, (regional_association, score) in enumerate(self.regional_associations_results.items()):
            value.append([index+1, regional_association, score])



        table_frame = ct.CTkScrollableFrame(inner_frame,height=100,width=300,fg_color=self.BACKGROUND_COLOR)
        table_frame.grid(row=2,column=0,padx=30)
        

        table = CTkTable(table_frame,width=190, row=len(value), column=3, values=value,**self.TABLE_KWARGS)
        table.grid(sticky='nsew')
        table.edit_column(0,width=10)
        table.edit_column(2,width=10)

        # save to CSV
        save_to_csv = ct.CTkButton(inner_frame,text='Save to CSV',command=lambda: self.program_functions.save_to_csv(self),width=30,**self.SOLID_BUTTON_KWARGS) # Creates the proceed button
        save_to_csv.grid(row=3,column=0,padx=30,pady=20,sticky='e') #displays the proceed button


    def settings_screen(self):
        """
        Display the settings screen for configuring program options.
        """

        self.remove_current_screen()

        # Creates help frame
        settings_screen_frame = ct.CTkFrame(**self.MAIN_SCREEN_FRAME_KWARGS) 
        settings_screen_frame.grid(row=0,column=0,sticky='NSEW') 
        settings_screen_frame.rowconfigure(0,weight=0) 
        settings_screen_frame.rowconfigure(1,weight=0) 
        settings_screen_frame.columnconfigure(0,weight=1) 

        # nav bar frame
        nav_bar_frame = ct.CTkFrame(settings_screen_frame,height=20,**self.NAV_BAR_FRAME_KWARGS)
        nav_bar_frame.grid(row=0, column=0,padx=20,pady=20)
        nav_bar_frame.columnconfigure(0,weight=0)
        nav_bar_frame.columnconfigure(1,weight=0)
        nav_bar_frame.columnconfigure(2,weight=0)
        nav_bar_frame.rowconfigure(0,weight=0)
    
        # Home button
        home_button = ct.CTkButton(nav_bar_frame,text='Home',command=self.home_screen,**self.NAV_BUTTON_UNSELECTED) # maximize the button width to the text
        home_button.grid(row=0,column=0,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'

        # Settings button
        settings_button = ct.CTkButton(nav_bar_frame,text='Settings',**self.NAV_BUTTON_SELECTED) # maximize the button width to the text
        settings_button.grid(row=0,column=1,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'

        # Help button
        help_button = ct.CTkButton(nav_bar_frame,text='Help',command=self.help_screen,**self.NAV_BUTTON_UNSELECTED) # maximize the button width to the text
        help_button.grid(row=0,column=2,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'



        # body frame
        body_frame = ct.CTkScrollableFrame(settings_screen_frame,**self.SOLID_FRAME_KWARGS,width=400,height=400)
        body_frame.grid(row=1,column=0,padx=100,pady=(30,50))
        body_frame.rowconfigure(0,weight=1)
        body_frame.columnconfigure(0,weight=1)

        save_frame = ct.CTkFrame(body_frame,fg_color=self.BACKGROUND_COLOR,height=50,width=50)
        save_frame.grid(sticky='nsew')
        save_button = ct.CTkButton(save_frame,**self.SOLID_BUTTON_KWARGS,text='save',width=20,command= lambda: self.program_functions.settings_save(self))
        save_button.grid(sticky='w',padx=10,pady=10)

        dq_frame = ct.CTkFrame(body_frame,fg_color=self.BACKGROUND_COLOR,height=50,width=50)
        dq_frame.grid(sticky='nsew',padx=40,pady=(20,0))

        dq_frame.rowconfigure(0,weight=1)
        dq_frame.columnconfigure(0,weight=1)
        
        self.dq_switch = ct.CTkSwitch(dq_frame,text='Do not include Disqualified/Did not start')
        self.dq_switch.grid(row=0,column=0,sticky='w')


        show_errors_frame = ct.CTkFrame(body_frame,fg_color=self.BACKGROUND_COLOR,height=50,width=50)
        show_errors_frame.grid(sticky='nsew',padx=40,pady=(20,0))

        show_errors_frame.rowconfigure(0,weight=1)
        show_errors_frame.columnconfigure(0,weight=1)
        
        self.show_errors_button = ct.CTkSwitch(show_errors_frame,text='Show errors')
        self.show_errors_button.grid(row=0,column=0,sticky='w')

        def populate_entry(data):
            data_str = json.dumps(data)  # Convert dictionary to JSON string
            self.entry.insert(0, data_str)

        scoring_criteria_frame = ct.CTkFrame(body_frame,fg_color=self.BACKGROUND_COLOR,height=50,width=50)
        scoring_criteria_frame.grid(sticky='nsew',padx=40,pady=(20,0))

        scoring_criteria_frame.rowconfigure(0,weight=1)
        scoring_criteria_frame.columnconfigure(0,weight=1)

        scoring_criteria_label = ct.CTkLabel(scoring_criteria_frame,text='Scoring Criteria')
        scoring_criteria_label.grid(sticky='w')

        self.entry = ct.CTkEntry(scoring_criteria_frame)
        self.entry.grid(sticky='nsew')

        populate_entry(self.settings_dict['POINTS_REFFERENCE_SETTINGS'])


        if self.settings_dict['DQ_SETTINGS']:
            self.dq_switch.select()
        else:
            self.dq_switch.deselect()
        if self.settings_dict['SHOW_ERRORS_SETTINGS']:
            self.show_errors_button.select()
        else:
            self.show_errors_button.deselect()



    def help_screen(self):
        """
        Display the help screen with program usage instructions.
        """
        self.remove_current_screen()

        # Creates help frame
        help_screen_frame = ct.CTkFrame(**self.MAIN_SCREEN_FRAME_KWARGS) 
        help_screen_frame.grid(row=0,column=0,sticky='NSEW') 
        help_screen_frame.rowconfigure(0,weight=0) 
        help_screen_frame.rowconfigure(1,weight=1) 
        help_screen_frame.columnconfigure(0,weight=1) 

        # nav bar frame
        nav_bar_frame = ct.CTkFrame(help_screen_frame,height=20,**self.NAV_BAR_FRAME_KWARGS)
        nav_bar_frame.grid(row=0, column=0,padx=20,pady=20)
        nav_bar_frame.columnconfigure(0,weight=0)
        nav_bar_frame.columnconfigure(1,weight=0)
        nav_bar_frame.columnconfigure(2,weight=0)
        nav_bar_frame.rowconfigure(0,weight=0)
    
        # Home button
        home_button = ct.CTkButton(nav_bar_frame,text='Home',command=self.home_screen,**self.NAV_BUTTON_UNSELECTED) # maximize the button width to the text
        home_button.grid(row=0,column=0,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'

        # Settings button
        settings_button = ct.CTkButton(nav_bar_frame,text='Settings',command=self.settings_screen,**self.NAV_BUTTON_UNSELECTED) # maximize the button width to the text
        settings_button.grid(row=0,column=1,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'

        # Help button
        help_button = ct.CTkButton(nav_bar_frame,text='Help',**self.NAV_BUTTON_SELECTED) # maximize the button width to the text
        help_button.grid(row=0,column=2,**self.NAV_BAR_PADDING) # displaces the help button on the 'north east'


        # body frame
        body_frame = ct.CTkScrollableFrame(help_screen_frame,**self.SOLID_FRAME_KWARGS)
        body_frame.grid(row=1,column=0,sticky='nsew',padx=200,pady=50)
        body_frame.rowconfigure(0,weight=1)
        body_frame.columnconfigure(0,weight=1)

        # inner frame
        inner_frame = ct.CTkFrame(body_frame,fg_color='transparent')
        inner_frame.grid(row=0,column=0,sticky='nsew',padx=100,pady=50)


        help_contents.fetch(inner_frame,self)


        

    
    # alerts
    def error(self,title,message):
        """
        Display an error message dialog.

        Args:
            title (str): The title of the error message.
            message (str): The content of the error message.
        """
        messagebox.showerror(title=title,message=message)

    def success(self,title,message):
        """
        Display a success message dialog.

        Args:
            title (str): The title of the success message.
            message (str): The content of the success message.
        """
        messagebox.showinfo(title=title,message=message)



    # screen utility functions
    def parent_path_submit(self):
        """
        Submits the input parent path after selecting a folder
        """
        self.parent_path = self.input_parent.get()
        self.program_functions.parent_folder = self.input_parent.get()
        check_parent_folder = self.program_functions.check_parent_folder_is_valid()
        if check_parent_folder is True:
            self.year_details_screen()
        else:
            self.error('Incorrect Folder',check_parent_folder)

    def pick_folder(self):
        """
        Open a file dialog for selecting a folder and update the parent path.
        """
        folder_path = filedialog.askdirectory()  # Open a folder selection dialog
        if folder_path: # checks if folder exists
                self.input_parent.delete(0,tk.END)
                self.input_parent.insert(0,folder_path)
        else: # if folder is not found
            self.error(title='folder error',message='pick a folder') # open error dialog. Folder error and the messaeg 'Cannot open folder'
    

    def remove_current_screen(self): # creates a function for removing the current screen
    
        # removes the current frame
        if self.root.winfo_children(): # checks if there is widgets in the screen
            for widget in self.root.winfo_children(): # loops every widget
                if isinstance(widget, ct.CTkFrame): # finds only the frames
                    widget.grid_remove() # hides the frame

    # window loop
    def run(self):
        """
        Runs the customtkinter app
        """
        self.root.mainloop() # display the whole GUI

def main():
    gui = GuiComponent() # creates the gui component
    gui.run() # calls the display function

main()
