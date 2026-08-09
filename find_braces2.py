with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == '{':
            stack.append((i+1, j+1, line.strip()))
        elif char == '}':
            if stack:
                stack.pop()

for b in stack:
    print(f"Line {b[0]}, col {b[1]}: {b[2]}")
