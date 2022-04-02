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
with open(csvPath) as file:
	reader = csv.DictReader(file)
	totalCol = len(reader.fieldnames)
	print(totalCol)
	totalRow = 0
	for x in reader:
		totalRow += 1
		if totalRow <= 1677:
			if x['placement'] == "" or x['coordX'] == "" or x['expandX'] == "":
				continue
			ax.add_patch(patch.Rectangle((float(x['coordX']), float(x['coord-Y'])), float(x['expandX']), float(x['expand-Y']), facecolor=x['placeholder'], alpha=0.5))
		else:
			if x['placement'] == "" or x['coordX'] == "" or x['expandX'] == "":
				continue
			ax2.add_patch(patch.Rectangle((float(x['coordX']), float(x['coord-Y'])), float(x['expandX']), float(x['expand-Y']), facecolor=x['placeholder'], alpha=0.5))
	if totalCol >= 8:
		# add a legend title on phase I:
	 	ax.text(prop1[0], prop1[1], title1, size=prop1[2] ,horizontalalignment=prop1[3], verticalalignment=prop1[4])
	 	# add legends
	 	# placeholder for 3 legends marker
	 	i = totalCol-8
	 	# legend y placement spacing below title
	 	j = prop1[1]+50

	 	for x in range(i):
	 		ax.add_patch(patch.Rectangle((prop1[0], j), 150, 150, facecolor=list1[x], ec='black', alpha=0.5))
	 		ax.text(prop1[0]+250, j, desc1[x], size=prop1[2]-(math.ceil(prop1[2]*50/100)), horizontalalignment='left', verticalalignment= 'top')
	 		j += 200

# a method for saving multipages PDF
def save_multiple_plot(fileName):
	ops = pp(fileName)
	fig_numbers = plt.get_fignums()
	figures = [plt.figure(n) for n in fig_numbers]
	for fig in figures:
		fig.savefig(ops, format='pdf', dpi=600, bbox_inches='tight')
	ops.close()

# codes for prompt window
choice = ui.buttonbox('Mau tampil atau PDF?', 'Pertanyaan', ('Tampil', 'PDF'))
if choice == 'Tampil':
	plt.show()
else:
	ax.axis('off')
	plt.axis('off')
	save_multiple_plot(exportPath)