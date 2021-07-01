#!/usr/bin/env python3

# Parse an ASuite database into LNK files (Windows Shortcuts).
# Useful if you have an existing ASuite database that you want to use externally (Windows Search, Keypirinha, ...).

import shutil
import os
import sqlite3

# Use the pylnk3 library https://github.com/strayge/pylnk
import pylnk3

# All directory must have double backslash (one is escape character) and no last backslash

# ASuite database
_ASUITE_SQLITE_DB = "D:\\Apps\\ASuite\\asuite.sqlite"
# Base directory where all LNK shortcut will be created. The folder must already exist.
_TARGET_LNK_FOLDER = "D:\\Apps\\ASuite\\asuite2lnk\\"

# Variables used in Asuite to be replaced, without following backslash
_VAR_DRIVE = "D:"
_VAR_ASUITE = "D:\\Apps\\ASuite"
_VAR_SYSTEMROOT = "C:\\Windows"
_VAR_WINDIR = _VAR_SYSTEMROOT

# Column number in the database
_COLUMN_NO_TITLE = 4
_COLUMN_NO_PATH = 5
_COLUMN_NO_WORK_PATH = 6
_COLUMN_NO_PARAMETER = 7
_COLUMN_NO_ICON_PATH = 16

# Replace variables with fixed values defined above
def variables_to_fixed_value(var):
    var = var.replace("$drive", _VAR_DRIVE)
    var = var.replace("$Drive", _VAR_DRIVE)
    var = var.replace("$asuite", _VAR_ASUITE)
    var = var.replace("%systemroot%", _VAR_SYSTEMROOT)
    var = var.replace("%windir%", _VAR_WINDIR)
    return var

# Replace illegal characters according to Windows
def replace_illegal_characters(var):
    var = var.replace("/", "-")
    var = var.replace(":", "-")
    var = var.replace("*", "-")
    var = var.replace("?", "-")
    var = var.replace("\"", "-")
    var = var.replace("<", "-")
    var = var.replace(">", "-")
    var = var.replace("|", "-")
    return var

# Ask if user wants to purge folder
user_input = input("Press [p] to purge all file in the folder: ")
if user_input == "p":
    # Delete the directory
    shutil.rmtree(_TARGET_LNK_FOLDER)
    # Re-create it
    os.makedirs(_TARGET_LNK_FOLDER)
    print("Directory purged.")

# Read database
asuite_db = sqlite3.connect(_ASUITE_SQLITE_DB)
cursor = asuite_db.cursor()
cursor.execute('''SELECT * FROM tbl_list''')
tbl_list_asuite_db = cursor.fetchall();

# For each entries
for asuite_db_item in tbl_list_asuite_db:    

    # For each entries which have a defined folder path
    if asuite_db_item[_COLUMN_NO_PATH] != "":

        # Grab variables, replace path with fixed value
        lnk_title = replace_illegal_characters(asuite_db_item[_COLUMN_NO_TITLE])
        lnk_path = variables_to_fixed_value(asuite_db_item[_COLUMN_NO_PATH])
        lnk_work_path = variables_to_fixed_value(asuite_db_item[_COLUMN_NO_WORK_PATH])
        lnk_parameter = variables_to_fixed_value(asuite_db_item[_COLUMN_NO_PARAMETER])
        lnk_icon_path = variables_to_fixed_value(asuite_db_item[_COLUMN_NO_ICON_PATH])

        # Try to catch any error for non-supported objects (folder, url, ...)
        try:
            # Instanciate the lnk object, define parameters
            lnk = pylnk3.for_file(
                target_file = lnk_path,
                work_dir = lnk_work_path,
                arguments = lnk_parameter,
                icon_file = lnk_icon_path,
                )

            # Save the LNK file to the defined path
            lnk.save(_TARGET_LNK_FOLDER + lnk_title + ".lnk")

            del lnk
        
        # Print out the title of the catched error
        except:
            print("Error for title: " + lnk_title)
        
        finally:
            # Delete the all object
            del lnk_title, lnk_path, lnk_work_path, lnk_parameter, lnk_icon_path

print("ASuite2lnk done!")
input("Press enter to leave the script...")
