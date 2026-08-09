import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Fix logicSection
content = content.replace(
"""        if (appMode == AppMode.ADVANCED || appMode == AppMode.SEQUENTIAL || appMode == AppMode.SINGLE) {
        val logicSection = addSection("Настройки Триггера", hasLogicChanges) { body ->""",
"""        val logicSection = addSection("Настройки Триггера", hasLogicChanges) { body ->"""
)

# Fix routingSection
content = content.replace(
"""        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
        } // logicSection
        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->""",
"""        val hasRoutingChanges = node.nextNodeIdOnSuccess != null || node.nextNodeIdOnFail != null || node.maxCheckCycles != null
        val routingSection = addSection("Маршрутизация (Ветвление)", hasRoutingChanges) { body ->"""
)

# Fix syncSwipeSection
content = content.replace(
"""        val hasSwipeChanges = node.syncWithNodeIds.isNotEmpty() || node.isSwipe || node.swipeTargetNodeId != null || node.swipeDurationMs != 500L
        if (appMode == AppMode.ADVANCED || appMode == AppMode.SEQUENTIAL) {
        val syncSwipeSection = addSection("Настройки Действий", hasSwipeChanges) { body ->""",
"""        val hasSwipeChanges = node.syncWithNodeIds.isNotEmpty() || node.isSwipe || node.swipeTargetNodeId != null || node.swipeDurationMs != 500L
        val syncSwipeSection = addSection("Настройки Действий", hasSwipeChanges) { body ->"""
)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

