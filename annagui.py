rom tkinter import *
from tkinter import messagebox
import untangle
import re
import time
import collections
import math
import os.path

#Function that displays texts on screen, filtering for Contacts and Search term
def display(*args):

	#Load function reads from xml file
	txts, contact, search, error = load()

	#Check if file was loaded
	if(error == "YES"):
		return 0


	if contact != "" and search != "":
		for sms in txts.smses.sms:
			if sms["contact_name"] == contact and search in sms["body"]:
				printout(sms)

	elif contact != "":
		for sms in txts.smses.sms:
			if sms["contact_name"] == contact:
				printout(sms)

	elif search != "":
		for sms in txts.smses.sms:
			if search in sms["body"]:
				printout(sms)

	else:
		for sms in txts.smses.sms:
			printout(sms)

	#Initialize scrollbar
	scrollbar()

#Function that prints out the text to the screen
def printout(sms):

	#Print date and time using time function. Divide by 1000 to convert into standard epoch time.
	output.insert(INSERT, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(sms["date"]) / 1000)) + " ",)
	
	#If this message was sent by someone else display their name
	if sms["type"] == "1":
		output.insert(INSERT, sms["contact_name"] + ": ")
	
	#If this message was sent by the user display "you"
	else:
		output.insert(INSERT, "You: ")

	#Print message body
	output.insert(INSERT, sms["body"])
	output.insert(INSERT, "\n")
	root.update_idletasks()

#Function that clears the text from the text field and uninitializes the scrollbar
def clear_text():
	output.delete(1.0, 'end')
	sb.configure(command=xml_entry.xview)
	output.configure(yscrollcommand=0)

#Function that analyzes the messages for Word Frequency and Incoming/Outgoing ratio 
def analyze(*args):

	#Load function reads from xml file
	txts, contact, search, error = load()

	#Check if file was loaded
	if(error == "YES"):
		return 0
	
	#Print out to text field
	output.insert(INSERT, "=" * 30)
	output.insert(INSERT, "\n")
	output.insert(INSERT, " MESSAGE ANALYSIS")
	output.insert(INSERT, "\n")
	output.insert(INSERT, "=" * 30)
	output.insert(INSERT, "\n")

	#Use count function
	incoming, outgoing = count(txts, contact, search)

	#Print out the Incoming, Outgoing ratio
	output.insert(INSERT, "Incoming: %s, Outgoing: %s" %(incoming, outgoing))
	output.insert(INSERT, "\n")
	if incoming and outgoing != 0: 
		output.insert(INSERT, "I/O Ratio: %s" %(round(incoming/outgoing, 2)))
	else:
		output.insert(INSERT, "I/O Ratio: N/A")
	output.insert(INSERT, "\n")
	output.insert(INSERT, "\n")
	root.update_idletasks()

	#Use average function
	average = size(txts, contact, search)

	output.insert(INSERT, "Average message size (in characters): %s" %(round(average, 2)))
	output.insert(INSERT, "\n")
	
	output.insert(INSERT, "\n")
	output.insert(INSERT, "\n")
	root.update_idletasks()

	if search == "":
		#Find the time between messages using timebet function
		timebetween = timebet(txts, contact, search)
		output.insert(INSERT, "Average time between replies: ")

		#If value is zero dont print it, other 
		if timebetween[0] != 0: output.insert(INSERT, "%s " %math.floor(timebetween[0]))
		if timebetween[0] > 1 and timebetween[2] != 0: 
			output.insert(INSERT, "years ") 
		elif timebetween[0] != 0: 
			output.insert(INSERT, "year ")

		if timebetween[1] != 0: output.insert(INSERT, "%s " %math.floor(timebetween[1]))
		if timebetween[1] > 1 and timebetween[2] != 0: 
			output.insert(INSERT, "months ")
		elif timebetween[1] != 0: 
			output.insert(INSERT, "month ")

		if timebetween[2] != 0: output.insert(INSERT, "%s " %math.floor(timebetween[2]))
		if timebetween[2] > 1 and timebetween[2] != 0: 
			output.insert(INSERT, "days ")
		elif timebetween[2] != 0: 
			output.insert(INSERT, "day ")

		if timebetween[3] != 0: output.insert(INSERT, "%s:" %math.floor(timebetween[3]))
		if timebetween[4] != 0: output.insert(INSERT, "%s:" %math.floor(timebetween[4]))
		if timebetween[5] < 9 and timebetween[5] != 0: output.insert(INSERT, "0")
		if timebetween[5] != 0: output.insert(INSERT, "%s" %math.floor(timebetween[5]))

		output.insert(INSERT, "\n")
		output.insert(INSERT, "\n")
		root.update_idletasks()


	#Print out heading
	output.insert(INSERT, "=" * 30)
	output.insert(INSERT, "\n")
	output.insert(INSERT, " WORD FREQUNCY ANALYSIS")
	output.insert(INSERT, "\n")
	output.insert(INSERT, "=" * 30)
	output.insert(INSERT, "\n")
	output.insert(INSERT, "\n")
	root.update_idletasks()

	#Append all the messages into a giant string
	if contact != "":
		all =  " ".join([sms['body'] for sms in txts.smses.sms if sms["contact_name"] == contact])
	else:
		all =  " ".join([sms['body'] for sms in txts.smses.sms])

	#Split the words up into a list of strings
	words = [w for w in re.split('\W', all) if w]

	#Put words into dictionary if not there, otherwise increase frequency
	dict = {}
	for key in words:

		if key in dict:
			dict[key] += 1
		else:
			dict[key] = 1

	#Sort dictionary into ordered dictionary
	ordict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

	#Print out a sorted list of all the words using the sorted function
	if search == "":
		for key in range(len(ordict)):
			output.insert(INSERT, (ordict[key][1], ":", ordict[key][0]))
			output.insert(INSERT, "\n")
			root.update_idletasks()

	else: 
		for key in range(len(ordict)):
			if search == ordict[key][0]:
				output.insert(INSERT, (ordict[key][1], ":", ordict[key][0]))
				output.insert(INSERT, "\n")
				root.update_idletasks()

	#Initialize scrollbar
	scrollbar()

