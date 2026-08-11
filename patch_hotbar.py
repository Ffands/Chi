import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """            setOnClickListener {
                if (hotbarRow.visibility == View.VISIBLE) {
                    hotbarRow.visibility = View.GONE
                } else {
                    hotbarRow.visibility = View.VISIBLE
                    updateHotbar(hotbarContainer)
                }
            }"""

good_str = """            setOnClickListener {
                if (hotbarRow.visibility == View.VISIBLE) {
                    hotbarRow.visibility = View.GONE
                } else {
                    hotbarRow.visibility = View.VISIBLE
                    updateHotbar(hotbarContainer)
                }
                floatingControlBar?.let {
                    val p = it.layoutParams as? WindowManager.LayoutParams
                    if (p != null) windowManager.updateViewLayout(it, p)
                }
            }"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("hotbar toggle patched")
