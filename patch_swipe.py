import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_swipeline = """                        // Swipe line
                        if (node.isSwipe && node.swipeEndX != null && node.swipeEndY != null) {
                            val params = nodeParams[node.id]
                            if (params != null) {
                                val startX = params.x + dpToPx(30).toFloat()
                                val startY = params.y + dpToPx(30).toFloat()
                                val endX = node.swipeEndX!!
                                val endY = node.swipeEndY!!"""

repl_swipeline = """                        // Swipe line
                        if (node.isSwipe) {
                            val params = nodeParams[node.id]
                            if (params != null) {
                                val startX = params.x + dpToPx(30).toFloat()
                                val startY = params.y + dpToPx(30).toFloat()
                                
                                var finalEndX = node.swipeEndX.toFloat()
                                var finalEndY = node.swipeEndY.toFloat()
                                
                                if (node.swipeTargetNodeId != null) {
                                    val tNode = service.nodes.find { it.id == node.swipeTargetNodeId }
                                    if (tNode != null) {
                                        val tParams = nodeParams[tNode.id]
                                        if (tParams != null) {
                                            finalEndX = tParams.x + dpToPx(30).toFloat()
                                            finalEndY = tParams.y + dpToPx(30).toFloat()
                                        }
                                    }
                                }
                                
                                val endX = finalEndX
                                val endY = finalEndY"""

content = content.replace(find_swipeline, repl_swipeline)

find_arrow_angle = """                                val path = android.graphics.Path().apply {
                                    moveTo(endX.toFloat(), endY.toFloat())
                                    lineTo(p1x.toFloat(), p1y.toFloat())
                                    lineTo(p2x.toFloat(), p2y.toFloat())
                                    close()
                                }"""
repl_arrow_angle = """                                val path = android.graphics.Path().apply {
                                    moveTo(endX, endY)
                                    lineTo(p1x, p1y)
                                    lineTo(p2x, p2y)
                                    close()
                                }"""
content = content.replace(find_arrow_angle, repl_arrow_angle)


# Also we need to fix the UI settings for the swipe mode
find_ui = """        val swipeDeltaLayout = LinearLayout(service).apply { orientation = LinearLayout.VERTICAL; setPadding(0, 5, 0, 0) }
        swipeDeltaLayout.addView(TextView(service).apply { text = "Вести к Триггеру №: "; setTextColor(Color.WHITE) })
        val swipeTargetEdit = EditText(service).apply {
            inputType = InputType.TYPE_CLASS_NUMBER
            setText(node.swipeTargetNodeId?.toString() ?: "")
            hint = "(Нет)"
            setHintTextColor(Color.parseColor("#AAAAAA"))
            setTextColor(Color.WHITE)
            layoutParams = LinearLayout.LayoutParams(WindowManager.LayoutParams.MATCH_PARENT, WindowManager.LayoutParams.WRAP_CONTENT)
        }
        swipeDeltaLayout.addView(swipeTargetEdit)"""

repl_ui = """        val swipeDeltaLayout = LinearLayout(service).apply { orientation = LinearLayout.VERTICAL; setPadding(0, 10, 0, 0) }
        val modeSpinnerLayout = LinearLayout(service).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        modeSpinnerLayout.addView(TextView(service).apply { text = "Режим свайпа: "; setTextColor(Color.WHITE) })
        val modeSpinner = Spinner(service).apply {
            adapter = android.widget.ArrayAdapter(service, android.R.layout.simple_spinner_item, arrayOf("Вектор (Суб-метка)", "К метке (ID)", "Ломаная линия (Жест)"))
            setSelection(if (node.swipePathPoints.isNotEmpty()) 2 else if (node.swipeTargetNodeId != null) 1 else 0)
        }
        modeSpinnerLayout.addView(modeSpinner)
        swipeDeltaLayout.addView(modeSpinnerLayout)

        val swipeTargetEditLayout = LinearLayout(service).apply { orientation = LinearLayout.HORIZONTAL; setPadding(0, 5, 0, 0); gravity = Gravity.CENTER_VERTICAL }
        swipeTargetEditLayout.addView(TextView(service).apply { text = "ID цели: "; setTextColor(Color.WHITE) })
        val swipeTargetEdit = EditText(service).apply {
            inputType = InputType.TYPE_CLASS_NUMBER
            setText(node.swipeTargetNodeId?.toString() ?: "")
            hint = "(Введите ID)"
            setHintTextColor(Color.parseColor("#AAAAAA"))
            setTextColor(Color.WHITE)
            layoutParams = LinearLayout.LayoutParams(dpToPx(100), WindowManager.LayoutParams.WRAP_CONTENT)
        }
        swipeTargetEditLayout.addView(swipeTargetEdit)
        swipeDeltaLayout.addView(swipeTargetEditLayout)
        
        modeSpinner.onItemSelectedListener = object : android.widget.AdapterView.OnItemSelectedListener {
            override fun onItemSelected(p0: android.widget.AdapterView<*>?, p1: View?, pos: Int, p3: Long) {
                swipeTargetEditLayout.visibility = if (pos == 1) View.VISIBLE else View.GONE
                
                if (pos == 0) {
                    // Vector
                    node.swipeTargetNodeId = null
                    node.swipePathPoints = emptyList()
                    if (node.isSwipe) createSwipeEndMarker(node)
                } else if (pos == 1) {
                    // To ID
                    removeSwipeEndMarker(node.id)
                    node.swipePathPoints = emptyList()
                } else if (pos == 2) {
                    // Gesture (don't clear points if we just switched to view it)
                    removeSwipeEndMarker(node.id)
                    node.swipeTargetNodeId = null
                }
                invalidateLines()
            }
            override fun onNothingSelected(p0: android.widget.AdapterView<*>?) {}
        }"""
content = content.replace(find_ui, repl_ui)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Swipe UX patched!")
