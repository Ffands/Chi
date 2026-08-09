import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

# I will find the exact bounds of executeNext() and replace it.
# We will use regex to find `private fun executeNext() {` up to `private fun getNextNodeLinear`.

match = re.search(r'private fun executeNext\(\).*?private fun getNextNodeLinear', content, re.DOTALL)
if match:
    old_code = match.group(0)
    
    new_code = """private fun executeThread(thread: ExecutionThread) {
        if (!isPlaying || !thread.isActive) return

        if (thread.currentNodeId == -1) {
            thread.isActive = false
            if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId}: Достигнут шаг -1")
            checkAllThreadsStopped()
            return
        }

        if (maxPlayDurationMs != null && maxPlayDurationMs!! > 0L) {
            val elapsed = System.currentTimeMillis() - playStartTimeMs
            if (elapsed >= maxPlayDurationMs!!) {
                isPlaying = false
                if (::uiManager.isInitialized) uiManager.logDebug("СТОП: Лимит времени истек")
                uiManager.setNodesTouchable(true)
                uiManager.updateMenu()
                return
            }
        }

        val node = nodes.find { it.id == thread.currentNodeId }
        
        if (node == null) {
            thread.currentNodeId = nodes.firstOrNull { !it.skipSequentialExecution }?.id
            
            if (thread.currentNodeId != null) {
                thread.currentCycle++
                if (maxCycles != null && maxCycles!! > 0 && thread.currentCycle >= maxCycles!!) {
                    thread.isActive = false
                    checkAllThreadsStopped()
                    return
                }
                thread.currentRepetition = 0
                if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId}: Конец цикла. Запуск ${thread.currentCycle}...")
                handler.postDelayed({ executeThread(thread) }, 100L)
            } else {
                thread.isActive = false
                checkAllThreadsStopped()
            }
            return
        }

        if (activeThreads.firstOrNull()?.threadId == thread.threadId) {
            uiManager.updateNodeScreenPosition(node)
        }

        checkConditionForNode(node) { isMatch ->
            if (!isPlaying || !thread.isActive) return@checkConditionForNode
            
            if (isMatch) {
                thread.currentCheckCycle = 0
                if (node.type == NodeType.CLICK) {
                    val activeNodes = mutableListOf(node)
                    if (node.syncWithNodeIds.isNotEmpty()) {
                        val idsStr = node.syncWithNodeIds.split(",")
                        for (idStr in idsStr) {
                            val id = idStr.trim().toIntOrNull()
                            if (id != null) {
                                val syncNode = nodes.find { it.id == id }
                                if (syncNode != null && syncNode.type == NodeType.CLICK) {
                                    activeNodes.add(syncNode)
                                }
                            }
                        }
                    }
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: ${if (node.isSwipe) "Свайп" else "Клик"}")
                    performGestureForNodes(activeNodes)
                } else if (node.triggerMode == 2 && node.ocrFullScreenClick) {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: OCR Клик")
                    performGestureForNodes(mutableListOf(node))
                } else {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: Условие сработало")
                }
                
                thread.currentRepetition++
                if (thread.currentRepetition < node.repetitions) {
                    thread.currentNodeId = node.id
                } else {
                    thread.currentRepetition = 0
                    thread.currentNodeId = node.nextNodeIdOnSuccess ?: getNextNodeLinear(node.id)
                }
            } else {
                if (node.maxCheckCycles != null && node.maxCheckCycles!! > 0) {
                    thread.currentCheckCycle++
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: Ждем (${thread.currentCheckCycle}/${node.maxCheckCycles})")
                    if (thread.currentCheckCycle >= node.maxCheckCycles!!) {
                        thread.currentCheckCycle = 0
                        thread.currentRepetition = 0
                        thread.currentNodeId = node.nextNodeIdOnFail ?: getNextNodeLinear(node.id)
                    } else {
                        thread.currentNodeId = node.id
                    }
                } else {
                    thread.currentRepetition = 0
                    thread.currentNodeId = node.nextNodeIdOnFail ?: node.id
                }
            }

            updateHighlight()

            val randomDelay = if (node.randomizeDelayMs > 0) (0..node.randomizeDelayMs).random() else 0L
            val minDelay = if (allowExtremeSpeed) 0L else 10L
            
            val finalDelay = if (!isMatch && thread.currentNodeId == node.id) {
                val pollDelay = if (node.triggerMode == 2) 300L else 150L
                Math.max(pollDelay, minDelay)
            } else {
                Math.max(minDelay, node.delayAfterMs + randomDelay)
            }

            handler.postDelayed({ executeThread(thread) }, finalDelay)
        }
    }

    private fun checkAllThreadsStopped() {
        if (activeThreads.all { !it.isActive }) {
            isPlaying = false
            uiManager.setNodesTouchable(true)
            uiManager.updateMenu()
        }
    }

    private fun getNextNodeLinear"""
    
    content = content.replace(old_code, new_code)
    
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("executeNext replaced with executeThread")
else:
    print("Could not find executeNext")

