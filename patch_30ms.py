import sys

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

content = content.replace("val minDelay = if (allowExtremeSpeed) 0L else 10L", "val minDelay = if (allowExtremeSpeed) 0L else 30L")
content = content.replace("val gestureDur = Math.max(duration, 50L)", "val gestureDur = Math.max(duration, 30L)")

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("30ms limit patched")
