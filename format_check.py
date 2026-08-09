with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    lines = f.readlines()

indent = 0
for i, line in enumerate(lines):
    open_c = line.count('{')
    close_c = line.count('}')
    indent += (open_c - close_c)

    if indent <= 0 and i > 20:
        print(f"Indent {indent} at line {i+1}: {line.strip()}")
