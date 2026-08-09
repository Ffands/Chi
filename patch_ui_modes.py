import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# For routing Section
routing_old = """        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->"""
routing_new = """        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->"""

content = content.replace(routing_old, routing_new)

# Wait, let's just do it directly when we add them to the content!
add_sections_old = """        content.addView(headerLayout)
        
        val antiDetectSection = addSection("Анти-Детект", hasAntiDetect) { body ->
"""

# I need to find where they are added to `content`.
# Let's search for `content.addView(logicSection)`
