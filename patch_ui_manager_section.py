import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_anti_detect = """        val antiDetectSection = addSection("Анти-Детект", node.randomizeRadius > 0 || node.randomizePause > 0) { body ->"""

manager_section = """        // --- MANAGER SECTION ---
        var managerSection: View? = null
        if (node.type == NodeType.MANAGER) {
            managerSection = addSection("Настройки Менеджера", true) { body ->
                val desc = TextView(service).apply {
                    text = "Менеджер по очереди проверяет Триггеры. Если Триггер срабатывает, происходит переход к указанной Метке."
                    setTextColor(Color.LTGRAY)
                    setScaledTextSize(12f)
                    setPadding(0, 0, 0, 10)
                }
                body.addView(desc)
                
                val listContainer = LinearLayout(service).apply { orientation = LinearLayout.VERTICAL }
                body.addView(listContainer)
                
                fun renderRoutes() {
                    listContainer.removeAllViews()
                    for ((index, route) in node.managerRoutes.withIndex()) {
                        val row = LinearLayout(service).apply {
                            orientation = LinearLayout.HORIZONTAL
                            gravity = Gravity.CENTER_VERTICAL
                            setPadding(0, 5, 0, 5)
                            background = android.graphics.drawable.GradientDrawable().apply {
                                setColor(Color.parseColor("#333333"))
                                setCornerRadius(8f)
                            }
                        }
                        
                        val txt1 = TextView(service).apply { text = "Триггер № "; setTextColor(Color.WHITE) }
                        val checkEdit = EditText(service).apply {
                            inputType = InputType.TYPE_CLASS_NUMBER
                            setText(route.checkNodeId.toString())
                            setTextColor(Color.WHITE)
                            layoutParams = LinearLayout.LayoutParams(dpToPx(40), WindowManager.LayoutParams.WRAP_CONTENT)
                            addTextChangedListener(object: android.text.TextWatcher {
                                override fun afterTextChanged(s: android.text.Editable?) {
                                    s?.toString()?.toIntOrNull()?.let { route.checkNodeId = it }
                                }
                                override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
                                override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
                            })
                        }
                        val txt2 = TextView(service).apply { text = " ➔ Метка № "; setTextColor(Color.WHITE) }
                        val goEdit = EditText(service).apply {
                            inputType = InputType.TYPE_CLASS_NUMBER
                            setText(route.onSuccessGoToId.toString())
                            setTextColor(Color.WHITE)
                            layoutParams = LinearLayout.LayoutParams(dpToPx(40), WindowManager.LayoutParams.WRAP_CONTENT)
                            addTextChangedListener(object: android.text.TextWatcher {
                                override fun afterTextChanged(s: android.text.Editable?) {
                                    s?.toString()?.toIntOrNull()?.let { route.onSuccessGoToId = it }
                                }
                                override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
                                override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
                            })
                        }
                        val delBtn = Button(service).apply {
                            text = "X"
                            setTextColor(Color.RED)
                            setBackgroundColor(Color.TRANSPARENT)
                            setPadding(5, 5, 5, 5)
                            layoutParams = LinearLayout.LayoutParams(WindowManager.LayoutParams.WRAP_CONTENT, WindowManager.LayoutParams.WRAP_CONTENT)
                            setOnClickListener {
                                val mut = node.managerRoutes.toMutableList()
                                mut.removeAt(index)
                                node.managerRoutes = mut
                                renderRoutes()
                            }
                        }
                        
                        row.addView(txt1)
                        row.addView(checkEdit)
                        row.addView(txt2)
                        row.addView(goEdit)
                        row.addView(delBtn)
                        listContainer.addView(row)
                    }
                    
                    val addBtn = Button(service).apply {
                        text = "+ ДОБАВИТЬ УСЛОВИЕ"
                        setTextColor(Color.parseColor("#4CAF50"))
                        setBackgroundColor(Color.TRANSPARENT)
                        setOnClickListener {
                            val mut = node.managerRoutes.toMutableList()
                            mut.add(ManagerRoute(-1, -1))
                            node.managerRoutes = mut
                            renderRoutes()
                        }
                    }
                    listContainer.addView(addBtn)
                }
                
                renderRoutes()
                
                val fallbackLayout = LinearLayout(service).apply {
                    orientation = LinearLayout.HORIZONTAL
                    setPadding(0, 20, 0, 0)
                    gravity = Gravity.CENTER_VERTICAL
                }
                fallbackLayout.addView(TextView(service).apply { text = "Если ничего не совпало, идти к №: "; setTextColor(Color.WHITE) })
                val fallbackEdit = EditText(service).apply {
                    inputType = InputType.TYPE_CLASS_NUMBER
                    setText(node.nextNodeIdOnFail?.toString() ?: "")
                    hint = "(Стоп)"
                    setHintTextColor(Color.LTGRAY)
                    setTextColor(Color.WHITE)
                    layoutParams = LinearLayout.LayoutParams(dpToPx(60), WindowManager.LayoutParams.WRAP_CONTENT)
                    addTextChangedListener(object: android.text.TextWatcher {
                        override fun afterTextChanged(s: android.text.Editable?) {
                            val v = s?.toString()?.toIntOrNull()
                            if (v != null) node.nextNodeIdOnFail = v else node.nextNodeIdOnFail = null
                        }
                        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
                        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
                    })
                }
                fallbackLayout.addView(fallbackEdit)
                body.addView(fallbackLayout)
            }
        }
        
""" + find_anti_detect

content = content.replace(find_anti_detect, manager_section)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Manager section inserted")
