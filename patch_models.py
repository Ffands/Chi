import re

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

# Add new fields to constructor
old_cons = """    var ocrFullScreenClick: Boolean = false,
    var checkResolutionScale: Float = 1.0f) {"""

new_cons = """    var ocrFullScreenClick: Boolean = false,
    var checkResolutionScale: Float = 1.0f,
    var isSmartOcr: Boolean = false,
    var ocrOperator: String = ">=",
    var ocrTargetValue: Double = 0.0,
    var ocrCustomSuffixes: String = "k:1000,m:1000000,b:1000000000,к:1000,м:1000000,б:1000000000") {"""

content = content.replace(old_cons, new_cons)

# Add to toJson()
old_tojson = """        obj.put("checkResolutionScale", checkResolutionScale.toDouble())
        if (swipePathPoints.isNotEmpty()) {"""

new_tojson = """        obj.put("checkResolutionScale", checkResolutionScale.toDouble())
        obj.put("isSmartOcr", isSmartOcr)
        obj.put("ocrOperator", ocrOperator)
        obj.put("ocrTargetValue", ocrTargetValue)
        obj.put("ocrCustomSuffixes", ocrCustomSuffixes)
        if (swipePathPoints.isNotEmpty()) {"""

content = content.replace(old_tojson, new_tojson)

# Add to fromJson()
old_fromjson = """                ocrFullScreenClick = obj.optBoolean("ocrFullScreenClick", false),
                checkResolutionScale = obj.optDouble("checkResolutionScale", 1.0).toFloat()
            )"""

new_fromjson = """                ocrFullScreenClick = obj.optBoolean("ocrFullScreenClick", false),
                checkResolutionScale = obj.optDouble("checkResolutionScale", 1.0).toFloat(),
                isSmartOcr = obj.optBoolean("isSmartOcr", false),
                ocrOperator = obj.optString("ocrOperator", ">="),
                ocrTargetValue = obj.optDouble("ocrTargetValue", 0.0),
                ocrCustomSuffixes = obj.optString("ocrCustomSuffixes", "k:1000,m:1000000,b:1000000000,к:1000,м:1000000,б:1000000000")
            )"""

content = content.replace(old_fromjson, new_fromjson)

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)

print("Models.kt patched")
