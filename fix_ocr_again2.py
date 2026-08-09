with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

helper_func = """    private fun parseNumericValue(text: String, suffixes: String): Double? {
        val cleanText = text.replace(Regex("[^0-9.,a-zA-Zа-яА-Я]"), "").replace(",", ".").lowercase()
        if (cleanText.isEmpty()) return null
        
        var multiplier = 1.0
        var numStr = cleanText
        
        val suffixMap = mutableMapOf<String, Double>()
        if (suffixes.isNotEmpty()) {
            val pairs = suffixes.split(",")
            for (p in pairs) {
                val kv = p.split(":")
                if (kv.size == 2) {
                    suffixMap[kv[0].trim().lowercase()] = kv[1].trim().toDoubleOrNull() ?: 1.0
                }
            }
        }
        
        for ((suf, mult) in suffixMap) {
            if (cleanText.endsWith(suf)) {
                multiplier = mult
                numStr = cleanText.substring(0, cleanText.length - suf.length)
                break
            } else if (cleanText.startsWith(suf)) {
                multiplier = mult
                numStr = cleanText.substring(suf.length)
                break
            }
        }
        
        val value = numStr.toDoubleOrNull()
        return if (value != null) value * multiplier else null
    }"""

if "parseNumericValue" not in content:
    content = content.replace("fun normalizeCyrillic", helper_func + "\n\n    fun normalizeCyrillic")


new_ocr_match = """                    var isMatch = false
                    var debugMsg = ""
                    
                    if (node.isSmartOcr) {
                        val parsedVal = parseNumericValue(recognizedText, node.ocrCustomSuffixes)
                        if (parsedVal != null) {
                            isMatch = when (node.ocrOperator) {
                                ">" -> parsedVal > node.ocrTargetValue
                                "<" -> parsedVal < node.ocrTargetValue
                                ">=" -> parsedVal >= node.ocrTargetValue
                                "<=" -> parsedVal <= node.ocrTargetValue
                                "==" -> parsedVal == node.ocrTargetValue
                                "!=" -> parsedVal != node.ocrTargetValue
                                else -> false
                            }
                            debugMsg = "Шаг ${node.id}: [Смарт OCR] Текст='$recognizedText', Число=$parsedVal. Условие: $parsedVal ${node.ocrOperator} ${node.ocrTargetValue} -> $isMatch"
                        } else {
                            debugMsg = "Шаг ${node.id}: [Смарт OCR] Текст='$recognizedText'. Не удалось распознать число."
                        }
                    } else {
                        val ocrMatch = fuzzyContains(recStrOcr, searchStr, maxCost) ||
                                      fuzzyContains(recognizedText.lowercase().replace(Regex("\\s+"), ""),
                                                   searchStrOrig.lowercase().replace(Regex("\\s+"), ""),
                                                   maxCost)
                        isMatch = ocrMatch
                        debugMsg = "Шаг ${node.id}: [OCR] '$recognizedText'. Ищем: '${node.targetText}'. Совпадение: $isMatch"
                    }
                    
                    if (::uiManager.isInitialized) {
                        handler.post {
                            uiManager.logDebug(debugMsg)
                        }
                    }"""

start_str = "val ocrMatch = fuzzyContains(recStrOcr, searchStr, maxCost) ||"
end_str = "if (isRegionSelected) cropped.recycle()"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_ocr_match + "\n                    \n                    " + content[end_idx:]

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
