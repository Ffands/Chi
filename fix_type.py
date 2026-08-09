with open('/app/applet/app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

content = content.replace('performGlobalClick(clickX, clickY, node.clickDurationMs)', 'performGlobalClick(clickX.toFloat(), clickY.toFloat(), node.clickDurationMs)')

with open('/app/applet/app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Type fixed!")
