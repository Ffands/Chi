with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

find_macro = """                } else if (node.type == NodeType.MACRO && !node.macroProfileName.isNullOrEmpty()) {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: Запуск макроса ${node.macroProfileName}")
                    val oldMaxId = if (nodes.isNotEmpty()) nodes.maxOf { it.id } else 0
                    val offset = oldMaxId + 1
                    
                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                        loadProfile(node.macroProfileName!!, append = true)
                        
                        // We need to route this thread to the first node of the loaded macro
                        thread.currentRepetition = 0
                        thread.currentNodeId = offset
                        
                        uiManager.recreateFloatingControlBar()
                        // Resume the thread pointing to the macro's start
                        scheduleNextExecution(thread, node.delayAfterMs)
                    }
                    return@checkConditionForNode // Wait for the async load
                } else {"""

repl_macro = """                } else if (node.type == NodeType.MACRO && !node.macroProfileName.isNullOrEmpty()) {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: Запуск макроса ${node.macroProfileName} (Параллельно: ${node.macroRunParallel})")
                    val oldMaxId = if (nodes.isNotEmpty()) nodes.maxOf { it.id } else 0
                    val offset = oldMaxId + 1
                    
                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                        loadProfile(node.macroProfileName!!, append = true)
                        
                        if (node.macroRunParallel) {
                            val newThread = ExecutionThread(
                                threadId = activeThreads.size + 1,
                                currentNodeId = offset
                            )
                            activeThreads.add(newThread)
                            executeThread(newThread)
                            
                            thread.currentRepetition = 0
                            thread.currentNodeId = node.nextNodeIdOnSuccess ?: getNextNodeLinear(node.id)
                            scheduleNextExecution(thread, node.delayAfterMs)
                        } else {
                            val nextId = node.nextNodeIdOnSuccess ?: getNextNodeLinear(node.id)
                            if (nextId != -1) {
                                thread.returnStack.push(nextId)
                            }
                            thread.currentRepetition = 0
                            thread.currentNodeId = offset
                            scheduleNextExecution(thread, node.delayAfterMs)
                        }
                        
                        uiManager.recreateFloatingControlBar()
                    }
                    return@checkConditionForNode // Wait for the async load
                } else {"""

content = content.replace(find_macro, repl_macro)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Macro Trigger patched")
