with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    text = f.read()

text = text.replace('Regex("\\s+")', 'Regex("\\\\s+")')
text = text.replace('Regex("(-?\\d+[.,\\d]*)([a-zа-я]*)")', 'Regex("(-?\\\\d+[.,\\\\d]*)([a-zа-я]*)")')

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(text)
print("Regex fixed")
