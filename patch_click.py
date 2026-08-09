with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

new_func = """
    private fun performGlobalClick(x: Float, y: Float, duration: Long) {
        val path = android.graphics.Path().apply { moveTo(x, y) }
        val stroke = android.accessibilityservice.GestureDescription.StrokeDescription(path, 0, duration)
        val gesture = android.accessibilityservice.GestureDescription.Builder().addStroke(stroke).build()
        gestureQueue.offer(gesture)
        processGestureQueue()
    }
"""

if "private fun performGlobalClick" not in content:
    idx = content.rfind("}")
    content = content[:idx] + new_func + content[idx:]
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("performGlobalClick added!")
else:
    print("performGlobalClick already exists")
