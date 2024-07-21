
# use static methods

class scoring_c():
    def __init__(self):
        pass

    @staticmethod
    def return_scores(formatted_file_contents,points_refference): # file_contents is a list
        # returns the regional association scores

        last_option = False
        if list(points_refference.keys())[-1] == ">":
            last_option = True
            last_option_value = list(points_refference.values())[-1]
            points_refference.pop(">") # removes the 'last option'
        
        regional_association_scores = {}

        teams_list = formatted_file_contents[1] # gets the teams list
        last_points_refference = list(points_refference.keys())[-1]

        for team_dict in teams_list:
            team_place = team_dict["place"]
            team_regional_association = team_dict["regional_association"]
            for place_refference in points_refference.keys():
                if place_refference == team_place:
                    
                    if team_regional_association in regional_association_scores:
                        regional_association_scores[team_regional_association] += points_refference[place_refference]
                    else:
                        regional_association_scores[team_regional_association] = points_refference[place_refference]

                elif last_option == True and team_place > last_points_refference:
                    if team_regional_association in regional_association_scores:
                        regional_association_scores[team_regional_association] += last_option_value
                    else:
                        regional_association_scores[team_regional_association] = last_option_value

        return regional_association_scores
        
        
        
        

                    
        



    @staticmethod
    def return_year_sum_score(files_regional_association_score_list ): # {filename:{reg1:100,reg2:200},filename{reg1:100,reg2:200}}
        # returns the total year score e.g. {reg1:500,reg2:600}

        sum_scores_dictionary = {}

        for scores_dictionary in files_regional_association_score_list: # [{scores_dictionary}]
            
            for i in scores_dictionary: # {regionalassoc:1}
                if i in sum_scores_dictionary: #sumscores{reg} == reg
                    sum_scores_dictionary[i] += scores_dictionary[i] 
                else:
                    sum_scores_dictionary[i] = scores_dictionary[i]

        return sum_scores_dictionary
        
    @staticmethod
    def sort_score(regional_association_score_dictionary):
        # Sorting the dictionary by values in descending order
        sorted_desc_scores = dict(sorted(regional_association_score_dictionary.items(), key=lambda item: item[1], reverse=True))
        return sorted_desc_scores