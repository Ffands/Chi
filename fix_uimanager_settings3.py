import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target = """    var uiScale: Float = 1.0f
    var uiAlpha: Float = 0.9f
    fun getEffectiveUiScale(): Float {"""

replacement = """    var uiScale: Float = 1.0f
    var uiAlpha: Float = 0.9f

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
        isMenuFullscreen = prefs.getBoolean("isMenuFullscreen", false)
        service.enableMultitouch = prefs.getBoolean("enableMultitouch", false)
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
            putBoolean("isMenuFullscreen", isMenuFullscreen)
            putBoolean("enableMultitouch", service.enableMultitouch)
            apply()
        }
    }

    init {
        loadUISettings()
    }

    fun getEffectiveUiScale(): Float {"""

# Replace using string replace without assuming exact spaces
content = re.sub(r'    var uiScale: Float = 1\.0f\s+var uiAlpha: Float = 0\.9f\s+fun getEffectiveUiScale\(\): Float \{', replacement, content)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
