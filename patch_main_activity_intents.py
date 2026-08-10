with open('app/src/main/java/com/example/autoclicker/MainActivity.kt', 'r') as f:
    content = f.read()

find_handle = """    private fun handleIntent(intent: Intent?) {
        when (intent?.action) {
            "ACTION_EXPORT_PROFILE" -> {
                // Read from static variable to avoid TransactionTooLargeException
                val name = intent.getStringExtra("profile_name") ?: "AutoClickerProfile"
                val sfIntent = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                    addCategory(Intent.CATEGORY_OPENABLE)
                    type = "application/json"
                    putExtra(Intent.EXTRA_TITLE, "$name.json")
                }
                startActivityForResult(sfIntent, REQ_EXPORT)
            }
            "ACTION_IMPORT_PROFILE" -> {
                val sfIntent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                    addCategory(Intent.CATEGORY_OPENABLE)
                    type = "application/json"
                }
                startActivityForResult(sfIntent, REQ_IMPORT)
            }
            "ACTION_SHARE_PROFILE" -> {
                val data = pendingExportData
                val title = intent.getStringExtra("profile_name") ?: "AutoClicker Profile"
                try {
                    val sendIntent = Intent(Intent.ACTION_SEND).apply {
                        type = "text/plain"
                        putExtra(Intent.EXTRA_TEXT, data)
                        putExtra(Intent.EXTRA_TITLE, title)
                    }
                    startActivity(Intent.createChooser(sendIntent, "Поделиться сценарием"))
                } catch (e: Exception) {
                    android.widget.Toast.makeText(this, "Ошибка при отправке сценария", android.widget.Toast.LENGTH_LONG).show()
                }
            }
            Intent.ACTION_VIEW -> {
                intent.data?.let { uri ->
                    try {
                        val content = contentResolver.openInputStream(uri)?.bufferedReader().use { it?.readText() }
                        if (content != null) {
                            val instance = AutoClickService.instance
                            if (instance != null) {
                                instance.loadProfileFromJson(content, append = false)
                                android.widget.Toast.makeText(this, "Профиль успешно загружен", android.widget.Toast.LENGTH_SHORT).show()
                            } else {
                                pendingImportData = content
                                android.widget.Toast.makeText(this, "Включите службу Автокликера для импорта профиля", android.widget.Toast.LENGTH_LONG).show()
                            }
                        }
                    } catch (e: Exception) {
                        e.printStackTrace()
                        android.widget.Toast.makeText(this, "Ошибка загрузки: неверный формат файла", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }
            }
        }
    }"""

repl_handle = """    private fun handleIntent(intent: Intent?) {
        val action = intent?.action ?: return
        intent.action = null // Clear action so we don't trigger it again on rotation
        
        when (action) {
            "ACTION_EXPORT_PROFILE" -> {
                val name = intent.getStringExtra("profile_name") ?: "AutoClickerProfile"
                val sfIntent = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                    addCategory(Intent.CATEGORY_OPENABLE)
                    type = "application/json"
                    putExtra(Intent.EXTRA_TITLE, "$name.json")
                }
                startActivityForResult(sfIntent, REQ_EXPORT)
            }
            "ACTION_IMPORT_PROFILE" -> {
                val sfIntent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                    addCategory(Intent.CATEGORY_OPENABLE)
                    type = "application/json"
                }
                startActivityForResult(sfIntent, REQ_IMPORT)
            }
            "ACTION_SHARE_PROFILE" -> {
                val data = pendingExportData
                val title = intent.getStringExtra("profile_name") ?: "AutoClicker Profile"
                try {
                    val cachePath = java.io.File(cacheDir, "shared_profiles")
                    cachePath.mkdirs()
                    val newFile = java.io.File(cachePath, "${title.replace(" ", "_")}.json")
                    newFile.writeText(data ?: "{}")
                    
                    val contentUri = androidx.core.content.FileProvider.getUriForFile(this, "com.example.autoclicker.fileprovider", newFile)
                    
                    val sendIntent = Intent(Intent.ACTION_SEND).apply {
                        type = "application/json"
                        putExtra(Intent.EXTRA_STREAM, contentUri)
                        putExtra(Intent.EXTRA_TITLE, title)
                        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    }
                    startActivity(Intent.createChooser(sendIntent, "Поделиться сценарием"))
                } catch (e: Exception) {
                    e.printStackTrace()
                    android.widget.Toast.makeText(this, "Ошибка при отправке сценария", android.widget.Toast.LENGTH_LONG).show()
                }
            }
            Intent.ACTION_VIEW -> {
                intent.data?.let { uri ->
                    try {
                        val fileContent = contentResolver.openInputStream(uri)?.bufferedReader().use { it?.readText() }
                        if (fileContent != null) {
                            val instance = AutoClickService.instance
                            if (instance != null) {
                                instance.loadProfileFromJson(fileContent, append = false)
                                android.widget.Toast.makeText(this, "Профиль успешно загружен", android.widget.Toast.LENGTH_SHORT).show()
                            } else {
                                pendingImportData = fileContent
                                android.widget.Toast.makeText(this, "Включите службу Автокликера для импорта профиля", android.widget.Toast.LENGTH_LONG).show()
                            }
                        }
                    } catch (e: Exception) {
                        e.printStackTrace()
                        android.widget.Toast.makeText(this, "Ошибка загрузки: неверный формат файла", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }
            }
        }
    }"""

content = content.replace(find_handle, repl_handle)

with open('app/src/main/java/com/example/autoclicker/MainActivity.kt', 'w') as f:
    f.write(content)
print("MainActivity Intents patched")
