import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """                    swipeEndViews[it.id]?.visibility = if (it.isVisible) View.VISIBLE else View.GONE
                    textZoneStartViews[it.id]?.visibility = if (it.isVisible) View.VISIBLE else View.GONE
                    textZoneEndViews[it.id]?.visibility = if (it.isVisible) View.VISIBLE else View.GONE
                }
                invalidateLines()"""

good_str = """                    swipeEndViews[it.id]?.visibility = if (it.isVisible) View.VISIBLE else View.GONE
                    textZoneStartViews[it.id]?.visibility = if (it.isVisible) View.VISIBLE else View.GONE
                    textZoneEndViews[it.id]?.visibility = if (it.isVisible) View.VISIBLE else View.GONE
                    colorCompareViews[it.id]?.visibility = if (it.isVisible) View.VISIBLE else View.GONE
                }
                invalidateLines()"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("togglevis patched")
