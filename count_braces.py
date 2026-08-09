with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    text = f.read()

open_braces = text.count('{')
close_braces = text.count('}')

print(f"Open: {open_braces}, Close: {close_braces}")
