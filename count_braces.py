import sys

def count_braces(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    open_b = content.count('{')
    close_b = content.count('}')
    print(f"{filepath}: {{ = {open_b}, }} = {close_b}")

count_braces('./app/src/main/java/com/example/autoclicker/AutoClickService.kt')
count_braces('./app/src/main/java/com/example/autoclicker/UIManager.kt')
count_braces('./app/src/main/java/com/example/autoclicker/Models.kt')
