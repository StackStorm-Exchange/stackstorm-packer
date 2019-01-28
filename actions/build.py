from lib.actions import BaseAction
import re


class BuildAction(BaseAction):

    def format_results(self, result_string, error=False):
        '''When returning the packer output information that are
        ansi characters that do not convert properly. Also when output
        the content to a string ansi escapes are added also. We need to
        convert these charaters if they exist and drop all the escapes
        so it outputs properly to stakcstorm.
        '''
        # ansi escape sequence
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

        # Drop all the ansi escapes and return the results
        result_string = ansi_escape.sub('', result_string)

        # Return a success or error status
        result_status = "success"
        if error:
            result_status = "error"

        # Return dictionary with status and result
        return {'status': result_status, 'result': result_string}

    def run(self, packerfile, cwd=None, exclude=None, only=None, variables=None,
            variables_file=None, parallel=True, debug=False, force=False):
        if cwd:
            self.set_dir(cwd)

        p = self.packer(packerfile, exc=exclude, only=only, variables=variables,
                        vars_file=variables_file)

        # If the packer build method fails. It only shows a small amount of data that
        # is not always helpful depending on where the error is. In the except block
        # we grab the whole output and return it.
        result = None
        try:
            p_result = p.build(parallel=parallel, debug=debug, force=force)
            result = self.format_results(p_result.stdout)
        except Exception as e:
            result = (False, self.format_results(e.stdout, True))  # pylint: disable=no-member

        return result
