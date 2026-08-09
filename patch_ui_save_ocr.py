with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target = "node.ocrFullScreenClick = ocrFullscreenCheck.isChecked"
replacement = """node.ocrFullScreenClick = ocrFullscreenCheck.isChecked
                node.ocrOperator = arrayOf("==", "!=", ">", "<", ">=", "<=")[smartOcrOpSpinner.selectedItemPosition]
                node.ocrTargetValue = smartOcrValEdit.text.toString().toDoubleOrNull() ?: 0.0
                node.ocrCustomSuffixes = smartOcrSufEdit.text.toString()"""

if target in content:
    content = content.replace(target, replacement)
    with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
        f.write(content)
    print("Patched UIManager save logic for Smart OCR")
else:
    print("Could not find target line")
