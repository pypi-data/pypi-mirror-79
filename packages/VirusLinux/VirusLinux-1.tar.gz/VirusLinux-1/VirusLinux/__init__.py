# importing tkinter module 
from tkinter import * 
from tkinter.ttk import *
import os
import platform 

root = Tk() 
root.title("")
root.geometry("600x200")

label = Label( root, text="Installing.....")
label.pack()
# Progress bar widget 
progress = Progressbar(root, orient = HORIZONTAL, 
			length = 200, mode = 'determinate') 

# Function responsible for the updation 
# of the progress bar value 
size = "200x200"


def prank(value,title,labeltext,size=size):
    for i in range(0,value):
        # print(string)
        root = Tk()
        root.title(title)
        root.geometry(size)
      
		
        label = Label(root, text=labeltext)
        label.pack()
		
		
        root.mainloop()

		

	

def bar(): 
    
	import time 
    
	progress['value'] = 20
	root.update_idletasks() 
	time.sleep(1) 

	progress['value'] = 40
	root.update_idletasks() 
	time.sleep(1) 

	progress['value'] = 50
	root.update_idletasks() 
	time.sleep(1) 

	progress['value'] = 60
	root.update_idletasks() 
	time.sleep(1) 

	progress['value'] = 80
	root.update_idletasks() 
	time.sleep(1) 
	progress['value'] = 100

progress.pack(pady = 10) 

# This button will initialize 
# the progress bar 

def fakefile(rangevalue):
    for i in range(0,rangevalue):
        f = open("Desktop/" + str(i) + ".exe", "x")
       	f.write("Woops! I have deleted the content!")
        f.close
		 


my_system = platform.uname() 

        
label = Label(root,text="System : " + my_system.system)
label.pack()
label = Label(root,text="Node Name : " + my_system.node)
label.pack()
label = Label(root,text="Release : " + my_system.release)
label.pack()
label = Label(root,text="Processor : " + my_system.processor)
label.pack()

label = Label(root,text="Machine : " + my_system.machine)
label.pack()


label = Label(root,text="Version : " + my_system.version)
label.pack()


label = Label(root,text="Made By : Kr Rathod ")
label.pack()



bar()
def shutdown():
	os.system("shutdown now -h")
	


mainloop() 
