with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    text = f.read()

count = 0
for i, c in enumerate(text):
    if c == '{': count += 1
    elif c == '}': count -= 1
print("Brackets count UIManager:", count)
