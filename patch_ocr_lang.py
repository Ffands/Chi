import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

find_analyzer = """    private fun getHuaweiAnalyzer(): com.huawei.hms.mlsdk.text.MLTextAnalyzer {
        synchronized(ocrLock) {
            if (mlTextAnalyzer != null) return mlTextAnalyzer!!
            com.huawei.hms.mlsdk.common.MLApplication.getInstance().apiKey = "dummy_api_key_for_local_use_only"
            val setting = com.huawei.hms.mlsdk.text.MLLocalTextSetting.Factory()
                .setOCRMode(com.huawei.hms.mlsdk.text.MLLocalTextSetting.OCR_DETECT_MODE)
                .setLanguage("ru")
                .create()
            mlTextAnalyzer = com.huawei.hms.mlsdk.MLAnalyzerFactory.getInstance().getLocalTextAnalyzer(setting)
            return mlTextAnalyzer!!
        }
    }"""

repl_analyzer = """    private var mlTextAnalyzerLang: String = "ru"
    
    private fun getHuaweiAnalyzer(lang: String): com.huawei.hms.mlsdk.text.MLTextAnalyzer {
        synchronized(ocrLock) {
            val hLang = if (lang == "eng") "en" else "ru"
            if (mlTextAnalyzer != null && mlTextAnalyzerLang == hLang) return mlTextAnalyzer!!
            if (mlTextAnalyzer != null) mlTextAnalyzer!!.stop()
            
            com.huawei.hms.mlsdk.common.MLApplication.getInstance().apiKey = "dummy_api_key_for_local_use_only"
            val setting = com.huawei.hms.mlsdk.text.MLLocalTextSetting.Factory()
                .setOCRMode(com.huawei.hms.mlsdk.text.MLLocalTextSetting.OCR_DETECT_MODE)
                .setLanguage(hLang)
                .create()
            mlTextAnalyzerLang = hLang
            mlTextAnalyzer = com.huawei.hms.mlsdk.MLAnalyzerFactory.getInstance().getLocalTextAnalyzer(setting)
            return mlTextAnalyzer!!
        }
    }"""

if find_analyzer in content:
    content = content.replace(find_analyzer, repl_analyzer)
    
    # Update calls
    content = content.replace(
        "val analyzer = getHuaweiAnalyzer()",
        "val analyzer = getHuaweiAnalyzer(node.targetLanguage)"
    )
    
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("OCR Language patched")
else:
    print("Could not find getHuaweiAnalyzer!")
