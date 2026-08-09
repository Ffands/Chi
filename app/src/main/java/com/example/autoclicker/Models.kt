package com.example.autoclicker

import android.graphics.Color

enum class NodeType { CLICK, CHECK_COLOR }
enum class AppMode { SINGLE, SEQUENTIAL, ADVANCED, RECORD }

data class TargetNode(
    var id: Int,
    var type: NodeType = NodeType.CLICK,
    var x: Int = 0,
    var y: Int = 0,
    var targetColor: Int? = null,
    var targetImageBase64: String? = null,
    var targetText: String? = null,
    var targetLanguage: String = "rus", // "rus" or "eng"
    var triggerMode: Int = -1, // -1: None, 0 = Pixel Color, 1 = Image Fragment, 2 = Text
    var dynamicColorUpdate: Boolean = false,
    var compareToNodeId: Int? = null,
    var colorCompareX: Int? = null,
    var colorCompareY: Int? = null,
    var imageThreshold: Float = 80f,
    var searchRadius: Int = 0,
    var delayAfterMs: Long = 300L,
    var randomizeDelayMs: Long = 0L,
    var randomizeRadius: Int = 0,
    var nextNodeIdOnSuccess: Int? = null,
    var nextNodeIdOnFail: Int? = null,
    var skipSequentialExecution: Boolean = false,
    var isVisible: Boolean = true,
    var crosshairColor: Int = Color.RED,
    var numberColor: Int = Color.WHITE,
    var sizeScale: Float = 1.0f,
    var syncWithNodeIds: String = "",
    var clickDurationMs: Long = 50L,
    var isSwipe: Boolean = false,
    var swipeTargetNodeId: Int? = null,
    var swipeEndX: Int = 0,
    var swipeEndY: Int = 0,
    var swipeDurationMs: Long = 500L,
    var textZoneStartX: Int = 0,
    var textZoneStartY: Int = 0,
    var textZoneEndX: Int = 0,
    var textZoneEndY: Int = 0,
    var maxCheckCycles: Int? = null,
    var colorOperator: String = "==",
    var colorTolerance: Int = 15,
    var linkedConditionNodeId: Int? = null,
    var linkedConditionOperator: String = "AND",
    var repetitions: Int = 1,
    var swipePathPoints: List<Pair<Float, Float>> = emptyList(),
    var ocrFullScreenClick: Boolean = false,
    var checkResolutionScale: Float = 1.0f,
    var isSmartOcr: Boolean = false,
    var ocrOperator: String = ">=",
    var ocrTargetValue: Double = 0.0,
    var ocrCustomSuffixes: String = "k:1000,m:1000000,b:1000000000,к:1000,м:1000000,б:1000000000"
) {
    @Transient var currentCheckCycle: Int = 0
    @Transient var currentRepetition: Int = 0
    @Transient var cachedTargetBitmap: android.graphics.Bitmap? = null

    fun colorMatch(otherColor: Int): Boolean {
        if(targetColor == null) return true
        val c1 = targetColor!!
        val c2 = otherColor
        val rDiff = Math.abs(Color.red(c1) - Color.red(c2))
        val gDiff = Math.abs(Color.green(c1) - Color.green(c2))
        val bDiff = Math.abs(Color.blue(c1) - Color.blue(c2))
        val isMatch = rDiff <= colorTolerance && gDiff <= colorTolerance && bDiff <= colorTolerance
        return if (colorOperator == "!=") !isMatch else isMatch
    }

    fun toJson(): org.json.JSONObject {
        val obj = org.json.JSONObject()
        obj.put("id", id)
        obj.put("type", type.name)
        obj.put("x", x)
        obj.put("y", y)
        if (targetColor != null) obj.put("targetColor", targetColor)
        if (targetImageBase64 != null) obj.put("targetImageBase64", targetImageBase64)
        if (targetText != null) obj.put("targetText", targetText)
        obj.put("targetLanguage", targetLanguage)
        obj.put("triggerMode", triggerMode)
        obj.put("dynamicColorUpdate", dynamicColorUpdate)
        if (compareToNodeId != null) obj.put("compareToNodeId", compareToNodeId)
        if (colorCompareX != null) obj.put("colorCompareX", colorCompareX)
        if (colorCompareY != null) obj.put("colorCompareY", colorCompareY)
        obj.put("imageThreshold", imageThreshold.toDouble())
        obj.put("searchRadius", searchRadius)
        obj.put("delayAfterMs", delayAfterMs)
        obj.put("randomizeDelayMs", randomizeDelayMs)
        obj.put("randomizeRadius", randomizeRadius)
        if (nextNodeIdOnSuccess != null) obj.put("nextNodeIdOnSuccess", nextNodeIdOnSuccess)
        if (nextNodeIdOnFail != null) obj.put("nextNodeIdOnFail", nextNodeIdOnFail)
        obj.put("skipSequentialExecution", skipSequentialExecution)
        obj.put("isVisible", isVisible)
        obj.put("crosshairColor", crosshairColor)
        obj.put("numberColor", numberColor)
        obj.put("sizeScale", sizeScale.toDouble())
        if (syncWithNodeIds.isNotEmpty()) obj.put("syncWithNodeIds", syncWithNodeIds)
        obj.put("clickDurationMs", clickDurationMs)
        obj.put("isSwipe", isSwipe)
        if (swipeTargetNodeId != null) obj.put("swipeTargetNodeId", swipeTargetNodeId)
        obj.put("swipeEndX", swipeEndX)
        obj.put("swipeEndY", swipeEndY)
        obj.put("swipeDurationMs", swipeDurationMs)
        obj.put("textZoneStartX", textZoneStartX)
        obj.put("textZoneStartY", textZoneStartY)
        obj.put("textZoneEndX", textZoneEndX)
        obj.put("textZoneEndY", textZoneEndY)
        if (maxCheckCycles != null) obj.put("maxCheckCycles", maxCheckCycles)
        obj.put("colorOperator", colorOperator)
        obj.put("colorTolerance", colorTolerance)
        if (linkedConditionNodeId != null) obj.put("linkedConditionNodeId", linkedConditionNodeId)
        obj.put("linkedConditionOperator", linkedConditionOperator)
        obj.put("repetitions", repetitions)
        obj.put("ocrFullScreenClick", ocrFullScreenClick)
        obj.put("checkResolutionScale", checkResolutionScale.toDouble())
        obj.put("isSmartOcr", isSmartOcr)
        obj.put("ocrOperator", ocrOperator)
        obj.put("ocrTargetValue", ocrTargetValue)
        obj.put("ocrCustomSuffixes", ocrCustomSuffixes)
        if (swipePathPoints.isNotEmpty()) {
            val pointArr = org.json.JSONArray()
            for (p in swipePathPoints) {
                val po = org.json.JSONObject()
                po.put("x", p.first.toDouble())
                po.put("y", p.second.toDouble())
                pointArr.put(po)
            }
            obj.put("swipePathPoints", pointArr)
        }
        return obj
    }

    companion object {
        fun fromJson(obj: org.json.JSONObject): TargetNode {
            val tMode = obj.optInt("triggerMode", -1)
            val tColor = if (obj.has("targetColor")) obj.getInt("targetColor") else null
            val tImage = obj.optString("targetImageBase64", null).takeIf { it?.isNotEmpty() == true }
            val tText = obj.optString("targetText", null).takeIf { it?.isNotEmpty() == true }
            
            val pathPoints = mutableListOf<Pair<Float, Float>>()
            if (obj.has("swipePathPoints")) {
                val arr = obj.getJSONArray("swipePathPoints")
                for (i in 0 until arr.length()) {
                    val po = arr.getJSONObject(i)
                    pathPoints.add(Pair(po.getDouble("x").toFloat(), po.getDouble("y").toFloat()))
                }
            }
            
            return TargetNode(
                id = obj.getInt("id"),
                type = NodeType.valueOf(obj.getString("type")),
                x = obj.getInt("x"),
                y = obj.getInt("y"),
                targetColor = tColor,
                targetImageBase64 = tImage,
                targetText = tText,
                targetLanguage = obj.optString("targetLanguage", "rus"),
                triggerMode = if (tMode == 0 && tColor == null && tImage == null && tText == null) -1 else tMode,
                dynamicColorUpdate = obj.optBoolean("dynamicColorUpdate", false),
                compareToNodeId = if (obj.has("compareToNodeId")) obj.getInt("compareToNodeId") else null,
                colorCompareX = if (obj.has("colorCompareX")) obj.getInt("colorCompareX") else null,
                colorCompareY = if (obj.has("colorCompareY")) obj.getInt("colorCompareY") else null,
                imageThreshold = obj.optDouble("imageThreshold", 80.0).toFloat(),
                searchRadius = obj.optInt("searchRadius", 0),
                delayAfterMs = obj.optLong("delayAfterMs", 300L),
                randomizeDelayMs = obj.optLong("randomizeDelayMs", 0L),
                randomizeRadius = obj.optInt("randomizeRadius", 0),
                nextNodeIdOnSuccess = if (obj.has("nextNodeIdOnSuccess")) obj.getInt("nextNodeIdOnSuccess") else null,
                nextNodeIdOnFail = if (obj.has("nextNodeIdOnFail")) obj.getInt("nextNodeIdOnFail") else null,
                skipSequentialExecution = obj.optBoolean("skipSequentialExecution", false),
                isVisible = obj.optBoolean("isVisible", true),
                crosshairColor = obj.optInt("crosshairColor", Color.RED),
                numberColor = obj.optInt("numberColor", Color.WHITE),
                sizeScale = obj.optDouble("sizeScale", 1.0).toFloat(),
                syncWithNodeIds = obj.optString("syncWithNodeIds", ""),
                clickDurationMs = obj.optLong("clickDurationMs", 50L),
                isSwipe = obj.optBoolean("isSwipe", false),
                swipeTargetNodeId = if (obj.has("swipeTargetNodeId")) obj.getInt("swipeTargetNodeId") else null,
                swipeEndX = obj.optInt("swipeEndX", 0),
                swipeEndY = obj.optInt("swipeEndY", 0),
                swipeDurationMs = obj.optLong("swipeDurationMs", 500L),
                textZoneStartX = obj.optInt("textZoneStartX", 0),
                textZoneStartY = obj.optInt("textZoneStartY", 0),
                textZoneEndX = obj.optInt("textZoneEndX", 0),
                textZoneEndY = obj.optInt("textZoneEndY", 0),
                maxCheckCycles = if (obj.has("maxCheckCycles")) obj.getInt("maxCheckCycles") else null,
                colorOperator = obj.optString("colorOperator", "=="),
                colorTolerance = obj.optInt("colorTolerance", 15),
                linkedConditionNodeId = if (obj.has("linkedConditionNodeId")) obj.getInt("linkedConditionNodeId") else null,
                linkedConditionOperator = obj.optString("linkedConditionOperator", "AND"),
                repetitions = obj.optInt("repetitions", 1),
                swipePathPoints = pathPoints,
                ocrFullScreenClick = obj.optBoolean("ocrFullScreenClick", false),
                checkResolutionScale = obj.optDouble("checkResolutionScale", 1.0).toFloat(),
                isSmartOcr = obj.optBoolean("isSmartOcr", false),
                ocrOperator = obj.optString("ocrOperator", ">="),
                ocrTargetValue = obj.optDouble("ocrTargetValue", 0.0),
                ocrCustomSuffixes = obj.optString("ocrCustomSuffixes", "k:1000,m:1000000,b:1000000000,к:1000,м:1000000,б:1000000000")
            )
        }
    }
}
