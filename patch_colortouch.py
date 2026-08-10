import sys
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

func_def = """    fun setupColorCompareTouchListener(view: View, params: WindowManager.LayoutParams, node: TargetNode) {
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f

        view.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = params.x
                    initialY = params.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    params.x = initialX + (event.rawX - initialTouchX).toInt()
                    params.y = initialY + (event.rawY - initialTouchY).toInt()
                    windowManager.updateViewLayout(view, params)
                    val newEx = params.x + dpToPx(20)
                    val newEy = params.y + dpToPx(20)
                    node.colorCompareX = newEx
                    node.colorCompareY = newEy
                    invalidateLines()
                    true
                }
                MotionEvent.ACTION_UP -> {
                    val newEx = params.x + dpToPx(20)
                    val newEy = params.y + dpToPx(20)
                    node.colorCompareX = newEx
                    node.colorCompareY = newEy
                    invalidateLines()
                    true
                }
                else -> false
            }
        }
    }

"""

if "fun setupColorCompareTouchListener" not in content:
    content = content.replace("    fun setupSwipeEndTouchListener", func_def + "    fun setupSwipeEndTouchListener")
    with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
        f.write(content)
    print("Added setupColorCompareTouchListener")
