import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

toggleplay_old = """            isPlaying = true
            currentCycle = 0
            playStartTimeMs = System.currentTimeMillis()
            for (n in nodes) {
                n.currentCheckCycle = 0
                n.currentRepetition = 0
            }
            val startNodeId = nodes.firstOrNull { !it.skipSequentialExecution }?.id
            if (startNodeId == null) {
                isPlaying = false
                return
            }
            currentNodeId = startNodeId
            if (::uiManager.isInitialized) uiManager.logDebug("--- СТАРТ ---")
            uiManager.setNodesTouchable(false)
            executeNext()"""

toggleplay_new = """            isPlaying = true
            currentCycle = 0
            playStartTimeMs = System.currentTimeMillis()
            activeThreads.clear()
            
            // Check if user set multiple start points by looking at all unlinked nodes, or just the first one
            // We can spawn threads for all nodes that are NOT the target of any other node, unless there's a loop.
            // For now, spawn 1 thread at the first enabled node. Users can add more threads in the future.
            // But wait, if they have multiple separate "groups" of nodes, maybe spawn a thread for each?
            // Let's spawn 1 thread for now, and add a setting for multithread starting later.
            val startNodeId = nodes.firstOrNull { !it.skipSequentialExecution }?.id
            if (startNodeId == null) {
                isPlaying = false
                return
            }
            
            // MULTITHREADING: Automatically detect independent entry points (nodes with no incoming connections)
            val allTargets = mutableSetOf<Int>()
            for (n in nodes) {
                n.nextNodeIdOnSuccess?.let { allTargets.add(it) }
                n.nextNodeIdOnFail?.let { allTargets.add(it) }
                if (!n.skipSequentialExecution && n.nextNodeIdOnSuccess == null && n.nextNodeIdOnFail == null) {
                    // Linear sequence target
                    val idx = nodes.indexOf(n)
                    if (idx + 1 < nodes.size) {
                        allTargets.add(nodes[idx + 1].id)
                    }
                }
            }
            
            var threadIdCounter = 1
            for (n in nodes) {
                if (!n.skipSequentialExecution && !allTargets.contains(n.id)) {
                    activeThreads.add(ExecutionThread(threadIdCounter++, n.id))
                }
            }
            
            if (activeThreads.isEmpty()) {
                activeThreads.add(ExecutionThread(threadIdCounter, startNodeId))
            }
            
            updateHighlight()
            if (::uiManager.isInitialized) uiManager.logDebug("--- СТАРТ (${activeThreads.size} поток(ов)) ---")
            uiManager.setNodesTouchable(false)
            
            // Start all threads
            for (thread in activeThreads) {
                executeThread(thread)
            }"""

content = content.replace(toggleplay_old, toggleplay_new)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)

print("togglePlay patched")
