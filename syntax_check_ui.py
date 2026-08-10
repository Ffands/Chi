import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    text = f.read()

count = 0
for i, c in enumerate(text):
    if c == '{':
        count += 1
    elif c == '}':
        count -= 1
        if count < 0:
            print(f"Error: unmatched }} at index {i}")
            sys.exit(1)

if count != 0:
    print(f"Error: unmatched {{ count={count}")
    sys.exit(1)
print("UI Braces match!")
