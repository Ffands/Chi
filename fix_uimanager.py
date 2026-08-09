import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Fix the first one (around line 818, which is in main menu profileLayout section)
first_target = """        val profileLayout = LinearLayout(service).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(0, 10, 0, 10)
        }
        } // syncSwipeSection
        val saveBtn = Button(service).apply {"""
first_replacement = """        val profileLayout = LinearLayout(service).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(0, 10, 0, 10)
        }
        val saveBtn = Button(service).apply {"""
content = content.replace(first_target, first_replacement)

# Fix the second one (around line 1208, in settings menu extremeSpeedLayout section)
second_target = """        extremeSpeedLayout.addView(extremeSpeedCheck)
        layout.addView(extremeSpeedLayout)
        } // syncSwipeSection
        val saveBtn = Button(service).apply {"""
second_replacement = """        extremeSpeedLayout.addView(extremeSpeedCheck)
        layout.addView(extremeSpeedLayout)
        val saveBtn = Button(service).apply {"""
content = content.replace(second_target, second_replacement)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