#Function that displays Help MessageBox
def proghelp():
	messagebox.showinfo("ANNA Help","ANNA has two main features: displaying\
	SMS conversations backed up from Android phones in XML Format and performing\
	simple analysis on them.\n \nYou can search for a term and display or analyze\a particular contact. Have fun! \n\n \u00a9 2017 David Gorski")

#Function that reads the xml source, contact name and search term, loads the messages into memory, and returns txts, contact, search 
def load():

	#Retrieve contact and search term from entry fields
	contact = con.get()
	search = sear.get()

	#Clear the textbox
	clear_text()
	source = loc.get()

	check = 0
	#If source is empty, use default
	if source == "":
		check = 1
		output.insert(INSERT, "PLEASE ENTER AN XML SOURCE FILENAME")
		root.update_idletasks()


	if os.path.exists(source) == True:
		txts = untangle.parse(source)
	
	elif os.path.exists(source) == False and check == 0:
		output.insert(INSERT, "XML SOURCE FILE NOT FOUND")
		root.update_idletasks()
		return 0,0,0, "YES"

	return txts, contact, search, "NO"

#Funtion that inistialize the scrollbar (improves performance drastically)
def scrollbar():
	sb.configure(command=output.yview)
	output.configure(yscrollcommand=sb.set)

#Function that counts how many incoming and how many outgoing messages
def count(txts, contact, search):

	incoming = 0
	outgoing = 0

	if contact != "" and search != "":
		for sms in txts.smses.sms:
			if sms["type"] == "1" and sms["contact_name"] == contact and search in sms["body"]:
				incoming += 1
			elif sms["contact_name"] == contact and search in sms["body"]:
				outgoing += 1

	elif contact != "":
		for sms in txts.smses.sms:
			if sms["type"] == "1" and sms["contact_name"] == contact:
				incoming += 1
			elif sms["contact_name"] == contact:
				outgoing += 1

	elif search != "":
		for sms in txts.smses.sms:
			if sms["type"] == "1" and search in sms["body"]:
				incoming += 1
			elif search in sms["body"]:
				outgoing += 1

	else:
		for sms in txts.smses.sms:
			if sms["type"] == "1":
				incoming += 1
			else:
				outgoing += 1

	return incoming, outgoing

#Function that determines average message size
def size(txts, contact, search):
	lengths = []
	average = 0

	if contact != "" and search != "":
		for sms in txts.smses.sms:
			if sms["type"] == "1" and sms["contact_name"] == contact and search in sms["body"]:
				lengths.append(len(sms["body"]))

	elif contact != "":
		for sms in txts.smses.sms:
			if sms["type"] == "1" and sms["contact_name"] == contact:
				lengths.append(len(sms["body"]))



	elif search != "":
		for sms in txts.smses.sms:
			if sms["type"] == "1" and search in sms["body"]:
				lengths.append(len(sms["body"]))

	else:
		for sms in txts.smses.sms:
			if sms["type"] == "1":
				lengths.append(len(sms["body"]))

	if len(lengths) != 0: average = sum(lengths)/len(lengths)

	return average

