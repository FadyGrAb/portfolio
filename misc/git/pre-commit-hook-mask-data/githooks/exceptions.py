from .utils import TextColorizer

colorize = TextColorizer()


class NoConfigurationFileFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        message = "Configuration file was not found. Run 'git-hooks init mask' to generate a template file in the following directory '.git/hooks/mask.toml'"
        return colorize.error(message)


class NotSupportedHook(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.illegal_hook = kwargs.get("hook", "")

    def __str__(self) -> str:
        message = f"Unsupported or wrong hook name ({self.illegal_hook}). Type `git-hooks list` to list supported hooks."
        return colorize.error(message)


class GitPathNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        message = "Can not find a .git directory in the current working directory. Make sure that you run the tool from your project's root directory and it's a valid git repo."
        return colorize.error(message)
