import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """    fun setNodesTouchable(touchable: Boolean) {
        for ((id, view) in nodeViews) {
            val params = nodeParams[id] ?: continue
            if (touchable) {
                params.flags = params.flags and WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE.inv()
            } else {
                params.flags = params.flags or WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE
            }
            windowManager.updateViewLayout(view, params)
        }
    }"""

good_str = """    fun setNodesTouchable(touchable: Boolean) {
        val lists = listOf(
            nodeViews to nodeParams,
            swipeEndViews to swipeEndParams,
            colorCompareViews to colorCompareParams,
            textZoneStartViews to textZoneStartParams,
            textZoneEndViews to textZoneEndParams
        )
        for ((viewsMap, paramsMap) in lists) {
            for ((id, view) in viewsMap) {
                val params = paramsMap[id] ?: continue
                if (touchable) {
                    params.flags = params.flags and WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE.inv()
                } else {
                    params.flags = params.flags or WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE
                }
                windowManager.updateViewLayout(view, params)
            }
        }
    }"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("setNodesTouchable patched")
