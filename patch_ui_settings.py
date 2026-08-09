import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

init_block = """    var uiAlpha: Float = 0.9f
    
    fun getEffectiveUiScale(): Float {"""

new_init_block = """    var uiAlpha: Float = 0.9f
    var showEyeBtn = true
    var showLinesBtn = true
    var showHotbarBtn = true
    var showSettingsBtn = true
    
    fun loadUISettings() {
        val prefs = service.getSharedPreferences("AutoClickerUISettings", android.content.Context.MODE_PRIVATE)
        uiScale = prefs.getFloat("uiScale", 1.0f)
        uiAlpha = prefs.getFloat("uiAlpha", 0.9f)
        showEyeBtn = prefs.getBoolean("showEyeBtn", true)
        showLinesBtn = prefs.getBoolean("showLinesBtn", true)
        showHotbarBtn = prefs.getBoolean("showHotbarBtn", true)
        showSettingsBtn = prefs.getBoolean("showSettingsBtn", true)
        isDebugWindowVisible = prefs.getBoolean("isDebugWindowVisible", false)
        isCaffeineEnabled = prefs.getBoolean("isCaffeineEnabled", false)
    }

    fun saveUISettings() {
        val prefs = service.getSharedPreferences("AutoClickerUISettings", android.content.Context.MODE_PRIVATE)
        prefs.edit().apply {
            putFloat("uiScale", uiScale)
            putFloat("uiAlpha", uiAlpha)
            putBoolean("showEyeBtn", showEyeBtn)
            putBoolean("showLinesBtn", showLinesBtn)
            putBoolean("showHotbarBtn", showHotbarBtn)
            putBoolean("showSettingsBtn", showSettingsBtn)
            putBoolean("isDebugWindowVisible", isDebugWindowVisible)
            putBoolean("isCaffeineEnabled", isCaffeineEnabled)
            apply()
        }
    }
    
    init {
        loadUISettings()
    }
    
    fun getEffectiveUiScale(): Float {"""

content = content.replace(init_block, new_init_block)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

print("UI settings save/load logic added.")
