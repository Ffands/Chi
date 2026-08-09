import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

old_ocr_block = """        val ocrFullscreenCheck = android.widget.CheckBox(service).apply {
            text = "Нажимать на найденный текст (центр метки сдвинется)"
            setTextColor(Color.parseColor("#FFCC00"))
            isChecked = node.ocrFullScreenClick
            setOnCheckedChangeListener { _, isChecked ->
                node.ocrFullScreenClick = isChecked
            }
        }
        ocrFullscreenLayout.addView(ocrFullscreenCheck)"""

new_ocr_block = """        val ocrFullscreenCheck = android.widget.CheckBox(service).apply {
            text = "Нажимать на найденный текст (центр метки сдвинется)"
            setTextColor(Color.parseColor("#FFCC00"))
            isChecked = node.ocrFullScreenClick
            setOnCheckedChangeListener { _, isChecked ->
                node.ocrFullScreenClick = isChecked
            }
        }
        ocrFullscreenLayout.addView(ocrFullscreenCheck)
        
        // Smart OCR Math Options
        val smartOcrLayout = LinearLayout(service).apply { orientation = LinearLayout.VERTICAL; setPadding(0, dpToPx(10), 0, dpToPx(5)) }
        val smartOcrCheck = android.widget.CheckBox(service).apply {
            text = "Умный OCR: Математическое сравнение"
            setTextColor(Color.parseColor("#4CAF50"))
            isChecked = node.isSmartOcr
        }
        smartOcrLayout.addView(smartOcrCheck)
        
        val smartOcrSettings = LinearLayout(service).apply { orientation = LinearLayout.VERTICAL; visibility = if (node.isSmartOcr) View.VISIBLE else View.GONE }
        
        val smartOcrOpLayout = LinearLayout(service).apply { orientation = LinearLayout.HORIZONTAL }
        smartOcrOpLayout.addView(TextView(service).apply { text = "Оператор:"; setTextColor(Color.WHITE); layoutParams = LinearLayout.LayoutParams(0, WindowManager.LayoutParams.WRAP_CONTENT, 0.4f) })
        val smartOcrOpSpinner = android.widget.Spinner(service).apply {
            layoutParams = LinearLayout.LayoutParams(0, WindowManager.LayoutParams.WRAP_CONTENT, 0.6f)
            setBackgroundColor(Color.parseColor("#444444"))
            val ops = arrayOf("==", "!=", ">", "<", ">=", "<=")
            this.adapter = createThemedSpinnerAdapter(ops)
            setSelection(ops.indexOf(node.ocrOperator).coerceAtLeast(0))
        }
        smartOcrOpLayout.addView(smartOcrOpSpinner)
        smartOcrSettings.addView(smartOcrOpLayout)
        
        val smartOcrValLayout = LinearLayout(service).apply { orientation = LinearLayout.HORIZONTAL }
        smartOcrValLayout.addView(TextView(service).apply { text = "Значение:"; setTextColor(Color.WHITE); layoutParams = LinearLayout.LayoutParams(0, WindowManager.LayoutParams.WRAP_CONTENT, 0.4f) })
        val smartOcrValEdit = EditText(service).apply {
            setText(node.ocrTargetValue.toString())
            inputType = android.text.InputType.TYPE_CLASS_NUMBER or android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL
            setTextColor(Color.WHITE)
            layoutParams = LinearLayout.LayoutParams(0, WindowManager.LayoutParams.WRAP_CONTENT, 0.6f)
        }
        smartOcrValLayout.addView(smartOcrValEdit)
        smartOcrSettings.addView(smartOcrValLayout)
        
        val smartOcrSufLayout = LinearLayout(service).apply { orientation = LinearLayout.VERTICAL }
        smartOcrSufLayout.addView(TextView(service).apply { text = "Суффиксы (k:1000, m:1000000):"; setTextColor(Color.GRAY) })
        val smartOcrSufEdit = EditText(service).apply {
            setText(node.ocrCustomSuffixes)
            setTextColor(Color.WHITE)
        }
        smartOcrSufLayout.addView(smartOcrSufEdit)
        smartOcrSettings.addView(smartOcrSufLayout)
        
        smartOcrCheck.setOnCheckedChangeListener { _, isChecked ->
            node.isSmartOcr = isChecked
            smartOcrSettings.visibility = if (isChecked) View.VISIBLE else View.GONE
        }
        smartOcrLayout.addView(smartOcrSettings)"""

content = content.replace(old_ocr_block, new_ocr_block)

# We also need to save the new fields when user clicks OK. Let's find where fields are saved in the dialog.
# The OK button in showEditNodeMenu reads from edittexts.
old_save_block = """            node.targetText = textTargetEdit.text.toString()
            node.targetLanguage = if (textLangSpinner.selectedItemPosition == 1) "eng" else if (textLangSpinner.selectedItemPosition == 2) "rus+eng" else "rus"
            node.imageThreshold = (imageThresholdEdit.text.toString().toFloatOrNull() ?: 80f)"""

new_save_block = """            node.targetText = textTargetEdit.text.toString()
            node.targetLanguage = if (textLangSpinner.selectedItemPosition == 1) "eng" else if (textLangSpinner.selectedItemPosition == 2) "rus+eng" else "rus"
            node.imageThreshold = (imageThresholdEdit.text.toString().toFloatOrNull() ?: 80f)
            
            node.ocrOperator = smartOcrOpSpinner.selectedItem.toString()
            node.ocrTargetValue = smartOcrValEdit.text.toString().toDoubleOrNull() ?: 0.0
            node.ocrCustomSuffixes = smartOcrSufEdit.text.toString()"""

content = content.replace(old_save_block, new_save_block)

# Add smartOcrLayout to triggerSettings view tree. Let's check where textTargetLayout is added.
old_trigger_add = """            triggerSettings.addView(textTargetLayout)
            triggerSettings.addView(textLangLayout)
            triggerSettings.addView(ocrFullscreenLayout)"""

new_trigger_add = """            triggerSettings.addView(textTargetLayout)
            triggerSettings.addView(textLangLayout)
            triggerSettings.addView(ocrFullscreenLayout)
            triggerSettings.addView(smartOcrLayout)"""

content = content.replace(old_trigger_add, new_trigger_add)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

print("Smart OCR UI patched")
