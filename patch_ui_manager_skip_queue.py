import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_skip = """        if (appMode == AppMode.ADVANCED) {
            if (node.type == NodeType.CHECK_COLOR || node.type == NodeType.MACRO) {"""
repl_skip = """        if (appMode == AppMode.ADVANCED) {
            if (node.type == NodeType.CHECK_COLOR || node.type == NodeType.MACRO || node.type == NodeType.MANAGER) {"""
content = content.replace(find_skip, repl_skip)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Skip switch updated")
