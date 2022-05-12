import sys
import os
import tkinter as tk
from tkinter.ttk import *
import csv
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from matplotlib.backends.backend_pdf import PdfPages as pp
from matplotlib import backend_bases
from PIL import Image
import easygui as ui

# loading bar appearance window
window = tk.Tk()
window.title('Loading')
load = Progressbar(window,
	orient=tk.HORIZONTAL,
	length=300,
	mode='determinate')
label = Label(window, text="Loading...")
load.pack() # load and pack inside said window
label.pack()

# loading bar worker
progress = 0
def bar(textVal):
	if 'progress' in locals():
		global progress
	if load['value'] > 99:
		window.withdraw() # withdraw the loading bar window so it doesn't appear again when opening another tkinter window
		return # stops here so below code doesn't get exec'd
	import time
	progress += 12.5
	load['value'] = progress
	label.config(text=textVal+"...")
	window.update() # update the appearance of said window
	time.sleep(1)

# paths
bar("Reading site plan")
imgPath = ["Raw_KdPengawas_Approv_I.png", "Raw_KdPengawas_Approv_II.png"]
# printout A3 portrait size and tight layout
bar("Setting up figure layout")
plt.rcParams["figure.figsize"] = [11.7, 16.5]
plt.rcParams["figure.autolayout"] = True
# disable some original matplotlib button for viewing purpose
bar("Adjusting layout")
backend_bases.NavigationToolbar2.toolitems = (
	('Home', 'Reset original view', 'home', 'home'),
    ('Back', 'Back to  previous view', 'back', 'back'),
    ('Forward', 'Forward to next view', 'forward', 'forward'),
    (None, None, None, None),
    ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
    ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
    #('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
    (None, None, None, None),
    #('Save', 'Save the figure', 'filesave', 'save_figure'),
	)
# some monkeypatching after code above (thx to freude from stackoverflow)
bar("Syncing layout")
if matplotlib.get_backend() == 'Qt5Agg':
    from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
    def _update_buttons_checked(self):
        # sync button checkstates to match active mode (patched)
        if 'pan' in self._actions:
            self._actions['pan'].setChecked(self._active == 'PAN')
        if 'zoom' in self._actions:
            self._actions['zoom'].setChecked(self._active == 'ZOOM')
    NavigationToolbar2QT._update_buttons_checked = _update_buttons_checked
# patch config.
bar("Configuring patch colors")
opacity = 1.0
fcSet = ['magenta','yellow','cyan',
			'red','green','blue',
			'mediumvioletred','orange','yellowgreen',
			'lime','dodgerblue','mediumpurple']
