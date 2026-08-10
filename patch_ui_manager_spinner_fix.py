import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_spinner = """                    val newType = when(pos) {
                        0 -> NodeType.CLICK
                        1 -> NodeType.CHECK_COLOR
                        2 -> NodeType.MACRO
                        else -> NodeType.CLICK
                    }"""
repl_spinner = """                    val newType = when(pos) {
                        0 -> NodeType.CLICK
                        1 -> NodeType.CHECK_COLOR
                        2 -> NodeType.MACRO
                        3 -> NodeType.MANAGER
                        else -> NodeType.CLICK
                    }"""

content = content.replace(find_spinner, repl_spinner)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Spinner fixed")
