import os 
import sys

def get_upper_folder(depth=0):
    """
    Function used to access modules in upper folders.
    Depth determines, how high you want to go.
    """
    upper = os.path.sep.join(sys.path[0].split(os.path.sep)[:-depth])
    sys.path.append(upper)
