import os
import platform
import math

class BaseTool:
    """Bütün alətlər üçün baza sinfi."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, params: str) -> str:
        raise NotImplementedError("Hər bir alət execute() metodunu reallaşdırmalıdır.")

class CalculatorTool(BaseTool):
    """Sürətli və təhlükəsiz riyazi hesablamalar aləti."""
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Riyazi ifadələri və hesablamaları icra edir."
        )

    def execute(self, params: str) -> str:
        try:
            # Təhlükəsiz riyazi mühit
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            result = eval(params, {"__builtins__": None}, allowed_names)
            return f"🔢 Hesablama Nəticəsi: {result}"
        except Exception as e:
            return f"❌ Hesablama xətası: {str(e)}"

class SystemInfoTool(BaseTool):
    """Sistem haqqında ümumi məlumat toplayan alət."""
    def __init__(self):
        super().__init__(
            name="system_info",
            description="Əməliyyat sistemi və mühit haqqında statik məlumat qaytarır."
        )

    def execute(self, params: str) -> str:
        info = [
            f"OS: {platform.system()} {platform.release()}",
            f"Arxitektura: {platform.machine()}",
            f"Python Versiyası: {platform.python_version()}",
            f"Cari Qovluq: {os.getcwd()}"
        ]
        return "ℹ️ Sistem Məlumatı:\n" + "\n".join(f"  • {item}" for item in info)

class FileReaderTool(BaseTool):
    """Lokal mətn fayllarını oxumaq üçün alət."""
    def __init__(self):
        super().__init__(
            name="file_reader",
            description="Göstərilən mətn faylının məzmununu oxuyur."
        )

    def execute(self, params: str) -> str:
        filepath = params.strip()
        if not os.path.exists(filepath):
            return f"❌ Fayl tapılmadı: {filepath}"
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(1000) # İlk 1000 simvol
            return f"📄 Fayl Məzmunu ({filepath}):\n{content}"
        except Exception as e:
            return f"❌ Fayl oxunarkən xəta: {str(e)}"

class ToolManager:
    """Alətləri qeydiyyata alan və icra edən menecer."""
    def __init__(self):
        self.tools = {}
        # Standart alətləri qeydiyyatdan keçiririk
        self.register_tool(CalculatorTool())
        self.register_tool(SystemInfoTool())
        self.register_tool(FileReaderTool())

    def register_tool(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get_available_tools(self):
        return {name: tool.description for name, tool in self.tools.items()}

    def execute_tool(self, tool_name: str, params: str) -> str:
        if tool_name in self.tools:
            return self.tools[tool_name].execute(params)
        return f"❌ '{tool_name}' adlı alət tapılmadı."
