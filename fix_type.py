import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_arrow_angle = """                                val path = android.graphics.Path().apply {
                                    moveTo(endX, endY)
                                    lineTo(p1x, p1y)
                                    lineTo(p2x, p2y)
                                    close()
                                }"""
repl_arrow_angle = """                                val path = android.graphics.Path().apply {
                                    moveTo(endX, endY)
                                    lineTo(p1x.toFloat(), p1y.toFloat())
                                    lineTo(p2x.toFloat(), p2y.toFloat())
                                    close()
                                }"""

if find_arrow_angle in content:
    content = content.replace(find_arrow_angle, repl_arrow_angle)
    with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
        f.write(content)
    print("Fixed type mismatch")
else:
    print("Could not find type mismatch block")
