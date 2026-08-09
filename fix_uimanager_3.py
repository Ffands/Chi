import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Fix the third one (around line 2331)
third_target = """        // --- SAVE BUTTON ---
        } // syncSwipeSection
        val saveBtn = Button(service).apply {"""
third_replacement = """        // --- SAVE BUTTON ---
        val saveBtn = Button(service).apply {"""
content = content.replace(third_target, third_replacement)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

