import sys
with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

func_def = """    private fun scheduleNextExecution(thread: ExecutionThread, delayMs: Long) {
        handler.postDelayed({ executeThread(thread) }, delayMs)
    }
"""
if "private fun scheduleNextExecution" not in content:
    content = content.replace("private fun executeThread(thread: ExecutionThread) {", func_def + "\n    private fun executeThread(thread: ExecutionThread) {")
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("Added scheduleNextExecution")
