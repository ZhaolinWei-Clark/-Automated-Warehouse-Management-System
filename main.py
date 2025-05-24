###################################################################################
#  Project:      Automated Warehouse Management System                            #
#  File:         main.py                                                          #
#  Team members: Kushal Sedhai     Haoyuan Jiang     Zhaolin Wei                  #
#  Student ID:   60286127          14636898          89282347                     #
#  Purpose:      Entry for the program.                                           #
#  Description:  This file serves as the entry point to the Automated Warehouse   #
#                Management System. It initializes the warehouse environment      #
#                and launches the graphical interface for interaction.            #
###################################################################################

#################################### IMPORTS ######################################

from warehouse import Warehouse
from gui import GUI

############################## MAIN PROGRAM EXECUTION #############################
if __name__ == '__main__':
    warehouse = Warehouse(length=20, width=20)
    gui = GUI(warehouse)
    gui.run()