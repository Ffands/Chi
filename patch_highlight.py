import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

old_func = """    fun updateCurrentNodeHighlight(currentId: Int) {
        android.os.Handler(android.os.Looper.getMainLooper()).post {
            for ((id, view) in nodeViews) {
                if (view is CrosshairView) {
                    val wasCurrent = view.isCurrentTarget
                    view.isCurrentTarget = (id == currentId)
                    if (wasCurrent != view.isCurrentTarget) {
                        view.invalidate()
                    }
                }
            }
        }
    }"""

new_func = """    fun updateCurrentNodeHighlight(currentIds: List<Int>) {
        android.os.Handler(android.os.Looper.getMainLooper()).post {
            for ((id, view) in nodeViews) {
                if (view is CrosshairView) {
                    val wasCurrent = view.isCurrentTarget
                    view.isCurrentTarget = currentIds.contains(id)
                    if (wasCurrent != view.isCurrentTarget) {
                        view.invalidate()
                    }
                }
            }
        }
    }"""

content = content.replace(old_func, new_func)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("UIManager patched for highlight")
