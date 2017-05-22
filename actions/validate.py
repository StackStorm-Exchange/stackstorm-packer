from lib.actions import BaseAction


class ValidateAction(BaseAction):
    def run(self, packerfile, cwd=None, exclude=None, only=None, variables=None,
            variables_file=None, syntax_only=False):
        if cwd:
            self.set_dir(cwd)

        p = self.packer(packerfile, exc=exclude, only=only, variables=variables,
                        vars_file=variables_file)
        return p.validate(syntax_only=syntax_only)
