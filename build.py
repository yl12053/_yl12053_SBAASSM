import os, platform, subprocess
f = os.listdir("UiInit")
c = ["UiInit." + x.rsplit(".")[0] for x in f]
delim = ":"
if platform.system() == "Windows":
    delim = ";"
argl = ["pyinstaller", "-F", "Main.py", "--add-data", "AGENCYR.TTF" + delim + "."]
for d in c:
    argl.append("--hidden-import")
    argl.append(d)
subprocess.call(argl)