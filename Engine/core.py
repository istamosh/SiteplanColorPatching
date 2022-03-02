import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from PIL import Image
imgPath = r"../Raw/Raw_KdPengawas_I.png"
csvPath = r"../Datas/patchdataset.csv"
plt.rcParams["figure.figsize"] = [6.4, 4.8]
plt.rcParams["figure.autolayout"] = True
img = Image.open(imgPath)

fig,ax = plt.subplots()

# draw frames config.
ax.axis('on')

# show main image and make it to frontmost layer
ax.imshow(img, zorder=3)

# draw patches, automated with csv, skip a line iteration if found an empty entry
with open(csvPath) as file:
	patchSet = csv.DictReader(file)

	for x in patchSet:
		if x['coordX'] == "" or x['expandX'] == "": continue
		ax.add_patch(patch.Rectangle((float(x['coordX']), float(x['coord-Y'])), float(x['expandX']), float(x['expand-Y']), facecolor=x['placeholder'], alpha=0.5))

## axis tick config.
## breakdown the limits of two axes and get the value
#_, x_max = plt.gca().get_xlim()
#y_min, _ = plt.gca().get_ylim()
## define max ranges
#x = np.random.randint(low=0, high=50, size=int(x_max))
#y = np.random.randint(low=0, high=50, size=int(y_min))
## set ranges between axis ticks
#ax.set_xticks(np.arange(0, len(x)+1, 25))
#ax.set_yticks(np.arange(0, len(y)+1, 25))


# rotate x axis text for readability
plt.xticks(rotation=45, ha='right')
# show plot result
plt.show()

# save plot result
# ax.axis('off')
# plt.axis('off')
# plt.savefig('../Exports/testexample_FigurePlot.pdf', format='pdf', dpi=600, bbox_inches='tight')