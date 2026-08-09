with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

start_str = "val maxCost = if (searchStr.length <= 3) 0 else if (searchStr.length <= 6) 1 else searchStr.length / 4"
end_str = "if (isRegionSelected) cropped.recycle()"

new_ocr_logic = """val maxCost = if (searchStr.length <= 3) 0 else if (searchStr.length <= 6) 1 else searchStr.length / 4

                    var isMatch = false
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
                                      fuzzyContains(recognizedText.lowercase().replace(Regex("\\\\s+"), ""),
                                                   searchStrOrig.lowercase().replace(Regex("\\\\s+"), ""),
                                                   maxCost)
                        isMatch = ocrMatch
                        debugMsg = "Шаг ${node.id}: [OCR] '$recognizedText'. Ищем: '${node.targetText}'. Совпадение: $isMatch"
                    }
                    
                    if (::uiManager.isInitialized) {
                        handler.post {
                            uiManager.logDebug(debugMsg)
                        }
                    }
                    
                    if (isRegionSelected) cropped.recycle()"""

idx1 = content.find(start_str)
if idx1 != -1:
    idx2 = content.find(end_str, idx1)
    if idx2 != -1:
        content = content[:idx1] + new_ocr_logic.replace("\\\\", "\\") + content[idx2 + len(end_str):]

idx1 = content.find(start_str, idx1 + 100)
if idx1 != -1:
    idx2 = content.find(end_str, idx1)
    if idx2 != -1:
        content = content[:idx1] + new_ocr_logic.replace("\\\\", "\\") + content[idx2 + len(end_str):]

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
