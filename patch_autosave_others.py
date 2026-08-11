import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# setupTextZoneTouchListener
bad_text = """                    invalidateLines()
                    true
                }
                else -> false"""

good_text = """                    invalidateLines()
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (isStart) {
                        node.textZoneStartX = params.x + dpToPx(15)
                        node.textZoneStartY = params.y + dpToPx(15)
                    } else {
                        node.textZoneEndX = params.x + dpToPx(15)
                        node.textZoneEndY = params.y + dpToPx(15)
                    }
                    invalidateLines()
                    service.autoSave()
                    true
                }
                else -> false"""

content = content.replace(bad_text, good_text, 1)

# setupColorCompareTouchListener
bad_color = """                MotionEvent.ACTION_UP -> {
                    val newEx = params.x + dpToPx(20)
                    val newEy = params.y + dpToPx(20)
                    node.colorCompareX = newEx
                    node.colorCompareY = newEy
                    invalidateLines()
                    true
                }"""

good_color = """                MotionEvent.ACTION_UP -> {
                    val newEx = params.x + dpToPx(20)
                    val newEy = params.y + dpToPx(20)
                    node.colorCompareX = newEx
                    node.colorCompareY = newEy
                    invalidateLines()
                    service.autoSave()
                    true
                }"""

content = content.replace(bad_color, good_color, 1)

# setupSwipeEndTouchListener
bad_swipe = """                MotionEvent.ACTION_UP -> {
                    val newEx = params.x + dpToPx(30)
                    val newEy = params.y + dpToPx(30)
                    if (newEx != node.swipeEndX || newEy != node.swipeEndY) {
                        node.swipePathPoints = emptyList()
                        node.swipeEndX = newEx
                        node.swipeEndY = newEy
                    }
                    invalidateLines()
                    true
                }"""

good_swipe = """                MotionEvent.ACTION_UP -> {
                    val newEx = params.x + dpToPx(30)
                    val newEy = params.y + dpToPx(30)
                    if (newEx != node.swipeEndX || newEy != node.swipeEndY) {
                        node.swipePathPoints = emptyList()
                        node.swipeEndX = newEx
                        node.swipeEndY = newEy
                    }
                    invalidateLines()
                    service.autoSave()
                    true
                }"""

content = content.replace(bad_swipe, good_swipe, 1)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("other autoSaves patched")
