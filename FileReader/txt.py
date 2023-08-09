import os, time

from PyQt5.QtWidgets import QFileDialog

def process(dirname):
    try:
        return (0, open(dirname).read().strip())
    except UnicodeDecodeError:
        return (1, "File using unknown encoding.")
    except Exception as e:
        return (1, str(e))

def exportRaw(compo):
    export = ""
    for cobj in compo.getMark().values():
        edict = cobj.export()
        export += f"=== {list(edict.keys())[0]} ===\n"
        for detail in list(edict.values())[0]:
            k, p = tuple(detail)
            if not isinstance(p, set) and not isinstance(p, list):
                export += f"{k}: {p}\n"
        export += "\n"
    export += f"This report is generated at {time.strftime('%a, %d %b %Y %H:%M:%S')}"
    return export.encode()

def export(compo):
    choose = QFileDialog.getSaveFileName(None, "Export to", os.getcwd(), "Plain Text Files (*.txt)")
    if choose:
        f = open(choose[0], "wb")
        f.write(exportRaw(compo))
        f.close()