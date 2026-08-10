import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_hide_logic = """            if (node.type == NodeType.CHECK_COLOR || node.type == NodeType.MACRO) {
                swipeLayout.visibility = View.GONE
                swipeDurRow.visibility = View.GONE
                swipeDeltaLayout.visibility = View.GONE
                clickDurRow.visibility = View.GONE
            }"""
repl_hide_logic = """            if (node.type == NodeType.CHECK_COLOR || node.type == NodeType.MACRO || node.type == NodeType.MANAGER) {
                swipeLayout.visibility = View.GONE
                swipeDurRow.visibility = View.GONE
                swipeDeltaLayout.visibility = View.GONE
                clickDurRow.visibility = View.GONE
            }
            if (node.type == NodeType.MANAGER) {
                conditionSection.visibility = View.GONE
                logicSection.visibility = View.GONE
                macroSection.visibility = View.GONE
                antiDetectSection.visibility = View.GONE
                syncSwipeSection.visibility = View.GONE
            }"""

content = content.replace(find_hide_logic, repl_hide_logic)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Hide logic updated")
