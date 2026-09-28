from core.skill_base import Skill
from brain.tool_manager import ToolManager

_tm = ToolManager()

class RepoInspect(Skill):
    name = "repo_inspect"
    description = "GitHub reposunun README/fayl strukturunu oxuyur"
    risk = "low"

    def run(self, repo_path, **kwargs):
        return _tm.execute_tool("repo_inspect", repo_path)
