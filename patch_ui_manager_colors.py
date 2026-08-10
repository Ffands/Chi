import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_add = """            crosshairColor = if (type == NodeType.CLICK) Color.RED else Color.BLUE"""
repl_add = """            crosshairColor = if (type == NodeType.CLICK) Color.RED else if (type == NodeType.MANAGER) Color.parseColor("#9C27B0") else Color.BLUE"""
content = content.replace(find_add, repl_add)

find_spinner_change = """                    if (node.type != newType) {
                        node.type = newType"""
repl_spinner_change = """                    if (node.type != newType) {
                        node.type = newType
                        node.crosshairColor = if (node.type == NodeType.CLICK) Color.RED else if (node.type == NodeType.MANAGER) Color.parseColor("#9C27B0") else Color.BLUE
                        nodeViews[node.id]?.invalidate()"""
content = content.replace(find_spinner_change, repl_spinner_change)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Colors updated")
