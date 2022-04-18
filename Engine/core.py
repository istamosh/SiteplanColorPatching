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

# patch config.
opacity = 1.0
fcSet = ['red','royalblue','yellow',
			'magenta','limegreen','orange',
			'deeppink','darkviolet','cyan',
			'chartreuse','goldenrod','orangered']

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
ymax, _ = ax.get_ylim()
legendTitle = 'Lorem ipsum'
placementProp = [3500, math.floor(ymax*3/100), 20, 'left', 'bottom']

# draw patches, automated with csv, skip a line iteration if found an empty entry
with open(csvPath, encoding=csvEncoding) as file:
	reader = csv.DictReader(file)
	# list column after 'Spesifikasi' for later use
	entryColumn = []
	for idx, x in enumerate(reader.fieldnames):
		if idx > reader.fieldnames.index("Spesifikasi"):
			entryColumn.append(x)

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
			else:
				for idx, x in enumerate(entryColumn):
					if row[x] == "v":
						ax2.add_patch(patch.Rectangle((float(row['coordX']),
						float(row['coord-Y'])), float(row['expandX']),
						float(row['expand-Y']), fc=fcSet[idx], alpha=opacity))
		
		if len(reader.fieldnames) > reader.fieldnames.index("Spesifikasi"):
			# add a legend title on phase I:
		 	ax.text(placementProp[0], placementProp[1], legendTitle,
		 		size=placementProp[2] ,ha=placementProp[3], va=placementProp[4])

		 	# add legends
		 	# legend y placement spacing below title
		 	vertTolerance = placementProp[1]+(math.ceil(placementProp[1]*16.7/100))
		 	horzTolerance = placementProp[0]+1500
		 	vertTolerance1 = vertTolerance

		 	for idx, x in enumerate(entryColumn):
		 		if idx <= 5:
			 		ax.add_patch(patch.Rectangle((placementProp[0], vertTolerance),
			 			150, 150, fc=fcSet[idx], ec='black', alpha=opacity))
			 		ax.text(placementProp[0]+250, vertTolerance, entryColumn[idx],
			 			size=placementProp[2]-(math.ceil(placementProp[2]*25/100)),
			 			ha='left', va='top')
			 		vertTolerance += 200
			 	else:
			 		ax.add_patch(patch.Rectangle((horzTolerance, vertTolerance1),
			 			150, 150, fc=fcSet[idx], ec='black', alpha=opacity))
			 		ax.text(horzTolerance+250, vertTolerance1, entryColumn[idx],
			 			size=placementProp[2]-(math.ceil(placementProp[2]*25/100)),
			 			ha='left', va='top')
			 		vertTolerance1 += 200

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