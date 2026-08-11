import sys

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

bad_str = """                            val actualDur = Math.max(duration, 50L)
                            val fastDur = if (isSwipe) 100L else 50L
                            
                            val gesture = android.accessibilityservice.GestureDescription.Builder()
                                .addStroke(android.accessibilityservice.GestureDescription.StrokeDescription(path, 0, fastDur))
                                .build()"""

good_str = """                            val gestureDur = Math.max(duration, 50L)
                            
                            val gesture = android.accessibilityservice.GestureDescription.Builder()
                                .addStroke(android.accessibilityservice.GestureDescription.StrokeDescription(path, 0, gestureDur))
                                .build()"""

content = content.replace(bad_str, good_str)

bad_str2 = """                            if (isSwipe) {
                                node.isSwipe = true
                                node.swipeEndX = upX.toInt()
                                node.swipeEndY = upY.toInt()
                                node.swipeDurationMs = actualDur
                                node.swipePathPoints = swipePoints.toList()
                                if (::uiManager.isInitialized) {
                                    uiManager.createSwipeEndMarker(node)
                                }
                            } else {
                                node.clickDurationMs = actualDur
                            }"""

good_str2 = """                            if (isSwipe) {
                                node.isSwipe = true
                                node.swipeEndX = upX.toInt()
                                node.swipeEndY = upY.toInt()
                                node.swipeDurationMs = gestureDur
                                node.swipePathPoints = swipePoints.toList()
                                if (::uiManager.isInitialized) {
                                    uiManager.createSwipeEndMarker(node)
                                }
                            } else {
                                node.clickDurationMs = gestureDur
                            }"""
                            
content = content.replace(bad_str2, good_str2)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Record gesture reverted")
