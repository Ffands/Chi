import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_ccm = """    fun createColorCompareMarker(node: TargetNode) {
        if (colorCompareViews.containsKey(node.id)) return

        if (node.colorCompareX == null || node.colorCompareY == null) {
            node.colorCompareX = node.x + dpToPx(30)
            node.colorCompareY = node.y + dpToPx(30)
        }

        val container = FrameLayout(service)
        val diamond = android.view.View(service).apply {
            background = android.graphics.drawable.GradientDrawable().apply {
                shape = android.graphics.drawable.GradientDrawable.RECTANGLE
                setColor(Color.MAGENTA)
                setStroke(dpToPx(2), Color.WHITE)
            }
            rotation = 45f
            alpha = 0.8f
        }
        val text = TextView(service).apply {
            text = "c"
            setTextColor(Color.WHITE)
            textSize = 10f * uiScale
            gravity = Gravity.CENTER
            setShadowLayer(2f, 1f, 1f, Color.BLACK)
        }

        container.addView(diamond, FrameLayout.LayoutParams(dpToPx(20), dpToPx(20)).apply { gravity = Gravity.CENTER })
        container.addView(text, FrameLayout.LayoutParams(dpToPx(24), dpToPx(24)).apply { gravity = Gravity.CENTER })

        val params = WindowManager.LayoutParams(
            dpToPx(40), dpToPx(40),
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = node.colorCompareX!! - dpToPx(20)
            y = node.colorCompareY!! - dpToPx(20)
        }

        var flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN
        if (service.isPlaying || service.isRecording) {
            flags = flags or WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE
        }
        params.flags = flags

        container.visibility = if (node.isVisible) View.VISIBLE else View.GONE
        setupColorCompareTouchListener(container, params, node)

        windowManager.addView(container, params)
        colorCompareViews[node.id] = container
        colorCompareParams[node.id] = params
    }"""

find_ccm_regex = r"    fun createColorCompareMarker\(node: TargetNode\) \{[\s\S]*?colorCompareParams\[node\.id\] = params\n    \}"

repl_ccm = """    fun createColorCompareMarker(node: TargetNode) {
        if (colorCompareViews.containsKey(node.id)) return

        if (node.colorCompareX == null || node.colorCompareY == null) {
            node.colorCompareX = node.x + dpToPx(30)
            node.colorCompareY = node.y + dpToPx(30)
        }

        val container = SubMarkerView(service, node, 2)

        var flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN
        if (service.isPlaying || service.isRecording) {
            flags = flags or WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE
        }

        val params = WindowManager.LayoutParams(
            dpToPx(40), dpToPx(40),
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,
            flags,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = node.colorCompareX!! - dpToPx(20)
            y = node.colorCompareY!! - dpToPx(20)
        }

        container.visibility = if (node.isVisible) View.VISIBLE else View.GONE
        setupColorCompareTouchListener(container, params, node)

        windowManager.addView(container, params)
        colorCompareViews[node.id] = container
        colorCompareParams[node.id] = params
    }"""

content = re.sub(find_ccm_regex, repl_ccm, content)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Color compare patched!")
