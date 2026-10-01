from core.skill_base import Skill
from skills.cpp_analyzer.auto_fixer import AutoFixer

class CppFix(Skill):
    name = "cpp_fix"
    description = "C++ kodunda aşkarlanan raw pointer massivlərini std::vector-ə avtomatik çevirir (dry-run defolt)"
    risk = "medium"

    def run(self, directory=".", dry_run=True, **kwargs):
        fixer = AutoFixer(dry_run=dry_run)
        fixer.run_fixes(directory)
        return f"'{directory}' üzərində {'DRY-RUN (heç nə dəyişmədi)' if dry_run else 'real düzəliş'} tamamlandı."
