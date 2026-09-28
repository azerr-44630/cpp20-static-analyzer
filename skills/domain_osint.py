from core.skill_base import Skill
from brain.tool_manager import ToolManager

_tm = ToolManager()

class DomainOsint(Skill):
    name = "domain_osint"
    description = "Domen/IP üzrə server, başlıq və status kodu analizi"
    risk = "medium"

    def run(self, domain, **kwargs):
        return _tm.execute_tool("domain_osint", domain)
