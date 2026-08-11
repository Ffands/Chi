import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """    fun applyUIScaleChange() {
        val currentTag = menuContentContainer.getChildAt(0)?.tag as? String
        recreateFloatingControlBar()
        // we recreate all node views too, otherwise their size stays old
        service.nodes.forEach { 
            nodeViews[it.id]?.let { view -> windowManager.removeView(view) }
        }
        nodeViews.clear()
        recreateAllNodeViews()
        recreateModMenu(currentTag)
    }"""

good_str = """    fun applyUIScaleChange() {
        val currentTag = menuContentContainer.getChildAt(0)?.tag as? String
        recreateFloatingControlBar()
        
        // Remove all markers
        service.nodes.forEach { 
            nodeViews[it.id]?.let { view -> windowManager.removeView(view) }
            swipeEndViews[it.id]?.let { view -> windowManager.removeView(view) }
            colorCompareViews[it.id]?.let { view -> windowManager.removeView(view) }
            textZoneStartViews[it.id]?.let { view -> windowManager.removeView(view) }
            textZoneEndViews[it.id]?.let { view -> windowManager.removeView(view) }
        }
        nodeViews.clear()
        swipeEndViews.clear()
        colorCompareViews.clear()
        textZoneStartViews.clear()
        textZoneEndViews.clear()
        
        recreateAllNodeViews()
        recreateModMenu(currentTag)
    }"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("uiscale patched")
