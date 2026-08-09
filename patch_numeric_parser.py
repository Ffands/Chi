with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

start_idx = content.find("private fun parseNumericValue(text: String, suffixes: String): Double? {")
end_idx = content.find("fun normalizeCyrillic", start_idx)

new_func = """private fun parseNumericValue(text: String, suffixes: String): Double? {
        val noSpaces = text.replace(Regex("\\\\s+"), "").lowercase()
        val match = Regex("(-?\\\\d+[.,\\\\d]*)([a-zа-я]*)").find(noSpaces)
        if (match == null) return null
        
        var numPart = match.groupValues[1]
        val sufPart = match.groupValues[2]
        
        if (numPart.contains(",") && numPart.contains(".")) {
            numPart = numPart.replace(",", "")
        } else if (numPart.count { it == ',' } == 1 && !numPart.contains(".")) {
            numPart = numPart.replace(",", ".")
        } else {
            numPart = numPart.replace(",", "")
        }
        
        val dotCount = numPart.count { it == '.' }
        if (dotCount > 1) {
            numPart = numPart.replace(".", "")
        }
        
        val value = numPart.toDoubleOrNull() ?: return null
        
        var multiplier = 1.0
        if (sufPart.isNotEmpty() && suffixes.isNotEmpty()) {
            val pairs = suffixes.split(",")
            val suffixMap = mutableMapOf<String, Double>()
            for (p in pairs) {
                val kv = p.split(":")
                if (kv.size == 2) {
                    suffixMap[kv[0].trim().lowercase()] = kv[1].trim().toDoubleOrNull() ?: 1.0
                }
            }
            for ((suf, mult) in suffixMap) {
                if (sufPart.startsWith(suf)) {
                    multiplier = mult
                    break
                }
            }
        }
        
        return value * multiplier
    }

    """

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_func.replace("\\\\", "\\") + content[end_idx:]
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("parseNumericValue patched!")
else:
    print("parseNumericValue not found!")
