import os
"""
I made the parent_path as a param instead of an attribute of the class is to
- Flexibility: You can work with different parent_path values without needing to create a new instance of the class each time.
- Modularity: Each method can operate independently, making it easier to test and debug.
- Simplicity: Reduces the complexity of the class, making it easier to maintain and understand.

I am using static methods decorator
@staticmethod
"""


class file_read_c():
    def __init__(self):
        pass

    @staticmethod
    def return_years(parent_path):
        # returns years in a list e.g.[year1,year2]
        
        years_and_files = {}
        year_list = os.listdir(parent_path)
        for year_path in year_list:
            year = year_path[len(year_path) - 4: len(year_path)]
            years_and_files[year] = len(os.listdir(parent_path + "/" + year_path)) # put inside the year dict
        
        return years_and_files
        

    @staticmethod
    def find_year_path(parent_path, year, prefix):
        # returns the path of the arguement year
        year_list = os.listdir(parent_path)
        year_path = None

        for i in year_list:
            if i == f"{prefix}{year}":
                year_path = f"{parent_path}/{prefix}{year}"
        return year_path

            
        
        
        
    
    @staticmethod
    def return_files(year_path):
        # returns list of files in a dir e.g.  [file1,file2,file3]

        files_list = os.listdir(year_path)
        
        return files_list

    @staticmethod
    def return_content(filepath):
        # returns dictionary of the contents of a file. Includes its file name and content on a raw form
        """
        ["1,team,reg","2,team,reg"]
        """
        
        with open(filepath) as file:
            file_contents = file.readlines()
        return file_contents
    



    @staticmethod
    def format_content(file_contents,filename):
        # returns a dictionary of the formatted/categorized version of the contents of the file contents
        
        race_info = file_contents[0]
        subsequent_rows = file_contents[1:-1]

        # race info
        formatted_race_info = race_info.split(',')

        clean_formatted_race_info = []

        for i in formatted_race_info:
            if i != "":
                clean_formatted_race_info.append(i)
            else:
                continue
        formatted_race_info = clean_formatted_race_info
        
        # check if they ave the appropriate fields
        if len(formatted_race_info) < 6:
            return "ERROR"

        race_number = formatted_race_info[0]
        race_type = formatted_race_info[1]
        race_heat = formatted_race_info[2]
        race_title = formatted_race_info[3]
        race_length = formatted_race_info[4]
        race_start_time = formatted_race_info[5]
        subsequent_rows_count = len(subsequent_rows)

        race_info_attributes = {"number":race_number,
                                "type":race_type,
                                "heat":race_heat,
                                "title":race_title,
                                "length":race_length,
                                "start_time":race_start_time,
                                "subsequent_rows_count":subsequent_rows_count}
        
        # teams
        team_list = []
        for string_team in subsequent_rows:
            formatted_team = string_team.split(',')
            
            clean_formatted_team = []

            for i in formatted_team:
                if i != "":
                    clean_formatted_team.append(i)
                else:
                    continue
            formatted_team = clean_formatted_team
            
            if len(formatted_team) < 10:
                return "ERROR"

            # after removing the unneccessary commas
            team_place = formatted_team[0]
            team_id = formatted_team[1]
            team_lane = formatted_team[2]
            team_name = formatted_team[3]
            team_regional_association = formatted_team[4]
            team_elapsed_time = formatted_team[5]
            team_difference = formatted_team[6]
            team_start = formatted_team[7]
            team_difference = formatted_team[8]
            team_difference = formatted_team[9]
            
            if team_regional_association[0].isdigit():
                return "ERROR"


            team_attributes = {"place":team_place,
                                "id":team_id,
                                "lane":team_lane,
                                "name":team_name,
                                "regional_association":team_regional_association,
                                "elapsed_time":team_elapsed_time,
                                "difference":team_difference,
                                "start":team_start}
            team_list.append(team_attributes)
        
                
        file_attributes = [race_info_attributes,team_list]
        

        
                
        return file_attributes