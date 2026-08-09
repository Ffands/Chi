import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

# Add gesture queue variables
vars_old = """    val activeThreads = java.util.concurrent.CopyOnWriteArrayList<ExecutionThread>()"""
vars_new = """    val activeThreads = java.util.concurrent.CopyOnWriteArrayList<ExecutionThread>()
    
    // Gesture Queue
    private val gestureQueue = java.util.concurrent.ConcurrentLinkedQueue<android.accessibilityservice.GestureDescription>()
    private var isDispatchingGesture = false
    
    private fun processGestureQueue() {
        if (isDispatchingGesture || gestureQueue.isEmpty() || !isPlaying) return
        val gesture = gestureQueue.poll() ?: return
        
        isDispatchingGesture = true
        dispatchGesture(gesture, object : android.accessibilityservice.AccessibilityService.GestureResultCallback() {
            override fun onCompleted(gestureDescription: android.accessibilityservice.GestureDescription?) {
                isDispatchingGesture = false
                processGestureQueue()
            }
            override fun onCancelled(gestureDescription: android.accessibilityservice.GestureDescription?) {
                isDispatchingGesture = false
                processGestureQueue()
            }
        }, null)
    }"""
content = content.replace(vars_old, vars_new)

# Modify performGestureForNodes
old_dispatch = """        dispatchGesture(builder.build(), null, null)"""
new_dispatch = """        gestureQueue.add(builder.build())
        processGestureQueue()"""
content = content.replace(old_dispatch, new_dispatch)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Gesture Queue patched")
