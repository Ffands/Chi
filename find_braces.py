with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == '{':
            stack.append((i+1, j+1))
        elif char == '}':
            if stack:
                stack.pop()
            else:
                print(f"Extra closing brace at line {i+1}, col {j+1}")
                exit(1)

if stack:
    print("Unclosed braces:")
    for b in stack:
        print(f"Line {b[0]}, col {b[1]}")
