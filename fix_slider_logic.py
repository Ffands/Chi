import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target = """        resolutionScaleLayout.addView(resolutionScaleText)
        resolutionScaleLayout.addView(resolutionScaleBar)

        val imgPreview = android.widget.ImageView(service).apply {"""

replacement = """        resolutionScaleLayout.addView(resolutionScaleText)
        resolutionScaleLayout.addView(resolutionScaleBar)

        val imgPreview = android.widget.ImageView(service).apply {
            layoutParams = LinearLayout.LayoutParams(WindowManager.LayoutParams.MATCH_PARENT, dpToPx(150)).apply { 
                gravity = Gravity.CENTER_HORIZONTAL 
                setMargins(0, dpToPx(10), 0, dpToPx(10))
            }
            scaleType = android.widget.ImageView.ScaleType.FIT_CENTER
            adjustViewBounds = true
        }

        val updatePreviewImage = {
            if (node.targetImageBase64 != null) {
                try {
                    val bytes = android.util.Base64.decode(node.targetImageBase64, android.util.Base64.DEFAULT)
                    var bitmap = android.graphics.BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
                    
                    val currentScale = (resolutionScaleBar.progress + 10) / 100f
                    if (node.triggerMode == 2) {
                        bitmap = service.enhanceBitmapForOcr(bitmap)
                    } else if (node.triggerMode == 1 && currentScale < 1.0f) {
                        val checkStep = (1f / currentScale).toInt().coerceAtLeast(1)
                        if (checkStep > 1) {
                            val sw = maxOf(1, bitmap.width / checkStep)
                            val sh = maxOf(1, bitmap.height / checkStep)
                            bitmap = android.graphics.Bitmap.createScaledBitmap(bitmap, sw, sh, false)
                        }
                    }
                    imgPreview.setImageBitmap(bitmap)
                    imgPreview.setBackgroundColor(Color.TRANSPARENT)
                } catch(e: Exception) {}
            } else {
                imgPreview.setBackgroundColor(Color.parseColor("#555555"))
            }
        }
        
        resolutionScaleBar.setOnSeekBarChangeListener(object : android.widget.SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: android.widget.SeekBar?, progress: Int, fromUser: Boolean) {
                val scale = (progress + 10) / 100f
                resolutionScaleText.text = "Качество (${(scale * 100).toInt()}%):"
                updatePreviewImage()
            }
            override fun onStartTrackingTouch(seekBar: android.widget.SeekBar?) {}
            override fun onStopTrackingTouch(seekBar: android.widget.SeekBar?) {}
        })
        
        updatePreviewImage()
"""

# Wait, I need to replace the old imgPreview block entirely!
old_imgpreview_block = """        val imgPreview = android.widget.ImageView(service).apply {
            layoutParams = LinearLayout.LayoutParams(WindowManager.LayoutParams.MATCH_PARENT, dpToPx(150)).apply { 
                gravity = Gravity.CENTER_HORIZONTAL 
                setMargins(0, dpToPx(10), 0, dpToPx(10))
            }
            scaleType = android.widget.ImageView.ScaleType.FIT_CENTER
            adjustViewBounds = true
            if (node.targetImageBase64 != null) {
                try {
                    val bytes = android.util.Base64.decode(node.targetImageBase64, android.util.Base64.DEFAULT)
                    var bitmap = android.graphics.BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
                    if (node.triggerMode == 2) {
                        bitmap = service.enhanceBitmapForOcr(bitmap)
                    }
                    setImageBitmap(bitmap)
                } catch(e: Exception) {}
            } else {
                setBackgroundColor(Color.parseColor("#555555"))
            }
        }"""

content = content.replace("        resolutionScaleLayout.addView(resolutionScaleText)\n        resolutionScaleLayout.addView(resolutionScaleBar)\n\n" + old_imgpreview_block, replacement)

# Now fix the save logic (resolutionScaleEdit no longer exists)
save_target = """                node.searchRadius = searchRadiusEdit.text.toString().toIntOrNull() ?: 0
                node.checkResolutionScale = resolutionScaleEdit.text.toString().toFloatOrNull() ?: 1.0f
                node.targetText = textTargetEdit.text.toString().takeIf { it.isNotEmpty() }"""

save_replace = """                node.searchRadius = searchRadiusEdit.text.toString().toIntOrNull() ?: 0
                node.checkResolutionScale = (resolutionScaleBar.progress + 10) / 100f
                node.targetText = textTargetEdit.text.toString().takeIf { it.isNotEmpty() }"""

content = content.replace(save_target, save_replace)

# Also fix the updatePreviewImage call inside captureImageFragment callback!
capture_callback_target = """                                if (node.triggerMode == 2) {
                                    bitmap = service.enhanceBitmapForOcr(bitmap)
                                }
                                imgPreview.setImageBitmap(bitmap)"""

capture_callback_replace = """                                updatePreviewImage()"""

content = content.replace(capture_callback_target, capture_callback_replace)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
