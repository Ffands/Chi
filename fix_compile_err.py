import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

content = content.replace("updateLinesOverlay()", "invalidateLines()")
content = content.replace("canvas.drawLine(startX, startY, endX, endY, paint = Paint().apply {", "canvas.drawLine(startX, startY, endX, endY, Paint().apply {")

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
