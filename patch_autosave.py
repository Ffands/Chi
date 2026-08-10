import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

autosave_code = """    fun autoSave() {
        val prefs = getSharedPreferences("AutoClickerProfiles", android.content.Context.MODE_PRIVATE)
        val obj = org.json.JSONObject()
        val metrics = resources.displayMetrics
        obj.put("screenWidth", metrics.widthPixels)
        obj.put("screenHeight", metrics.heightPixels)
        val arr = org.json.JSONArray()
        for (node in nodes) {
            arr.put(node.toJson())
        }
        obj.put("nodes", arr)
        prefs.edit().putString("!_AUTOSAVE_!", obj.toString()).apply()
    }

    fun saveProfile(name: String) {"""

content = content.replace("    fun saveProfile(name: String) {", autosave_code)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    ui = f.read()

# Call service.autoSave() after closing the node editor
ui = re.sub(
    r'(menuParams = android\.view\.WindowManager\.LayoutParams.*?windowManager\.updateViewLayout\(menuView, menuParams\)\n\s*})',
    r'\1\n            service.autoSave()',
    ui,
    flags=re.DOTALL
)

ui = ui.replace(
    "service.nodes.add(node)",
    "service.nodes.add(node)\n        service.autoSave()"
)
ui = ui.replace(
    "service.nodes.remove(node)",
    "service.nodes.remove(node)\n            service.autoSave()"
)

# Call autosave on profile load finish (so the autosave is refreshed)
ui = ui.replace(
    "service.loadProfile(selected)",
    "service.loadProfile(selected)\n                    service.autoSave()"
)

# Call autosave in showMenu -> import
ui = ui.replace(
    "service.loadProfileFromJson(clipText)",
    "service.loadProfileFromJson(clipText)\n                        service.autoSave()"
)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(ui)
print("AutoSave patched")
