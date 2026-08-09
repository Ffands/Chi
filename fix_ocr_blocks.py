import re
with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

start_idx_test = content.find("fun testTextRecognition(node: TargetNode, bitmap: Bitmap) {")
end_idx_test = content.find("private fun checkTextCondition(node: TargetNode", start_idx_test)

start_idx_check = end_idx_test
end_idx_check = content.find("private fun checkNodeCondition(node: TargetNode", start_idx_check)

test_func = """fun testTextRecognition(node: TargetNode, bitmap: Bitmap) {
        val searchStrOrig = node.targetText?.trim() ?: ""
        if (searchStrOrig.isEmpty()) {
            handler.post { Toast.makeText(this, "Пожалуйста, введите искомый текст", Toast.LENGTH_SHORT).show() }
            return
        }
        
        handler.post { Toast.makeText(this, "Тестирование распознавания...", Toast.LENGTH_SHORT).show() }
        
        try {
            val cropped = bitmap
            val w = cropped.width
            val h = cropped.height
            val isRegionSelected = true
            
            Thread {
                var debugBmp: Bitmap? = null
                try {
                    val recognizedText: String
                    if (w < 5 || h < 5) {
                        recognizedText = ""
                    } else {
                        val enhanced = enhanceBitmapForOcr(cropped)
                        debugBmp = enhanced
                        val analyzer = getHuaweiAnalyzer()
                        val frame = com.huawei.hms.mlsdk.common.MLFrame.fromBitmap(enhanced)
                        val task = analyzer.asyncAnalyseFrame(frame)
                        val result = com.huawei.hmf.tasks.Tasks.await(task)
                        recognizedText = result?.stringValue ?: ""
                        if (enhanced != cropped) enhanced.recycle()
                    }
                    
                    val searchStr = normalizeCyrillic(searchStrOrig).replace(" ", "")
                    val recStrOcr = normalizeCyrillic(recognizedText).replace(" ", "")
                    
                    val maxCost = if (searchStr.length <= 3) 0 else if (searchStr.length <= 6) 1 else searchStr.length / 4

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
                } catch (e: Exception) {
                    e.printStackTrace()
                    handler.post { Toast.makeText(this@AutoClickService, "Ошибка: ${e.message}", Toast.LENGTH_SHORT).show() }
                }
            }.start()
            
        } catch (e: Exception) {
            e.printStackTrace()
            handler.post { Toast.makeText(this, "Ошибка: ${e.message}", Toast.LENGTH_SHORT).show() }
        }
    }

    """

check_func = """private fun checkTextCondition(node: TargetNode, bitmap: Bitmap, callback: (Boolean) -> Unit) {
        try {
            val startX = node.textZoneStartX
            val startY = node.textZoneStartY
            val endX = node.textZoneEndX
            val endY = node.textZoneEndY
            val left = minOf(startX, endX).coerceIn(0, bitmap.width - 1)
            val top = minOf(startY, endY).coerceIn(0, bitmap.height - 1)
            val right = maxOf(startX, endX).coerceIn(0, bitmap.width - 1)
            val bottom = maxOf(startY, endY).coerceIn(0, bitmap.height - 1)
            val w = maxOf(1, right - left)
            val h = maxOf(1, bottom - top)
            
            var isRegionSelected = !(left == 0 && top == 0 && right == 0 && bottom == 0)
            var cropped = if (isRegionSelected) Bitmap.createBitmap(bitmap, left, top, w, h) else bitmap
            
            Thread {
                try {
                    val searchStrOrig = node.targetText!!
                    val recognizedText: String
                    var foundRect: android.graphics.Rect? = null
                    
                    if (w < 5 || h < 5) {
                        recognizedText = ""
                    } else {
                        val enhanced = enhanceBitmapForOcr(cropped)
                        val analyzer = getHuaweiAnalyzer()
                        val frame = com.huawei.hms.mlsdk.common.MLFrame.fromBitmap(enhanced)
                        val task = analyzer.asyncAnalyseFrame(frame)
                        val result = com.huawei.hmf.tasks.Tasks.await(task)
                        recognizedText = result?.stringValue ?: ""
                        
                        if (node.ocrFullScreenClick && result != null) {
                            val searchStr = normalizeCyrillic(searchStrOrig).replace(" ", "").lowercase()
                            val maxCost = if (searchStr.length <= 3) 0 else if (searchStr.length <= 6) 1 else searchStr.length / 4

                            for (block in result.blocks) {
                                for (line in block.contents) {
                                    val blockText = normalizeCyrillic(line.stringValue).replace(" ", "").lowercase()
                                    if (fuzzyContains(blockText, searchStr, maxCost)) {
                                        foundRect = line.border
                                        break
                                    }
                                }
                                if (foundRect != null) break
                            }
                        }
                        if (enhanced != cropped) enhanced.recycle()
                    }
                    
                    val searchStr = normalizeCyrillic(searchStrOrig).replace(" ", "")
                    val recStrOcr = normalizeCyrillic(recognizedText).replace(" ", "")
                    
                    val maxCost = if (searchStr.length <= 3) 0 else if (searchStr.length <= 6) 1 else searchStr.length / 4
                    
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
                    
                    if (isRegionSelected && !cropped.isRecycled) cropped.recycle()
                    
                    if (isMatch && node.ocrFullScreenClick && foundRect != null) {
                        val clickX = left + foundRect.centerX()
                        val clickY = top + foundRect.centerY()
                        performGlobalClick(clickX, clickY, node.clickDurationMs)
                    }
                    
                    val finalResult = if (node.colorOperator == "!=") !isMatch else isMatch
                    handler.post { callback(finalResult) }
                } catch (e: Exception) {
                    if (isRegionSelected && !cropped.isRecycled) cropped.recycle()
                    if (::uiManager.isInitialized) {
                        handler.post { uiManager.logDebug("OCR Ошибка: ${e.message}") }
                    }
                    handler.post { callback(false) }
                }
            }.start()
        } catch (e: Exception) {
            e.printStackTrace()
            handler.post { Toast.makeText(this, "Ошибка: ${e.message}", Toast.LENGTH_SHORT).show() }
            callback(false)
        }
    }

    """

if start_idx_test != -1 and end_idx_test != -1 and end_idx_check != -1:
    content = content[:start_idx_test] + test_func.replace("\\\\", "\\") + check_func.replace("\\\\", "\\") + content[end_idx_check:]
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("Methods patched!")
else:
    print(f"Could not find method boundaries: start={start_idx_test}, mid={start_idx_check}, end={end_idx_check}")
