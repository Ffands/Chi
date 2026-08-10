import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# 1. Replace SwipeEndView with SubMarkerView (for both swipe and color)
old_swipe_end_view = """class SwipeEndView(context: Context, val node: TargetNode) : View(context) {
    private val density = context.resources.displayMetrics.density
    
    private val paint = Paint().apply {
        style = Paint.Style.STROKE
        isAntiAlias = true
        color = Color.parseColor("#FF00FF") // Magenta
    }
    
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        paint.strokeWidth = 3f * density * node.sizeScale
        val cx = width / 2f
        val cy = height / 2f
        val radius = 6f * density * node.sizeScale
        canvas.drawCircle(cx, cy, radius, paint)
        canvas.drawLine(cx - radius, cy, cx + radius, cy, paint)
        canvas.drawLine(cx, cy - radius, cx, cy + radius, paint)
    }
}"""

new_sub_marker_view = """class SubMarkerView(context: Context, val node: TargetNode, val markerType: Int) : View(context) {
    // 1 = Swipe, 2 = Color Compare
    private val density = context.resources.displayMetrics.density
    
    private val paint = Paint().apply {
        style = Paint.Style.STROKE
        isAntiAlias = true
        color = if (markerType == 1) Color.parseColor("#00BFFF") else Color.parseColor("#FF00FF") // Cyan for swipe, Magenta for color
        strokeWidth = 2f * density * node.sizeScale
    }
    private val fillPaint = Paint().apply {
        style = Paint.Style.FILL
        isAntiAlias = true
        color = paint.color
        alpha = 80
    }
    private val textPaint = Paint().apply {
        color = Color.WHITE
        textSize = 10f * density * node.sizeScale
        isAntiAlias = true
        textAlign = Paint.Align.CENTER
        setShadowLayer(2f, 1f, 1f, Color.BLACK)
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val cx = width / 2f
        val cy = height / 2f
        
        val radius = 8f * density * node.sizeScale
        val innerRadius = 3f * density * node.sizeScale
        val lineExt = 4f * density * node.sizeScale
        
        canvas.drawCircle(cx, cy, radius, paint)
        canvas.drawCircle(cx, cy, innerRadius, fillPaint)
        
        canvas.drawLine(cx, cy - radius - lineExt, cx, cy + radius + lineExt, paint)
        canvas.drawLine(cx - radius - lineExt, cy, cx + radius + lineExt, cy, paint)
        
        val label = if (markerType == 1) "S${node.id}" else "C${node.id}"
        canvas.drawText(label, cx + radius + lineExt, cy - radius, textPaint)
    }
}"""

if old_swipe_end_view in content:
    content = content.replace(old_swipe_end_view, new_sub_marker_view)
else:
    print("Could not find SwipeEndView!")

# 2. Patch createSwipeEndMarker to use SubMarkerView
find_swipe = """val swipeEndView = SwipeEndView(service, node)"""
repl_swipe = """val swipeEndView = SubMarkerView(service, node, 1)"""
content = content.replace(find_swipe, repl_swipe)

# 3. Patch createColorCompareMarker to use SubMarkerView
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

        container.visibility = if (node.isVisible) View.VISIBLE else View.GONE
        setupColorCompareTouchListener(container, params, node)

        windowManager.addView(container, params)
        colorCompareViews[node.id] = container
        colorCompareParams[node.id] = params
    }"""

repl_ccm = """    fun createColorCompareMarker(node: TargetNode) {
        if (colorCompareViews.containsKey(node.id)) return

        if (node.colorCompareX == null || node.colorCompareY == null) {
            node.colorCompareX = node.x + dpToPx(30)
            node.colorCompareY = node.y + dpToPx(30)
        }

        val container = SubMarkerView(service, node, 2)

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

        container.visibility = if (node.isVisible) View.VISIBLE else View.GONE
        setupColorCompareTouchListener(container, params, node)

        windowManager.addView(container, params)
        colorCompareViews[node.id] = container
        colorCompareParams[node.id] = params
    }"""
if find_ccm in content:
    content = content.replace(find_ccm, repl_ccm)
else:
    print("Could not find createColorCompareMarker!")

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Sub-markers patched!")
