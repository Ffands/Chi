with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

find_threads = """            var threadIdCounter = 1
            for (n in nodes) {
                if (!n.skipSequentialExecution && !allTargets.contains(n.id)) {
                    activeThreads.add(ExecutionThread(threadIdCounter++, n.id))
                }
            }"""

repl_threads = """            var threadIdCounter = 1
            for (n in nodes) {
                if (!n.skipSequentialExecution) {
                    if (n.isIndependentThread || !allTargets.contains(n.id)) {
                        activeThreads.add(ExecutionThread(threadIdCounter++, n.id))
                    }
                }
            }"""

content = content.replace(find_threads, repl_threads)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("AutoClickService patched for isIndependentThread")
