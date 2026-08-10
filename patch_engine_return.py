with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

find_exec = """    private fun executeThread(thread: ExecutionThread) {
        if (!isPlaying || !thread.isActive) return

        if (thread.currentNodeId == -1) {
            thread.isActive = false
            if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId}: Достигнут шаг -1")
            checkAllThreadsStopped()
            return
        }

        if (maxPlayDurationMs != null && maxPlayDurationMs!! > 0L) {"""

repl_exec = """    private fun executeThread(thread: ExecutionThread) {
        if (!isPlaying || !thread.isActive) return

        if (thread.currentNodeId == -1) {
            if (thread.returnStack.isNotEmpty()) {
                thread.currentNodeId = thread.returnStack.pop()
                if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId}: Возврат из макроса на шаг ${thread.currentNodeId}")
                scheduleNextExecution(thread, 0L)
                return
            }
            thread.isActive = false
            if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId}: Достигнут шаг -1")
            checkAllThreadsStopped()
            return
        }

        if (maxPlayDurationMs != null && maxPlayDurationMs!! > 0L) {"""

content = content.replace(find_exec, repl_exec)

find_node_null = """        val node = nodes.find { it.id == thread.currentNodeId }
        
        if (node == null) {
            thread.currentNodeId = nodes.firstOrNull { !it.skipSequentialExecution }?.id
            
            if (thread.currentNodeId != null) {"""

repl_node_null = """        val node = nodes.find { it.id == thread.currentNodeId }
        
        if (node == null) {
            if (thread.returnStack.isNotEmpty()) {
                thread.currentNodeId = thread.returnStack.pop()
                if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId}: Возврат из макроса на шаг ${thread.currentNodeId}")
                scheduleNextExecution(thread, 0L)
                return
            }
            
            thread.currentNodeId = nodes.firstOrNull { !it.skipSequentialExecution }?.id
            
            if (thread.currentNodeId != null) {"""

content = content.replace(find_node_null, repl_node_null)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Return stack patched")
