import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

func_add = """    fun updateAppMode(modeStr: String) {
        if (::uiManager.isInitialized) {
            uiManager.appMode = try {
                AppMode.valueOf(modeStr)
            } catch (e: Exception) {
                AppMode.ADVANCED
            }
            uiManager.updateMenu()
        }
    }"""
    
content = content.replace("    fun toggleRecording() {", func_add + "\n\n    fun toggleRecording() {")

# Also on start:
start_find = """            uiManager = UIManager(this)"""
start_repl = """            uiManager = UIManager(this)
            
            val prefs = getSharedPreferences("AutoClickerSettings", android.content.Context.MODE_PRIVATE)
            val currentMode = prefs.getString("AppMode", "ADVANCED")
            updateAppMode(currentMode!!)
"""
content = content.replace(start_find, start_repl)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("AutoClickService patched for Mode Selection")
