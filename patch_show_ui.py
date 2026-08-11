import sys
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_show = """    fun showFloatingControlBar() {
        if (floatingControlBar != null) return"""

good_show = """    fun showFloatingControlBar() {
        if (floatingControlBar != null) {
            floatingControlBar?.visibility = View.VISIBLE
            return
        }"""

bad_exit = """        val exitBtn = Button(service).apply {
            text = "✖"
            setTextColor(Color.parseColor("#FFD50000"))
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            setOnClickListener {
                try {
                    service.disableSelf()
                } catch(e: Exception) {}
                removeAllViews()
            }
        }"""

good_exit = """        val exitBtn = Button(service).apply {
            text = "✖"
            setTextColor(Color.parseColor("#FFD50000"))
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            setOnClickListener {
                floatingControlBar?.visibility = View.GONE
            }
        }"""

content = content.replace(bad_show, good_show)
content = content.replace(bad_exit, good_exit)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Patched showFloatingControlBar and exitBtn")
