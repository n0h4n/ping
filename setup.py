import cx_Freeze

#executables = [cx_Freeze.Executable("main_v2.py")]
import os 
os.environ['TCL_LIBRARY'] = "C:\\Users\\Nohan\\AppData\\Local\\Programs\\Python\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Nohan\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"

include = list()
include.append("C:\\Users\\Nohan\\AppData\\Local\\Programs\\Python\\Python35-32\\DLLs\\tk86t.dll")
include.append("C:\\Users\\Nohan\\AppData\\Local\\Programs\\Python\\Python35-32\\DLLs\\tcl86t.dll")

cx_Freeze.setup(
	name="Ping",
	options={"build_exe":{"packages":["tkinter","threading","time","socket","client","misc"],"include_files":include}},
	description="Pong",
	version="0.1.0",
	executables=[cx_Freeze.Executable("main.py",base = "Win32GUI")]

	)
