name = "pydatasci"

import os
from os import path

import appdirs, sqlite3


app_name = "pydatasci"

def directoree(app_name):
	app_dir = user_data_dir(app_name)
	print(app_dir)

def say():
	print("A little something into the camera.")
