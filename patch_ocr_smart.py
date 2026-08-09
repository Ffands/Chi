import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

# 1. Add parseNumericValue method to AutoClickService
helper_func = """
    private fun parseNumericValue(text: String, suffixes: String): Double? {
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
    }
"""

if "parseNumericValue" not in content:
    content = content.replace("fun normalizeCyrillic", helper_func + "\n    fun normalizeCyrillic")

# 2. Modify the OCR match logic
old_ocr_match = """                    val ocrMatch = fuzzyContains(recStrOcr, searchStr, maxCost) ||
                                  fuzzyContains(recognizedText.lowercase().replace(Regex("\\s+"), ""),
                                               searchStrOrig.lowercase().replace(Regex("\\s+"), ""),
                                               maxCost)
                    
                    val isMatch = ocrMatch
                    
                    if (::uiManager.isInitialized) {
                        handler.post {
                            uiManager.logDebug("Шаг ${node.id}: [OCR] '$recognizedText'. Ищем: '${node.targetText}'. Совпадение: $ocrMatch -> $isMatch")
                        }
                    }"""

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

content = content.replace(old_ocr_match, new_ocr_match)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)

print("Smart OCR patched")
