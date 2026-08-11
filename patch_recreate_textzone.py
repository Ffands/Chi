import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """            if (node.triggerMode == 0 && !node.dynamicColorUpdate && node.compareToNodeId == null && node.colorCompareX != null) {
                createColorCompareMarker(node)
            }
        }
        updateMenu()"""

good_str = """            if (node.triggerMode == 0 && !node.dynamicColorUpdate && node.compareToNodeId == null && node.colorCompareX != null) {
                createColorCompareMarker(node)
            }
            if ((node.triggerMode == 1 || node.triggerMode == 2) && node.textZoneStartX != 0) {
                createTextZoneMarkers(node)
            }
        }
        updateMenu()"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("recreate textzone patched")
