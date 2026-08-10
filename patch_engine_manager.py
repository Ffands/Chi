import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

find_macro = """                } else if (node.type == NodeType.MACRO && !node.macroProfileName.isNullOrEmpty()) {"""
repl_macro = """                } else if (node.type == NodeType.MANAGER) {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: Менеджер...")
                    evaluateManagerRoutes(node.managerRoutes, 0, thread, node)
                    return@checkConditionForNode
                } else if (node.type == NodeType.MACRO && !node.macroProfileName.isNullOrEmpty()) {"""
content = content.replace(find_macro, repl_macro)

new_method = """    private fun evaluateManagerRoutes(routes: List<ManagerRoute>, index: Int, thread: ExecutionThread, managerNode: TargetNode) {
        if (!isPlaying || !thread.isActive) return
        if (index >= routes.size) {
            thread.currentRepetition = 0
            thread.currentNodeId = managerNode.nextNodeIdOnFail ?: getNextNodeLinear(managerNode.id)
            if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${managerNode.id}: Менеджер -> ${thread.currentNodeId} (По умолчанию)")
            scheduleNextExecution(thread, managerNode.delayAfterMs)
            return
        }
        
        val route = routes[index]
        val nodeToCheck = nodes.find { it.id == route.checkNodeId }
        if (nodeToCheck == null || !nodeHasCondition(nodeToCheck)) {
            evaluateManagerRoutes(routes, index + 1, thread, managerNode)
            return
        }
        
        checkConditionForNode(nodeToCheck) { isMatch ->
            if (!isPlaying || !thread.isActive) return@checkConditionForNode
            if (isMatch) {
                thread.currentRepetition = 0
                thread.currentNodeId = route.onSuccessGoToId
                if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${managerNode.id}: Менеджер совпало ${route.checkNodeId} -> ${thread.currentNodeId}")
                scheduleNextExecution(thread, managerNode.delayAfterMs)
            } else {
                evaluateManagerRoutes(routes, index + 1, thread, managerNode)
            }
        }
    }
"""

# Insert new_method before fun executeThread(
content = content.replace("    private fun executeThread(", new_method + "\n    private fun executeThread(")

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Engine manager logic patched")
