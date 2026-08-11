import sys
with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

bad_toast = 'android.widget.Toast.makeText(this, "Запись! Выполняйте действия на экране.", android.widget.Toast.LENGTH_SHORT).show()'
good_toast = 'android.widget.Toast.makeText(this, "Запись! Жесты воспроизводятся после отпускания пальца (ограничение Android).", android.widget.Toast.LENGTH_LONG).show()'

content = content.replace(bad_toast, good_toast)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Patched record toast")
