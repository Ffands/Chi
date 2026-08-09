import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

old_func = """    fun updateHighlight() {
        if (::uiManager.isInitialized) {
            uiManager.updateCurrentNodeHighlight(activeThreads.firstOrNull()?.currentNodeId ?: -2)
        }
    }"""

new_func = """    fun updateHighlight() {
        if (::uiManager.isInitialized) {
            val activeIds = activeThreads.mapNotNull { it.currentNodeId }
            uiManager.updateCurrentNodeHighlight(activeIds)
        }
    }"""

content = content.replace(old_func, new_func)

# Also update the fallback in isPlaying setter where we did `updateHighlight()` - wait, `updateHighlight()` takes no arguments, so it will just use activeThreads (which is empty), so it passes empty list! Perfect.

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("AutoClickService patched for highlight")
