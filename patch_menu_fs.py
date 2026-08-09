import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

load_old = """        isDebugWindowVisible = prefs.getBoolean("isDebugWindowVisible", false)
        isCaffeineEnabled = prefs.getBoolean("isCaffeineEnabled", false)
    }"""
load_new = """        isDebugWindowVisible = prefs.getBoolean("isDebugWindowVisible", false)
        isCaffeineEnabled = prefs.getBoolean("isCaffeineEnabled", false)
        isMenuFullscreen = prefs.getBoolean("isMenuFullscreen", false)
    }"""
content = content.replace(load_old, load_new)

save_old = """            putBoolean("isDebugWindowVisible", isDebugWindowVisible)
            putBoolean("isCaffeineEnabled", isCaffeineEnabled)
            apply()
        }"""
save_new = """            putBoolean("isDebugWindowVisible", isDebugWindowVisible)
            putBoolean("isCaffeineEnabled", isCaffeineEnabled)
            putBoolean("isMenuFullscreen", isMenuFullscreen)
            apply()
        }"""
content = content.replace(save_old, save_new)

toggle_old = """        isMenuFullscreen = !isMenuFullscreen"""
toggle_new = """        isMenuFullscreen = !isMenuFullscreen
        saveUISettings()"""
content = content.replace(toggle_old, toggle_new)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("isMenuFullscreen saved to preferences")
