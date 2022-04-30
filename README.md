# SiteplanColorPlot
Siteplan color patching project for Kedung Pengawas (Green New Residence) Housing.

I made this so our colleague don't have to manually print then color the blocks using coloring marker, or even manual color-hatching inside autoCAD or edited in photoshop one by one, time is money.

How to use:
- Download these files (obviously)
- Go to \Engine\dist folder, and open the .exe file
- Choose "Tampil" for showing patched site plan without the need of saving as PDF, or "PDF" for export as 2-pages PDF
- Both choices will ask you where you save the formatted .csv file, go to \Datas\Test CSV and choose BlockReference.csv
- Name a title for the legend
- Choosing Tampil will show two windows, choosing magnifying glass button then click-drag the plot screen to zoom the said area, while arrow button to pan the plot screen
- Choosing PDF menu will require you to wait then a message box will show up telling you the export is completed
- You may want to edit the CSV before accessing the EXE by adding up to 12 headers right after "Spesifikasi" header then adding "v" below it to color-patch the adjacent row, more information regarding this line can be seen on patchdataset.csv


Note:
- Choosing PDF menu will make a PDF with same name and directory beside the CSV, so make sure to move old PDF so it doesn't get replaced.
- Accessing PDF while it's loading will interrupt the exporting processes
- Adding other than "v" mark is currently unrecognized by the program, this will change in the future release
- CSV is encoded in UTF-8, so it's recommended to save as CSV UTF-8 (Comma delimited) format


Libs used:
- matplotlib as the color patcher and visualization engine
- tkinter and easygui as the UI
