from core.skill_base import Skill
from brain.tool_manager import ToolManager

_tm = ToolManager()

class WebFetch(Skill):
    name = "web_fetch"
    description = "Verilən URL-in səhifə məzmununu çəkir"
    risk = "low"

    def run(self, url, **kwargs):
        return _tm.execute_tool("web_fetch", url)
