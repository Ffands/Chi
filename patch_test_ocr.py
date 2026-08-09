with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

old_func_start = content.find("fun testTextRecognition(node: TargetNode, bitmap: Bitmap) {")
old_func_end = content.find("private fun checkTextCondition", old_func_start)

if old_func_start != -1 and old_func_end != -1:
    new_func = """fun testTextRecognition(node: TargetNode, bitmap: Bitmap) {
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
                        if (enhanced != cropped && debugBmp == null) enhanced.recycle()
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
                            val finalBmp = debugBmp ?: cropped
                            uiManager.showOcrResultDialog(recognizedText, searchStrOrig, isMatch, finalBmp)
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
    content = content[:old_func_start] + new_func.replace("\\\\", "\\") + content[old_func_end:]
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("testTextRecognition patched!")
else:
    print("Could not find testTextRecognition boundaries")
