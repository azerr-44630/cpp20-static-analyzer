from core.skill_base import Skill

class Hello(Skill):
    name = "hello"
    description = "Test skill"
    risk = "low"

    def run(self, **kwargs):
        return "Skill sistemi işləyir"
