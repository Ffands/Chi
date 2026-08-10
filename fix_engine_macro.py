with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

find_exec = """                } else if (node.triggerMode == 2 && node.ocrFullScreenClick) {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: OCR Клик")
                    performGestureForNodes(mutableListOf(node))
                } else {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: Условие сработало")
                }"""

repl_exec = """                } else if (node.triggerMode == 2 && node.ocrFullScreenClick) {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: OCR Клик")
                    performGestureForNodes(mutableListOf(node))
                } else if (node.type == NodeType.MACRO && !node.macroProfileName.isNullOrEmpty()) {
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
                } else {
                    if (::uiManager.isInitialized) uiManager.logDebug("Поток ${thread.threadId} Шаг ${node.id}: Условие сработало")
                }"""

content = content.replace(find_exec, repl_exec)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("AutoClickService patched for MACRO execution")
