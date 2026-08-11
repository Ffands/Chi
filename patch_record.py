import sys

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

bad_str = """                            val gestureDur = Math.max(duration, 50L)
                            
                            val gesture = android.accessibilityservice.GestureDescription.Builder()
                                .addStroke(android.accessibilityservice.GestureDescription.StrokeDescription(path, 0, gestureDur))
                                .build()"""

good_str = """                            val actualDur = Math.max(duration, 50L)
                            val fastDur = if (isSwipe) 100L else 50L
                            
                            val gesture = android.accessibilityservice.GestureDescription.Builder()
                                .addStroke(android.accessibilityservice.GestureDescription.StrokeDescription(path, 0, fastDur))
                                .build()"""

content = content.replace(bad_str, good_str)

bad_str2 = """                            if (isSwipe) {
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

good_str2 = """                            if (isSwipe) {
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
                            
content = content.replace(bad_str2, good_str2)

# Fix postDelayed which is missing its timeout or has a timeout on the next line
import re
content = re.sub(r'recordOverlay\?\.postDelayed\(\{', r'recordOverlay?.post({', content)
content = re.sub(r'\}[\s]*,[\s]*50\)', r'})', content) # if there was a 50 timeout

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)

print("Record gesture patched")
