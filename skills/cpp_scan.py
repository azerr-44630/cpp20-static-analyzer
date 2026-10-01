from core.skill_base import Skill
from skills.cpp_analyzer.ast_engine import CppASTAnalyzer

class CppScan(Skill):
    name = "cpp_scan"
    description = "C++ kodunda təhlükəsizlik pattern-lərini (strcpy, malloc, raw pointer və s.) skan edir"
    risk = "low"

    def run(self, directory=".", **kwargs):
        analyzer = CppASTAnalyzer()
        issues = analyzer.analyze_directory(directory)
        if not issues:
            return f"'{directory}' qovluğunda problem tapılmadı."
        lines = [f"### C++ Təhlükəsizlik Skanı ({directory}):"]
        for issue in issues:
            lines.append(f"- [{issue['type']}] {issue['file']}:{issue['line']} -> {issue['code']}")
        return "\n".join(lines)
