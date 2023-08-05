name = "pydatasci"

import sqlite3
import appdirs


def create_ml_database():
	app_dir = appdirs.user_data_dir(name)
	db_name = 'mldb.sqlite3'
	full_db_path = app_dir + db_name
	conn = sqlite3.connect(full_db_path)
	del conn
	print("Created database for machine learning metrics at path: " + full_db_path)


def say():
	print("A little something into the camera.")
