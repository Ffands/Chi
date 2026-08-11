import sys

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

bad_str = """    private fun checkConditionForNode(node: TargetNode, callback: (Boolean) -> Unit) {
        if (!nodeHasCondition(node)) {
            callback(true)
            return
        }

        try {
            takeScreenshot(Display.DEFAULT_DISPLAY, mainExecutor, object : TakeScreenshotCallback {
                override fun onSuccess(screenshot: ScreenshotResult) {
                    try {
                        val buffer = screenshot.hardwareBuffer
                        val hwBitmap = Bitmap.wrapHardwareBuffer(buffer, screenshot.colorSpace)
                        if (hwBitmap != null) {
                            val bitmap = hwBitmap.copy(Bitmap.Config.ARGB_8888, false)
                            if (bitmap != null) {
                                checkNodeConditionAsync(node, bitmap) { isMainMatch ->
                                    if (node.linkedConditionNodeId != null) {
                                        val linkedNode = nodes.find { it.id == node.linkedConditionNodeId }
                                        if (linkedNode != null) {
                                            checkNodeConditionAsync(linkedNode, bitmap) { isLinkedMatch ->
                                                val isColorMatch = if (node.linkedConditionOperator == "OR") {
                                                    isMainMatch || isLinkedMatch
                                                } else {
                                                    isMainMatch && isLinkedMatch
                                                }
                                                bitmap.recycle()
                                                hwBitmap.recycle()
                                                buffer.close()
                                                callback(isColorMatch)
                                            }
                                            return@checkNodeConditionAsync
                                        }
                                    }
                                    bitmap.recycle()
                                    hwBitmap.recycle()
                                    buffer.close()
                                    callback(isMainMatch)
                                }
                                return
                            }
                            hwBitmap.recycle()
                        }
                        buffer.close()
                    } catch(e: Exception) {
                        e.printStackTrace()
                    }
                    callback(false)
                }
                override fun onFailure(errorCode: Int) {
                    callback(false)
                }
            })
        } catch(e: Exception) {
            callback(false)
        }
    }"""

good_str = """    private var lastScreenshotTime = 0L
    private var cachedBitmap: Bitmap? = null
    private var isTakingScreenshot = false
    private val screenshotCallbacks = mutableListOf<(Bitmap?) -> Unit>()

    private fun requestScreenshot(callback: (Bitmap?) -> Unit) {
        val now = System.currentTimeMillis()
        if (cachedBitmap != null && now - lastScreenshotTime < 50) {
            callback(cachedBitmap)
            return
        }

        screenshotCallbacks.add(callback)

        if (isTakingScreenshot) return
        isTakingScreenshot = true

        try {
            takeScreenshot(Display.DEFAULT_DISPLAY, mainExecutor, object : TakeScreenshotCallback {
                override fun onSuccess(screenshot: ScreenshotResult) {
                    try {
                        val buffer = screenshot.hardwareBuffer
                        val hwBitmap = Bitmap.wrapHardwareBuffer(buffer, screenshot.colorSpace)
                        if (hwBitmap != null) {
                            val newBitmap = hwBitmap.copy(Bitmap.Config.ARGB_8888, false)
                            hwBitmap.recycle()
                            buffer.close()

                            if (newBitmap != null) {
                                cachedBitmap?.recycle()
                                cachedBitmap = newBitmap
                                lastScreenshotTime = System.currentTimeMillis()

                                val callbacks = screenshotCallbacks.toList()
                                screenshotCallbacks.clear()
                                isTakingScreenshot = false

                                callbacks.forEach { it(cachedBitmap) }
                                return
                            }
                        }
                        buffer.close()
                    } catch(e: Exception) {
                        e.printStackTrace()
                    }
                    failAll()
                }

                override fun onFailure(errorCode: Int) {
                    failAll()
                }

                private fun failAll() {
                    val callbacks = screenshotCallbacks.toList()
                    screenshotCallbacks.clear()
                    isTakingScreenshot = false
                    callbacks.forEach { it(null) }
                }
            })
        } catch(e: Exception) {
            val callbacks = screenshotCallbacks.toList()
            screenshotCallbacks.clear()
            isTakingScreenshot = false
            callbacks.forEach { it(null) }
        }
    }

    private fun checkConditionForNode(node: TargetNode, callback: (Boolean) -> Unit) {
        if (!nodeHasCondition(node)) {
            callback(true)
            return
        }

        requestScreenshot { bitmap ->
            if (bitmap == null) {
                callback(false)
                return@requestScreenshot
            }

            checkNodeConditionAsync(node, bitmap) { isMainMatch ->
                if (node.linkedConditionNodeId != null) {
                    val linkedNode = nodes.find { it.id == node.linkedConditionNodeId }
                    if (linkedNode != null) {
                        checkNodeConditionAsync(linkedNode, bitmap) { isLinkedMatch ->
                            val isColorMatch = if (node.linkedConditionOperator == "OR") {
                                isMainMatch || isLinkedMatch
                            } else {
                                isMainMatch && isLinkedMatch
                            }
                            // Do not recycle bitmap here, it is cached globally
                            callback(isColorMatch)
                        }
                        return@checkNodeConditionAsync
                    }
                }
                // Do not recycle bitmap here, it is cached globally
                callback(isMainMatch)
            }
        }
    }"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("screenshot pool patched")
