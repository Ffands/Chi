with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

content = content.replace("enum class NodeType { CLICK, CHECK_COLOR }", "enum class NodeType { CLICK, CHECK_COLOR, MACRO }")
content = content.replace("var targetColor: Int? = null,", "var targetColor: Int? = null,\n    var macroProfileName: String? = null,")

tojson_find = """        if (targetColor != null) obj.put("targetColor", targetColor)"""
tojson_repl = """        if (targetColor != null) obj.put("targetColor", targetColor)\n        if (macroProfileName != null) obj.put("macroProfileName", macroProfileName)"""
content = content.replace(tojson_find, tojson_repl)

fromjson_find = """val tColor = if (obj.has("targetColor")) obj.getInt("targetColor") else null"""
fromjson_repl = """val tColor = if (obj.has("targetColor")) obj.getInt("targetColor") else null\n            val tMacro = obj.optString("macroProfileName", null).takeIf { it?.isNotEmpty() == true }"""
content = content.replace(fromjson_find, fromjson_repl)

fromjson2_find = """targetColor = tColor,"""
fromjson2_repl = """targetColor = tColor,\n                macroProfileName = tMacro,"""
content = content.replace(fromjson2_find, fromjson2_repl)

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)
print("Models patched")
