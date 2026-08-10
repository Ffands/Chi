import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

content = content.replace('!_AUTOSAVE_!', 'Автосохранение')

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("AutoSave name patched to Автосохранение")
