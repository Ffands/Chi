import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target_play = """            setOnLongClickListener {
                showSettingsBtn = true
                saveUISettings()
                gearBtn.visibility = View.VISIBLE
                showModMenu()
                true
            }"""

replace_play = """            setOnLongClickListener {
                showSettingsBtn = true
                saveUISettings()
                recreateFloatingControlBar()
                showModMenu()
                true
            }"""

content = content.replace(target_play, replace_play)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
