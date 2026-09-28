from core.skill_base import Skill
from brain.tool_manager import ToolManager

_tm = ToolManager()

class WebSearch(Skill):
    name = "web_search"
    description = "İnternetdə canlı axtarış aparır"
    risk = "low"

    def run(self, query, **kwargs):
        return _tm.execute_tool("web_search", query)
