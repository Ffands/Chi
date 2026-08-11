import sys
import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """    fun removeAllViews() {
        floatingControlBar?.let { windowManager.removeView(it) }
        modMenu?.let { windowManager.removeView(it) }
        nodeViews.values.forEach { windowManager.removeView(it) }
        swipeEndViews.values.forEach { windowManager.removeView(it) }
        textZoneStartViews.values.forEach { windowManager.removeView(it) }
        textZoneEndViews.values.forEach { windowManager.removeView(it) }
        colorCompareViews.values.forEach { windowManager.removeView(it) }
    }"""

good_str = """    fun removeAllViews() {
        try { floatingControlBar?.let { windowManager.removeView(it) } } catch(e: Exception){}
        try { modMenu?.let { windowManager.removeView(it) } } catch(e: Exception){}
        try { nodeViews.values.forEach { windowManager.removeView(it) } } catch(e: Exception){}
        try { swipeEndViews.values.forEach { windowManager.removeView(it) } } catch(e: Exception){}
        try { textZoneStartViews.values.forEach { windowManager.removeView(it) } } catch(e: Exception){}
        try { textZoneEndViews.values.forEach { windowManager.removeView(it) } } catch(e: Exception){}
        try { colorCompareViews.values.forEach { windowManager.removeView(it) } } catch(e: Exception){}
        try { linesOverlay?.let { windowManager.removeView(it) } } catch(e: Exception){}
    }"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("removeAllViews patched")
