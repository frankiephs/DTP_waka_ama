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


