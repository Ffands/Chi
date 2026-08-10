import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_items = """            val items = arrayOf("КЛИК", "ТРИГГЕР", "МАКРОС")"""
repl_items = """            val items = arrayOf("КЛИК", "ТРИГГЕР", "МАКРОС", "МЕНЕДЖЕР")"""
content = content.replace(find_items, repl_items)

find_set = """            setSelection(when(node.type) {
                NodeType.CLICK -> 0
                NodeType.CHECK_COLOR -> 1
                NodeType.MACRO -> 2
            })"""
repl_set = """            setSelection(when(node.type) {
                NodeType.CLICK -> 0
                NodeType.CHECK_COLOR -> 1
                NodeType.MACRO -> 2
                NodeType.MANAGER -> 3
            })"""
content = content.replace(find_set, repl_set)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Spinner fixed fully")
