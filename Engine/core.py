import sys
import csv
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from matplotlib.backends.backend_pdf import PdfPages as pp
from PIL import Image
import easygui as ui

# paths
imgPath = [r"../Raw/Raw_KdPengawas_Approv_I.png", r"../Raw/Raw_KdPengawas_Approv_II.png"]
csvPath = r"../Datas/patchdataset.csv"
csvEncoding = 'utf-8-sig' #prevent false Encoding
exportPath = "../Exports/multiplePageTest.pdf"

# printout A3 portrait size and tight layout
plt.rcParams["figure.figsize"] = [11.7, 16.5]
plt.rcParams["figure.autolayout"] = True

# Figure I code
img1 = Image.open(imgPath[0])
fig,ax = plt.subplots()
ax.axis('on') # draw xy axes.
ax.imshow(img1, zorder=3) # show main image and make it to frontmost layer
fig.canvas.manager.set_window_title('Siteplan Phase I') # add name to window (placeholder)

# Figure II code
img2 = Image.open(imgPath[1])
fig2, ax2 = plt.subplots()
ax2.imshow(img2, zorder=3)
fig2.canvas.manager.set_window_title('Siteplan Phase II')

plt.yticks(rotation=90, ha='right') # rotate x axis text for readability

# Phase I legends properties
title1 = 'Lorem ipsum'
prop1 = [3500, 300, 20, 'left', 'bottom']
list1 = ['violet', 'lightgreen', 'cyan']
desc1 = ['commercial', 'subside', 'subside 5x12']

# draw patches, automated with csv, skip a line iteration if found an empty entry
with open(csvPath, encoding=csvEncoding) as file:
	reader = csv.DictReader(file)
	# list column after 'Spesifikasi' for later use
	entryColumn = []
	for idx, x in enumerate(reader.fieldnames):
		if idx > reader.fieldnames.index("Spesifikasi"):
			entryColumn.append(x)
	print(entryColumn)

	# go to phase II if block reaches d64
	phaseSeparator = 0
	for idx, row in enumerate(reader):
		if row['block'] == "d64":
			phaseSeparator = idx+1
			break
	print(phaseSeparator, " rows")

	# read csv from beginning
	file.seek(0)
	next(file)

	# negative color set for combining purpose
	fcSet = ['aqua','chartreuse','crimson']

	rowCounter = 0
	for row in reader:
		rowCounter += 1
		if rowCounter <= phaseSeparator:
			# skip if there are empty entries inside row (hardcoded check 'v' and alpha/opacity)
			# hardcoded version.
			# if rowCounter <= 3:
			# 	print(row['hehe'], "row index: ", rowCounter)
			if row[entryColumn[0]] == "v":
				ax.add_patch(patch.Rectangle((float(row['coordX']),
					float(row['coord-Y'])), float(row['expandX']),
					float(row['expand-Y']), fc=fcSet[0], alpha=0.5))
			if row[entryColumn[1]] == "v":
				ax.add_patch(patch.Rectangle((float(row['coordX']),
					float(row['coord-Y'])), float(row['expandX']),
					float(row['expand-Y']), fc=fcSet[1], alpha=0.5))
			if row[entryColumn[2]] == "v":
				ax.add_patch(patch.Rectangle((float(row['coordX']),
					float(row['coord-Y'])), float(row['expandX']),
					float(row['expand-Y']), fc=fcSet[2], alpha=0.5))

			# for idx, x in enumerate(entryColumn):
			# 	if row[x] == "v":
			# 		fc = fcSet[idx]
			# 		ax.add_patch(patch.Rectangle((float(row['coordX']), float(row['coord-Y'])), float(row['expandX']), float(row['expand-Y']), facecolor=row[fc], alpha=0.5))
		else:
			for x in entryColumn:
				if row[x] == "v":
					fc = fcSet[x]
					ax2.add_patch(patch.Rectangle((float(row['coordX']), float(row['coord-Y'])), float(row['expandX']), float(row['expand-Y']), facecolor=row[fc], alpha=0.5))
	
	if len(reader.fieldnames) > reader.fieldnames.index("Spesifikasi"):
		# add a legend title on phase I:
	 	ax.text(prop1[0], prop1[1], title1, size=prop1[2] ,ha=prop1[3], va=prop1[4])
	 	# add legends
	 	# legend y placement spacing below title
	 	j = prop1[1]+50

	 	for idx, x in enumerate(entryColumn):
	 		ax.add_patch(patch.Rectangle((prop1[0], j), 150, 150, facecolor=fcSet[idx], ec='black', alpha=0.5))
	 		ax.text(prop1[0]+250, j, entryColumn[idx], size=prop1[2]-(math.ceil(prop1[2]*50/100)), ha='left', va= 'top')
	 		j += 200

# defining a method for saving multipages PDF
def save_multiple_plot(fileName):
	ops = pp(fileName)
	fig_numbers = plt.get_fignums()
	figures = [plt.figure(n) for n in fig_numbers]
	for fig in figures:
		fig.savefig(ops, format='pdf', dpi=600, bbox_inches='tight')
	ops.close()

# codes for prompt window
choice = ui.buttonbox('Mau tampil atau PDF?', 'Pertanyaan', ('Tampil', 'PDF', 'Keluar'))
if choice == 'Tampil':
	plt.show()
elif choice == 'PDF':
	ax.axis('off')
	plt.axis('off')
	save_multiple_plot(exportPath)
else:
	sys.exit(0)