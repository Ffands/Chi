import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """        val exitBtn = Button(service).apply {
            text = "✖"
            setTextColor(Color.parseColor("#FFD50000"))
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            setOnClickListener {
                floatingControlBar?.visibility = View.GONE
            }
        }"""

good_str = """        val exitBtn = Button(service).apply {
            text = "✖"
            setTextColor(Color.parseColor("#FFD50000"))
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            setOnClickListener {
                if (service.isPlaying) service.togglePlay()
                if (service.isRecording) service.toggleRecording()
                service.nodes.clear()
                removeAllViews()
                floatingControlBar = null
                modMenu = null
                nodeViews.clear()
                swipeEndViews.clear()
                textZoneStartViews.clear()
                textZoneEndViews.clear()
                colorCompareViews.clear()
                linesOverlay?.let { try { windowManager.removeView(it) } catch(e:Exception){} }
                linesOverlay = null
                // Also update main app status if needed, but the main app is likely in background.
            }
        }"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("exitBtn patched")
