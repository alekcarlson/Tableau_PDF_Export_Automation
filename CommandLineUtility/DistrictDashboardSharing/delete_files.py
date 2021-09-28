import os

districtdirectory = "C:/Users/Administrator/CommandLineUtility/DistrictDashboardSharing/SOME_DASHBOARDExports_Script"
countydirectory = "C:/Users/Administrator/CommandLineUtility/DistrictDashboardSharing/SOME_DASHBOARDExports_ScriptCounty"
maindir = "C:/Users/Administrator/CommandLineUtility/DistrictDashboardSharing"

for f in os.listdir(districtdirectory):
    if f.endswith(".pdf"):
        os.remove(os.path.join(districtdirectory, f))

for f in os.listdir(countydirectory):
    if f.endswith(".pdf"):
        os.remove(os.path.join(countydirectory, f))

os.remove(os.path.join(maindir, "districts.csv"))
os.remove(os.path.join(maindir, "counties.csv"))
