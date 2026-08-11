import sys

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

content = content.replace("clickDurationMs: Long = 50L", "clickDurationMs: Long = 30L")
content = content.replace('if (clickDurationMs != 50L) obj.put("clickDurationMs", clickDurationMs)', 'if (clickDurationMs != 30L) obj.put("clickDurationMs", clickDurationMs)')
content = content.replace('clickDurationMs = obj.optLong("clickDurationMs", 50L)', 'clickDurationMs = obj.optLong("clickDurationMs", 30L)')

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    ui_content = f.read()
ui_content = ui_content.replace('node.clickDurationMs != 50L', 'node.clickDurationMs != 30L')
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(ui_content)

print("patched models")
