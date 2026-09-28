from core.skill_base import Skill
from brain.tool_manager import ToolManager

_tm = ToolManager()

class SystemInfo(Skill):
    name = "system_info"
    description = "Cihazın sistem məlumatlarını göstərir"
    risk = "low"

    def run(self, **kwargs):
        return _tm.execute_tool("system_info", "")
