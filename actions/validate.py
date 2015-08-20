from lib.actions import BaseAction


class ValidateAction(BaseAction):
    def run(self, packerfile, cwd):
        if cwd:
            self.set_dir(cwd)

        p = self.packer(packerfile)
        return p.validate(syntax_only=False)
