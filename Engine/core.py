import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from matplotlib.backends.backend_pdf import PdfPages as pp
from PIL import Image
import easygui as ui

# paths
imgPath = [r"../Raw/Raw_KdPengawas_I.png", r"../Raw/Raw_KdPengawas_II.png"]
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

# draw patches, automated with csv, skip a line iteration if found an empty entry
with open(csvPath) as file:
	reader = csv.DictReader(file)
	totalRow = 0
	for x in reader:
		totalRow += 1
		if totalRow <= 1677:
			if x['coordX'] == "" or x['expandX'] == "":
				continue
			ax.add_patch(patch.Rectangle((float(x['coordX']), float(x['coord-Y'])), float(x['expandX']), float(x['expand-Y']), facecolor=x['placeholder'], alpha=0.5))
		else:
			if x['coordX'] == "" or x['expandX'] == "":
				continue
			ax2.add_patch(patch.Rectangle((float(x['coordX']), float(x['coord-Y'])), float(x['expandX']), float(x['expand-Y']), facecolor=x['placeholder'], alpha=0.5))
	print(totalRow)

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