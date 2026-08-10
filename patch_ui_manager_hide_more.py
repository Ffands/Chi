import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

content = content.replace('addSection("Тайминги", hasTimingChanges)', 'val timingsSection = addSection("Тайминги", hasTimingChanges)')

find_hide_logic = """            if (node.type == NodeType.MANAGER) {
                conditionSection.visibility = View.GONE
                logicSection.visibility = View.GONE
                macroSection.visibility = View.GONE
                antiDetectSection.visibility = View.GONE
                syncSwipeSection.visibility = View.GONE
            }"""
repl_hide_logic = """            if (node.type == NodeType.MANAGER) {
                timingsSection.visibility = View.GONE
                logicSection.visibility = View.GONE
                routingSection.visibility = View.GONE
                macroSection.visibility = View.GONE
                antiDetectSection.visibility = View.GONE
                syncSwipeSection.visibility = View.GONE
            }"""
content = content.replace(find_hide_logic, repl_hide_logic)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Hide logic updated more")
