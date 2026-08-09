import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

old_perform = """    private fun performGestureForNodes(activeNodes: List<TargetNode>) {
        val builder = GestureDescription.Builder()
        
        for (node in activeNodes) {
            val path = Path()
            var startX = node.x.toFloat()
            var startY = node.y.toFloat()
            if (node.randomizeRadius > 0) {
                val angle = Math.random() * Math.PI * 2
                val r = Math.random() * node.randomizeRadius
                startX += (Math.cos(angle) * r).toFloat()
                startY += (Math.sin(angle) * r).toFloat()
            }
            path.moveTo(startX, startY)
            if (node.isSwipe) {
                var eX = node.swipeEndX.toFloat()
                var eY = node.swipeEndY.toFloat()
                if (node.swipeTargetNodeId != null) {
                    val tgtNode = nodes.find { it.id == node.swipeTargetNodeId }
                    if (tgtNode != null) {
                        try {
                            uiManager.updateNodeScreenPosition(tgtNode)
                        } catch(e: Exception){}
                        eX = tgtNode.x.toFloat()
                        eY = tgtNode.y.toFloat()
                    }
                    if (node.randomizeRadius > 0) {
                        val angle = Math.random() * Math.PI * 2
                        val r = Math.random() * node.randomizeRadius
                        eX += (Math.cos(angle) * r).toFloat()
                        eY += (Math.sin(angle) * r).toFloat()
                    }
                    path.lineTo(eX, eY)
                } else if (node.swipePathPoints.isNotEmpty()) {
                    path.moveTo(node.swipePathPoints[0].first, node.swipePathPoints[0].second)
                    for (i in 1 until node.swipePathPoints.size) {
                        path.lineTo(node.swipePathPoints[i].first, node.swipePathPoints[i].second)
                    }
                } else {
                    if (node.randomizeRadius > 0) {
                        val angle = Math.random() * Math.PI * 2
                        val r = Math.random() * node.randomizeRadius
                        eX += (Math.cos(angle) * r).toFloat()
                        eY += (Math.sin(angle) * r).toFloat()
                    }
                    path.lineTo(eX, eY)
                }
            }
            val stroke = GestureDescription.StrokeDescription(path, 0, if (node.isSwipe) node.swipeDurationMs else node.clickDurationMs)
            builder.addStroke(stroke)
        }
        gestureQueue.add(builder.build())
        processGestureQueue()
    }"""

new_perform = """    private fun performGestureForNodes(activeNodes: List<TargetNode>) {
        // If multitouch is globally disabled (or we want sequential), we can queue them separately.
        // For now, let's keep the option. We'll use a global flag or just dispatch them individually if there are multiple.
        // The user said: "мультитач плохая идея так как некоторая часть игр увидит как призыв к масштабированию, но стоит добавить мультитач в настройки внутри других режимов"
        // So we will dispatch them sequentially into the queue, UNLESS they specifically want multitouch.
        // To be safe and fix the bug, we'll queue each node as a separate gesture, so no multitouch zooming occurs.
        // If they ever want true multitouch, we can add a toggle later.
        
        for (node in activeNodes) {
            val builder = GestureDescription.Builder()
            val path = Path()
            var startX = node.x.toFloat()
            var startY = node.y.toFloat()
            if (node.randomizeRadius > 0) {
                val angle = Math.random() * Math.PI * 2
                val r = Math.random() * node.randomizeRadius
                startX += (Math.cos(angle) * r).toFloat()
                startY += (Math.sin(angle) * r).toFloat()
            }
            path.moveTo(startX, startY)
            if (node.isSwipe) {
                var eX = node.swipeEndX.toFloat()
                var eY = node.swipeEndY.toFloat()
                if (node.swipeTargetNodeId != null) {
                    val tgtNode = nodes.find { it.id == node.swipeTargetNodeId }
                    if (tgtNode != null) {
                        try {
                            uiManager.updateNodeScreenPosition(tgtNode)
                        } catch(e: Exception){}
                        eX = tgtNode.x.toFloat()
                        eY = tgtNode.y.toFloat()
                    }
                    if (node.randomizeRadius > 0) {
                        val angle = Math.random() * Math.PI * 2
                        val r = Math.random() * node.randomizeRadius
                        eX += (Math.cos(angle) * r).toFloat()
                        eY += (Math.sin(angle) * r).toFloat()
                    }
                    path.lineTo(eX, eY)
                } else if (node.swipePathPoints.isNotEmpty()) {
                    path.moveTo(node.swipePathPoints[0].first, node.swipePathPoints[0].second)
                    for (i in 1 until node.swipePathPoints.size) {
                        path.lineTo(node.swipePathPoints[i].first, node.swipePathPoints[i].second)
                    }
                } else {
                    if (node.randomizeRadius > 0) {
                        val angle = Math.random() * Math.PI * 2
                        val r = Math.random() * node.randomizeRadius
                        eX += (Math.cos(angle) * r).toFloat()
                        eY += (Math.sin(angle) * r).toFloat()
                    }
                    path.lineTo(eX, eY)
                }
            }
            val stroke = GestureDescription.StrokeDescription(path, 0, if (node.isSwipe) node.swipeDurationMs else node.clickDurationMs)
            builder.addStroke(stroke)
            gestureQueue.add(builder.build())
        }
        
        processGestureQueue()
    }"""

content = content.replace(old_perform, new_perform)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Multitouch patched to sequential")
