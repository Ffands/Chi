import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

alpha_minus = "uiAlpha -= 0.1f; applyUISettings(); showSettingsMenu()"
alpha_minus_new = "uiAlpha -= 0.1f; saveUISettings(); applyUISettings(); showSettingsMenu()"
content = content.replace(alpha_minus, alpha_minus_new)

alpha_plus = "uiAlpha += 0.1f; applyUISettings(); showSettingsMenu()"
alpha_plus_new = "uiAlpha += 0.1f; saveUISettings(); applyUISettings(); showSettingsMenu()"
content = content.replace(alpha_plus, alpha_plus_new)

scale_minus = "uiScale -= 0.1f; applyUIScaleChange()"
scale_minus_new = "uiScale -= 0.1f; saveUISettings(); applyUIScaleChange()"
content = content.replace(scale_minus, scale_minus_new)

scale_plus = "uiScale += 0.1f; applyUIScaleChange()"
scale_plus_new = "uiScale += 0.1f; saveUISettings(); applyUIScaleChange()"
content = content.replace(scale_plus, scale_plus_new)

debug_toggle_old = """            setOnClickListener {
                toggleDebugWindow()
                showSettingsMenu()
            }"""
debug_toggle_new = """            setOnClickListener {
                toggleDebugWindow()
                saveUISettings()
                showSettingsMenu()
            }"""
content = content.replace(debug_toggle_old, debug_toggle_new)

caffeine_toggle_old = """            setOnClickListener {
                isCaffeineEnabled = !isCaffeineEnabled
                updateFloatingControlBarCaffeine()
                showSettingsMenu()
            }"""
caffeine_toggle_new = """            setOnClickListener {
                isCaffeineEnabled = !isCaffeineEnabled
                saveUISettings()
                updateFloatingControlBarCaffeine()
                showSettingsMenu()
            }"""
content = content.replace(caffeine_toggle_old, caffeine_toggle_new)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

print("Saved settings for Alpha and Scale")
