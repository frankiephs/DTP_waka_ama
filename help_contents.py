import customtkinter as ct



title_text = "Help Page"


#------------------------------------------------------------------------


h1 = "About"

p1 = """

The Waka Ama Sprint Nationals Scoring System is a program that determines the overall 
winning regional association by:
- Reading the raw data from all the race results (You can also specify a keyword for 
specific files)
- Scores all the race results and allocate points to the regional association
- Sorts them from the regional association who got the most points to least

The program also:
- lets you have the option to export to .CSV file
- Displays if there is an error
- Show Results in a table before saving to .CSV file

"""



h2 = "How to use?"

p2 = """
Step 1: Open your parent folder or the folder where the WakaNats Folders are stored.
- Open your folder by clicking "Open Folder" or typing the folder location on the 
input field then click next.


Step 2: Type Input details, This is where you specify what files you want to score.
- Type the year you want to score in the year input field
- (Optional) if you want to only score specific files such as "Finals" files, then
enter your "Finals" in the keyword input field. You can leave it blank if you
do not want to specifiy one
- You can also see the available years on a table in the left side and their
total files.

Step 3. Wait while loading
- By default, if there are file errors showing while loading, it is because the 
file have errors inside them. The errors shows what team/line and the file. 
You can take notes if you prefer. The erros show what team/row and the ile name. 
Potential causes may be number of fields are incorrect. 
- The program does not include the teams that have DNS/DQ/Disqualified tags.
- The program uses a default scoring criteria, You can configure further for
Waka Ama worlds.

These are only default settings. You can configure this on Home > Settings

Step 4. View the results on the results screen showing what year and keyword if 
specified. 
- This includes an option to export to CSV on the bottom
- This includes a table that shows the results before you export.
"""

h3 = "Additional"

p3 = """
Program Flexibility
- Includes settings for customization and flexibility
- The program considers different regional associations that may compete each year
by scoring all available teams in a year.
- The program considers different number of lanes
- Places and points criteria is configurable for Waka Ama worlds

"""

h4 = "Error Help"

p4 = """
“Used a different folder name for the Waka Ama Nationals Year Folder”
- By default, the program only find folder that have WakaNats(year).
if the years are renamed to something else, then the program will
not read those folders. Try to rename your folders to "WakaNats(year)".
e.g. WakaNats 2020

"Error on CSV Export"
- Make sure your

"Wrong results"
- Make sure you set up your settings value right because the program
will always stick from the settings provided

"There are no files of the keyword (Keyword specified)"
- by default, The filter keyword input field is CASE SENSITIVE. Always look
for spelling mistakes.
"""





# title_font
# heading_font



def fetch(frame,fonts):
    
    title = ct.CTkLabel(frame,text=title_text,justify="center",font=fonts.title_font)
    title.grid()

    heading1 = ct.CTkLabel(frame,text=h1,justify="center",font=fonts.heading_font)
    heading1.grid()

    par1 = ct.CTkLabel(frame,text=p1,justify="left")
    par1.grid()

    heading2 = ct.CTkLabel(frame,text=h2,justify="center",font=fonts.heading_font)
    heading2.grid()

    par2 = ct.CTkLabel(frame,text=p2,justify="left")
    par2.grid()

    heading3 = ct.CTkLabel(frame,text=h3,justify="center",font=fonts.heading_font)
    heading3.grid()

    par3 = ct.CTkLabel(frame,text=p3,justify="left")
    par3.grid()