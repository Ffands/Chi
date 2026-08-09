import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

# Replace variables
vars_old = """    var allowExtremeSpeed = false
    private var currentNodeId: Int? = null
        set(value) {
            field = value
            if (::uiManager.isInitialized) {
                uiManager.updateCurrentNodeHighlight(value ?: -2)
            }
        }"""

vars_new = """    var allowExtremeSpeed = false
    
    data class ExecutionThread(
        val threadId: Int,
        var currentNodeId: Int?,
        var currentCheckCycle: Int = 0,
        var currentRepetition: Int = 0,
        var currentCycle: Int = 0,
        var isWaiting: Boolean = false
    )
    val activeThreads = java.util.concurrent.CopyOnWriteArrayList<ExecutionThread>()
    
    fun updateHighlight() {
        if (::uiManager.isInitialized) {
            uiManager.updateCurrentNodeHighlight(activeThreads.firstOrNull()?.currentNodeId ?: -2)
        }
    }"""

content = content.replace(vars_old, vars_new)

# In isPlaying setter
isplay_old = """        set(value) {
            field = value
            if (!value) {
                currentNodeId = null
            }
        }"""
isplay_new = """        set(value) {
            field = value
            if (!value) {
                activeThreads.clear()
                updateHighlight()
            }
        }"""
content = content.replace(isplay_old, isplay_new)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)

print("Variables replaced")
