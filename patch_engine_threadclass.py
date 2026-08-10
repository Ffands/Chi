with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

find_thread = """    data class ExecutionThread(
        val threadId: Int,
        var currentNodeId: Int?,
        var currentCheckCycle: Int = 0,
        var currentRepetition: Int = 0,
        var currentCycle: Int = 0,
        var isWaiting: Boolean = false,
        var isActive: Boolean = true
    )"""

repl_thread = """    data class ExecutionThread(
        val threadId: Int,
        var currentNodeId: Int?,
        var currentCheckCycle: Int = 0,
        var currentRepetition: Int = 0,
        var currentCycle: Int = 0,
        var isWaiting: Boolean = false,
        var isActive: Boolean = true
    ) {
        val returnStack = java.util.Stack<Int>()
    }"""

if find_thread in content:
    content = content.replace(find_thread, repl_thread)
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("ExecutionThread patched")
else:
    print("ExecutionThread not found!")
