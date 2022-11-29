import os

class Terraform:

    def __init__(
        self,
        terraform_path: str = None,
    ) -> None:
        self.terraform_path = (terraform_path if terraform_path else "terraform")

    def apply(self, auto_approve=True, **kwargs):
        options = kwargs
        options['auto-approve'] = auto_approve
        #print(options)
        return self.cmd("apply", **options)

    def destroy(self):
        return self.cmd("destroy")

    def plan(self, **kwargs):
        options = kwargs
        return self.cmd("plan", **options)

    def cmd_string(self, cmd: str, **kwargs,):
        cmds = cmd.split()
        cmds = [self.terraform_path] + cmds

        for option, value in kwargs.items():
            if option == "var":
                for x in value:
                    cmds += [f'-var="{x}={value[x]}"']
            if option == "auto-approve":
                if value:
                    cmds += ["-auto-approve"]

        return cmds

    def cmd(self, cmd: str, **kwargs,):
        cmds = self.cmd_string(cmd, **kwargs)
        cmds = " ".join(cmds)

        os.system(f'cmd /c {cmds}')
        return print(f"Comando: {cmds}")

    def get_state(self):
        pass

