import customtkinter as CT
# https://pypi.org/project/tkhtmlview/
# markdown to html library
import markdown
from tkhtmlview import HTMLLabel # external library



"""
Creating tkinter labels solely will be very challenging because I will need to manually
configure the layout system, long lines of texts and complex formatting.

I will need HTML tkinter renderer library and markdown to html library



"""


def get_help_contents(gui_instance,frame):
    
    """
    sheading - short for subheading
    sec(num) - short for section. Represents the section title and its section place
    psec(num) - Represents the paragraph/body of the section and its section place
    """


    


    title = "Official Help page"
    sheading = ""

    
    sec1 = "About"
    ph1 = ""



    sec2 = "How to use"
    ph2 = ""


    sec3 = "Need Help"
    ph3 = ""


    sec4 = "Fixing Errors"
    ph4 = ""


    sec5 = "More information on github"
    ph5 = ""
























    # Adding the widget objects


    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()

    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()
    
    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()

    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()
    
    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()

    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()

    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()

    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()

    titleLabel = CT.CTkLabel(gui_instance.current_frame, text=title)
    titleLabel.grid()