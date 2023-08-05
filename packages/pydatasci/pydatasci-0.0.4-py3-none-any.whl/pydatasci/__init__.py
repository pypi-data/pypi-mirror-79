name = "pydatasci"

import os, sqlite3
from os import path

import appdirs


def directoree():
	app_dir = appdirs.user_data_dir(name)
	print(app_dir)

def say():
	print("A little something into the camera.")
