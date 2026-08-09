with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

func = """
    fun showOcrResultDialog(ocrText: String, searchedText: String, isMatch: Boolean, image: android.graphics.Bitmap) {
        android.os.Handler(android.os.Looper.getMainLooper()).post {
            val dialogView = android.widget.LinearLayout(service).apply {
                orientation = android.widget.LinearLayout.VERTICAL
                setPadding(dpToPx(20), dpToPx(20), dpToPx(20), dpToPx(20))
                
                addView(android.widget.TextView(service).apply {
                    text = "Huawei OCR: '$ocrText'\\n\\nИскали: '$searchedText'\\nИтог: $isMatch\\n\\nЧто видит OCR:"
                    setTextColor(android.graphics.Color.WHITE)
                    textSize = 14f
                })
                
                val iv = android.widget.ImageView(service).apply {
                    setImageBitmap(image)
                    layoutParams = android.widget.LinearLayout.LayoutParams(
                        android.view.ViewGroup.LayoutParams.MATCH_PARENT,
                        dpToPx(200)
                    ).apply { setMargins(0, dpToPx(10), 0, 0) }
                    scaleType = android.widget.ImageView.ScaleType.FIT_CENTER
                }
                addView(iv)
            }
            
            val dialog = android.app.AlertDialog.Builder(service, android.R.style.Theme_DeviceDefault_Dialog_Alert)
                .setTitle("Результат OCR (Huawei)")
                .setView(dialogView)
                .setPositiveButton("OK", null)
                .create()
                
            dialog.window?.setType(android.view.WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY)
            dialog.show()
        }
    }
"""

if "fun showOcrResultDialog" not in content:
    idx = content.rfind("}")
    content = content[:idx] + func + content[idx:]
    with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
        f.write(content)
    print("Added showOcrResultDialog to UIManager")
else:
    print("showOcrResultDialog already exists")
