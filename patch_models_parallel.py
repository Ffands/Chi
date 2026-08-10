with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

# 1. Add variable
content = content.replace(
    "var macroProfileName: String? = null,",
    "var macroProfileName: String? = null,\n    var macroRunParallel: Boolean = false,"
)

# 2. Add to toJson
content = content.replace(
    "if (macroProfileName != null) obj.put(\"macroProfileName\", macroProfileName)",
    "if (macroProfileName != null) obj.put(\"macroProfileName\", macroProfileName)\n        if (macroRunParallel) obj.put(\"macroRunParallel\", macroRunParallel)"
)

# 3. Add to fromJson 1
content = content.replace(
    "val tMacro = obj.optString(\"macroProfileName\", null).takeIf { it?.isNotEmpty() == true }",
    "val tMacro = obj.optString(\"macroProfileName\", null).takeIf { it?.isNotEmpty() == true }\n            val mRunPar = obj.optBoolean(\"macroRunParallel\", false)"
)

# 4. Add to fromJson 2
content = content.replace(
    "macroProfileName = tMacro,",
    "macroProfileName = tMacro,\n                macroRunParallel = mRunPar,"
)

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)
print("Models patched for parallel macros")
