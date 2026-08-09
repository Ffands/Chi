import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Remove logicSection if
logic_target = """        val hasLogicChanges = node.targetColor != null || node.targetImageBase64 != null || node.targetText != null || node.colorOperator != "==" || node.colorTolerance != 15 || node.linkedConditionNodeId != null || node.compareToNodeId != null || node.dynamicColorUpdate || node.triggerMode >= 0
        if (appMode == AppMode.ADVANCED || appMode == AppMode.SEQUENTIAL || appMode == AppMode.SINGLE) {
        val logicSection = addSection("Настройки Триггера", hasLogicChanges) { body ->"""
logic_repl = """        val hasLogicChanges = node.targetColor != null || node.targetImageBase64 != null || node.targetText != null || node.colorOperator != "==" || node.colorTolerance != 15 || node.linkedConditionNodeId != null || node.compareToNodeId != null || node.dynamicColorUpdate || node.triggerMode >= 0
        val logicSection = addSection("Настройки Триггера", hasLogicChanges) { body ->"""
content = content.replace(logic_target, logic_repl)

# Remove } // logicSection and routing if
routing_target = """        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
        } // logicSection
        if (appMode == AppMode.ADVANCED) {
        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->"""
routing_repl = """        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->"""
content = content.replace(routing_target, routing_repl)

# Wait, checking what was actually inserted for routing:
# Actually my script did:
#        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
#        } // logicSection
#        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->
# Wait, let me check the file content first.

