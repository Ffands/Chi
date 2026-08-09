import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target_longclick = """            setOnLongClickListener {
                showSettingsBtn = true
                saveUISettings()
                recreateFloatingControlBar()
                showModMenu()
                true
            }"""

content = content.replace(target_longclick, "")

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
