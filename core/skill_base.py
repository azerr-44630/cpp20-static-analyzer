class Skill:
    name = "base"
    description = ""
    risk = "low"  # low / medium / high

    def run(self, **kwargs):
        raise NotImplementedError