#Function that determines the average time between messages
def timebet(txts, contact, search):
	prev = 0
	dict = []
	average = 0

	#If the previous contact name is the same the current contact name, skip the message, otherwise, add the date to the dict list
	if contact != "" and search != "":
		counter = 0
		for sms in txts.smses.sms:
			if sms["contact_name"] != txts.smses.sms[counter-1]["contact_name"] and sms["contact_name"] == contact and search in sms["body"]:
				dict.append(float(sms["date"]))
			counter+=1

	elif contact != "":
		counter = 0
		for sms in txts.smses.sms:
			if sms["contact_name"] != txts.smses.sms[counter-1]["contact_name"] and sms["contact_name"] == contact:
				dict.append(float(sms["date"]))
			counter+=1

	elif search != "":
		counter = 0
		for sms in txts.smses.sms:
			if sms["contact_name"] != txts.smses.sms[counter-1]["contact_name"] and search in sms["body"]:
				dict.append(float(sms["date"]))
			counter+=1

	else:
		counter = 0
		for sms in txts.smses.sms:
			if sms["contact_name"] != txts.smses.sms[counter-1]["contact_name"]:
				dict.append(float(sms["date"]))
			counter+=1

	#Find the differences between the consecutive elemetns of the list, add those to a new list called differences 
	differences = [j-i for i, j in zip(dict[:-1], dict[1:])]
	#Find the average of the differences, divide by 1000 to convert from milliseconds to seconds
	timebetween = (sum(differences)/len(differences))/1000

	# Use the convert function to convert from Unix time to regular values
	averagetime = []
	years, timebetween = convert(31536000, timebetween)
	averagetime.append(years)
	months, timebetween = convert(2592000, timebetween)
	averagetime.append(months)
	days, timebetween = convert(86400, timebetween)
	averagetime.append(days)
	hours, timebetween = convert(3600, timebetween)
	averagetime.append(hours)
	minutes, timebetween = convert(60, timebetween)
	averagetime.append(minutes)
	seconds, timebetween = convert(1, timebetween)
	averagetime.append(seconds)

	return averagetime

#Function that converts Unix time into an list of values representing years, months, days, hours, minutes, seconds
def convert(metric, timebetween):
	if timebetween//metric >= 1:
		back = (timebetween//metric)
		timebetween -= back*metric

	else:
		back = 0
	return back, timebetween

#Initialize root window, give it a title, configure
root = Tk()
root.title("ANNA: The Text Message Conversation Analysis Tool")
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(880, 735))

#Initilize mainframe 
mainframe = Frame(root)
mainframe.pack()

#Initialize subframe that will hold text box and scrollbar
subframe = Frame(mainframe)
subframe.grid(column = 1, row = 4, columnspan = 3, sticky=(N, W, E, S))

#Initilize necessary variables
loc = StringVar()
con = StringVar()
sear = StringVar()
messages = StringVar()

#Initialize entry boxes
xml_entry = Entry(mainframe, textvariable=loc, width = 70)
xml_entry.grid(column=2, row=1, sticky=W+E)
contact_entry = Entry(mainframe, textvariable=con)
contact_entry.grid(column=2, row=2, sticky=W+E)
search_entry = Entry(mainframe, textvariable=sear)
search_entry.grid(column=2, row=3, sticky=W+E)

#Initilize scrollbar
sb = Scrollbar(subframe,orient=VERTICAL)
sb.pack(side= RIGHT, fill=Y)

#Initialize buttons
Button(mainframe, text="Help", command=proghelp).grid(column=3, row=1, sticky=W+E)
Button(mainframe, text="Display", command=display).grid(column=3, row=3, sticky=W+E)
Button(mainframe, text="Analyze", command=analyze).grid(column=3, row=2, sticky=W+E)

#Initialize labels
Label(mainframe, text="XML Source File").grid(column=1, row=1, sticky=W)
Label(mainframe, text="Contact (Leave Blank for All)").grid(column=1, row=2, sticky=W)
Label(mainframe, text="Search for Term").grid(column=1, row=3, sticky=W)

#Initialize textbox
output = Text(subframe, bg = "White", fg = "Black", bd = 1, relief=SUNKEN, height = 40, width = 120, highlightthickness = 0)
output.pack(side = LEFT)

#Add padding
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#Begin main Tk loop
root.mainloop()


