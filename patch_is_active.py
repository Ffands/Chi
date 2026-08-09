import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

thread_old = """    data class ExecutionThread(
        val threadId: Int,
        var currentNodeId: Int?,
        var currentCheckCycle: Int = 0,
        var currentRepetition: Int = 0,
        var currentCycle: Int = 0,
        var isWaiting: Boolean = false
    )"""

thread_new = """    data class ExecutionThread(
        val threadId: Int,
        var currentNodeId: Int?,
        var currentCheckCycle: Int = 0,
        var currentRepetition: Int = 0,
        var currentCycle: Int = 0,
        var isWaiting: Boolean = false,
        var isActive: Boolean = true
    )"""

content = content.replace(thread_old, thread_new)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)

print("ExecutionThread isActive patched")
