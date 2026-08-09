import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

# Replace single currentNodeId with threads
content = content.replace("private var currentNodeId: Int? = null", """
    data class ExecutionThread(
        val id: Int,
        var currentNodeId: Int,
        var currentCheckCycle: Int = 0,
        var currentRepetition: Int = 0,
        var currentCycle: Int = 0,
        var isActive: Boolean = true
    )
    
    private val activeThreads = mutableListOf<ExecutionThread>()
""")

content = content.replace("currentNodeId = null", "activeThreads.clear()")

print("Ready for next step")
