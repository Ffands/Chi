import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """                        if (dx != 0 || dy != 0) {
                            node.x = nx
                            node.y = ny
                            if (node.swipePathPoints.isNotEmpty()) {
                                node.swipePathPoints = node.swipePathPoints.map { Pair(it.first + dx, it.second + dy) }
                            }
                        }
                    }
                    if (Math.abs(event.rawX - initialTouchX) < 10 && Math.abs(event.rawY - initialTouchY) < 10) {"""

good_str = """                        if (dx != 0 || dy != 0) {
                            node.x = nx
                            node.y = ny
                            if (node.swipePathPoints.isNotEmpty()) {
                                node.swipePathPoints = node.swipePathPoints.map { Pair(it.first + dx, it.second + dy) }
                            }
                            service.autoSave()
                        }
                    }
                    if (Math.abs(event.rawX - initialTouchX) < 10 && Math.abs(event.rawY - initialTouchY) < 10) {"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("autoSave on drag patched")
