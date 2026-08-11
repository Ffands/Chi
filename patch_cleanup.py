import sys

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

bad_str = """    fun stopAll() {
        isPlaying = false
        isRecording = false
        activeThreads.clear()
        uiManager.applyUISettings()
        uiManager.recreateFloatingControlBar()
        uiManager.setNodesTouchable(true)
    }"""

good_str = """    fun stopAll() {
        isPlaying = false
        isRecording = false
        activeThreads.clear()
        cachedBitmap?.recycle()
        cachedBitmap = null
        uiManager.applyUISettings()
        uiManager.recreateFloatingControlBar()
        uiManager.setNodesTouchable(true)
    }"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("cleanup patched")
