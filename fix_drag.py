import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target = """        setupDragListener(container, params) { px, py ->
            node.colorCompareX = px + dpToPx(20)
            node.colorCompareY = py + dpToPx(20)
            invalidateLines()
        }"""

replacement = """        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f
        container.setOnTouchListener { _, event ->
            when (event.action) {
                android.view.MotionEvent.ACTION_DOWN -> {
                    initialX = params.x
                    initialY = params.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    true
                }
                android.view.MotionEvent.ACTION_MOVE -> {
                    params.x = initialX + (event.rawX - initialTouchX).toInt()
                    params.y = initialY + (event.rawY - initialTouchY).toInt()
                    windowManager.updateViewLayout(container, params)
                    node.colorCompareX = params.x + dpToPx(20)
                    node.colorCompareY = params.y + dpToPx(20)
                    invalidateLines()
                    true
                }
                else -> false
            }
        }"""
content = content.replace(target, replacement)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