# for file bundling purposes (thx to max from stackoverflow)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
# Figure I code
bar("Initializing site plan phase 1")
img1 = Image.open(resource_path(imgPath[0]))
fig,ax = plt.subplots()
ax.axis('on') # draw xy axes.
ax.imshow(img1, zorder=3) # show main image and make it to frontmost layer
fig.canvas.manager.set_window_title('Siteplan Phase I') # add name to window (placeholder)
plt.yticks(rotation=90, ha='right', va='center') # rotate x axis text for readability
# Figure II code
bar("Initializing site plan phase 2")
img2 = Image.open(resource_path(imgPath[1]))
fig2, ax2 = plt.subplots()
ax2.imshow(img2, zorder=3)
fig2.canvas.manager.set_window_title('Siteplan Phase II')
plt.yticks(rotation=90, ha='right', va='center') # rotate x axis text for readability
# Legends properties
bar("Working on coordinates")
ymax, _ = ax.get_ylim()
_ , xmax = ax2.get_xlim()
placementProp = [3500, math.floor(ymax*3/100), 20, 'left', 'top']
leg2 = [7000, _]
# draw patches, automated with csv, skip a line iteration if found an empty entry
def doWork():
	fetch = promptMenus()
	workingPath = fetch[0].rsplit("/", 1)
	os.chdir(workingPath[0])
	with open(workingPath[1], encoding='utf-8-sig') as file:
		reader = csv.DictReader(file)
		# list column and its patch counter after 'Spesifikasi' for later use
		entryColumn = []
		placeholderCounter = []
		for idx, x in enumerate(reader.fieldnames):
			if idx > reader.fieldnames.index("Spesifikasi"):
				entryColumn.append(x)
				placeholderCounter.append(0)
	
		# go to phase II if block reaches d64
		phaseSeparator = 0
		for idx, row in enumerate(reader):
			if row['block'] == "d64":
				phaseSeparator = idx+1
				break
	
		# read csv from beginning
		file.seek(0)
		next(file)
	
		# add color(s) based on entry column(s)
		if len(entryColumn) <= 12:
			rowCounter = 0
			for row in reader:
				rowCounter += 1
				if rowCounter < phaseSeparator:
					# skip if there are empty entries inside row (hardcoded check 'v' and alpha/opacity)
					for idx, x in enumerate(entryColumn):
						if row[x] == "v":
							ax.add_patch(patch.Rectangle((float(row['coordX']),
							float(row['coord-Y'])), float(row['expandX']),
							float(row['expand-Y']), fc=fcSet[idx], alpha=opacity))
							placeholderCounter[idx] += 1
				else:
					for idx, x in enumerate(entryColumn):
						if row[x] == "v":
							ax2.add_patch(patch.Rectangle((float(row['coordX']),
							float(row['coord-Y'])), float(row['expandX']),
							float(row['expand-Y']), fc=fcSet[idx], alpha=opacity))
							placeholderCounter[idx] += 1
			
			if len(reader.fieldnames) > reader.fieldnames.index("Spesifikasi"):
				# add legends
			 	# legend y placement spacing below title
			 	vertTolerance = placementProp[1]+math.ceil(placementProp[1]*50/100)
			 	horzTolerance = placementProp[0]+1500
			 	vertTolerance1 = vertTolerance
			 	legendSize = 150
			 	angle = -90
	
				# add a legend title on phase I:
			 	ax.text(placementProp[0], placementProp[1], fetch[1],
			 		size=placementProp[2] ,ha=placementProp[3], va=placementProp[4])
			 	ax2.text(xmax-placementProp[1], leg2[0], fetch[1],
			 		rotation=angle,	size=placementProp[2], 
			 		ha='right', va='top')

			 	for idx, x in enumerate(entryColumn):
			 		if idx <= 5:
			 			# phase I
				 		ax.add_patch(patch.Rectangle((placementProp[0], vertTolerance+100),
				 			legendSize, legendSize, fc=fcSet[idx], ec='black', alpha=opacity))
				 		ax.text(placementProp[0]+250, vertTolerance+math.floor(legendSize*50/100)+100,
				 		 	entryColumn[idx] + " (" + str(placeholderCounter[idx]) +")", 
				 		 	size=placementProp[2]-math.ceil(placementProp[2]*25/100),
				 			ha='left', va='center')
	
				 		# phase II
				 		ax2.add_patch(patch.Rectangle((xmax-placementProp[1]-vertTolerance, leg2[0]),
				 			legendSize, legendSize, fc=fcSet[idx], ec='black', alpha=opacity))
				 		ax2.text(xmax-250-vertTolerance, leg2[0]+250,
				 			entryColumn[idx] + " (" + str(placeholderCounter[idx]) +")", 
				 			size=placementProp[2]-math.ceil(placementProp[2]*25/100),
				 			ha='center', va='top', rotation=angle)
	
				 		vertTolerance += 200
				 	else:
				 		# phase I
				 		ax.add_patch(patch.Rectangle((horzTolerance, vertTolerance1+100),
				 			legendSize, legendSize, fc=fcSet[idx], ec='black', alpha=opacity))
				 		ax.text(horzTolerance+250, vertTolerance1+math.floor(legendSize*50/100)+100,
				 		 	entryColumn[idx] + " (" + str(placeholderCounter[idx]) +")", 
				 		 	size=placementProp[2]-math.ceil(placementProp[2]*25/100),
				 			ha='left', va='center')
	
				 		# phase II
				 		ax2.add_patch(patch.Rectangle((xmax-placementProp[1]-vertTolerance1, leg2[0]+1500),
				 			legendSize, legendSize, fc=fcSet[idx], ec='black', alpha=opacity))
				 		ax2.text(xmax-vertTolerance1-250, leg2[0]+1500+250,
				 			entryColumn[idx] + " (" + str(placeholderCounter[idx]) +")", 
				 			size=placementProp[2]-math.ceil(placementProp[2]*25/100),
				 			ha='center', va='top', rotation=angle)
	
				 		vertTolerance1 += 200
	return fetch[0]			 		
# defining a method for saving multipages PDF
def save_multiple_plot(fileName):
	ops = pp(fileName)
	fig_numbers = plt.get_fignums()
	figures = [plt.figure(n) for n in fig_numbers]
	for fig in figures:
		fig.savefig(ops, format='pdf', dpi=600, bbox_inches='tight')
	ops.close()
	tk.messagebox.showinfo("Info","Selesai export ke PDF!")

def promptMenus():
	targetPath = tk.filedialog.askopenfilename(title="Pilih file CSV",
		filetypes=(("CSV Files", "*.csv"),))
	if targetPath == None or targetPath == "":
		terminate()
		return None
	legendTitle = ui.enterbox("Input judul legenda:", "Pertanyaan", "ketik disini...")
	if legendTitle == None:
		terminate()
		return None
	return targetPath, legendTitle

def terminate():
	sys.exit(0)

bar("ok")
# codes for prompt window
choice = ui.buttonbox('Ingin tampil atau PDF?', 'Pertanyaan', ('Tampil', 'PDF', 'Keluar'))
if choice == 'Tampil':
	doWork()
	plt.show()
elif choice == 'PDF':
	_targetPath = doWork()
	targetPdf = _targetPath.rsplit(".", 1)[0] + ".pdf"
	ax.axis('off')
	plt.axis('off')
	save_multiple_plot(targetPdf)
else:
	terminate()