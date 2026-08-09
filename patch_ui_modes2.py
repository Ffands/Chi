import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Wrap logicSection
logic_start = """        val hasLogicChanges = node.targetColor != null || node.targetImageBase64 != null || node.targetText != null || node.colorOperator != "==" || node.colorTolerance != 15 || node.linkedConditionNodeId != null || node.compareToNodeId != null || node.dynamicColorUpdate || node.triggerMode >= 0
        val logicSection = addSection("Настройки Триггера", hasLogicChanges) { body ->"""

logic_new = """        val hasLogicChanges = node.targetColor != null || node.targetImageBase64 != null || node.targetText != null || node.colorOperator != "==" || node.colorTolerance != 15 || node.linkedConditionNodeId != null || node.compareToNodeId != null || node.dynamicColorUpdate || node.triggerMode >= 0
        if (appMode == AppMode.ADVANCED || appMode == AppMode.SEQUENTIAL || appMode == AppMode.SINGLE) {
        val logicSection = addSection("Настройки Триггера", hasLogicChanges) { body ->"""
content = content.replace(logic_start, logic_new)
content = content.replace("""        val routingSection =""", """        } // logicSection
        val routingSection =""")

routing_start = """        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->"""
routing_new = """        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
        if (appMode == AppMode.ADVANCED) {
        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->"""
content = content.replace(routing_start, routing_new)
content = content.replace("""        val hasSwipeChanges =""", """        } // routingSection
        val hasSwipeChanges =""")

sync_start = """        val syncSwipeSection = addSection("Настройки Действий", hasSwipeChanges) { body ->"""
sync_new = """        if (appMode == AppMode.ADVANCED || appMode == AppMode.SEQUENTIAL) {
        val syncSwipeSection = addSection("Настройки Действий", hasSwipeChanges) { body ->"""
content = content.replace(sync_start, sync_new)
content = content.replace("""        val saveBtn = Button(service).apply {""", """        } // syncSwipeSection
        val saveBtn = Button(service).apply {""")

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Edit Node Menu modes patched")
