from core.skill_base import Skill
from brain.tool_manager import ToolManager

_tm = ToolManager()

class GithubOsint(Skill):
    name = "github_osint"
    description = "GitHub istifadəçi profilini təhlil edir"
    risk = "low"

    def run(self, username, **kwargs):
        return _tm.execute_tool("github_osint", username)
