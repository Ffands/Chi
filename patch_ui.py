import sys
import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Fix topScroll width to WRAP_CONTENT so it shrinks when buttons are hidden
bad_scroll = "layoutParams = LinearLayout.LayoutParams(dpToPx(180), LinearLayout.LayoutParams.WRAP_CONTENT)"
good_scroll = "layoutParams = LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT)"
content = content.replace(bad_scroll, good_scroll)

# Fix minMaxBtn to force update layout
bad_minmax = """                if (isMinimized) hotbarRow.visibility = View.GONE
            }"""
good_minmax = """                if (isMinimized) hotbarRow.visibility = View.GONE
                floatingControlBar?.let {
                    val p = it.layoutParams as? WindowManager.LayoutParams
                    if (p != null) windowManager.updateViewLayout(it, p)
                }
            }"""
content = content.replace(bad_minmax, good_minmax)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("UI patched")
