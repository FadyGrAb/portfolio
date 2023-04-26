import pathlib
import shutil
import subprocess
import sys

import click

from ..exceptions import *
from ..mask import MaskGitHook
from ..utils import TextColorizer


def get_current_repo_git_path() -> pathlib.Path:
    cmd_git_dir = (
        subprocess.run("git rev-parse --show-toplevel", capture_output=True, shell=True)
        .stdout.decode("utf8")
        .strip()
    )
    return pathlib.Path(cmd_git_dir) / ".git"


supported_hooks = ["mask"]


@click.group()
def cli():
    """A CLI tool to create a data masking git hook to mask the user's
    predefined sensitive data before the git commit.
    """
    pass


@cli.command()
@click.argument("hook")
def init(hook: str) -> None:
    """Adds the hook and template config to '.git/hooks'.
    Currently the 'hook' arg can take only 'mask' value.
    """
    try:
        if hook.lower() not in supported_hooks:
            raise NotSupportedHook(hook=hook)

        templates_dir = pathlib.Path(__file__).parents[1] / "templates"
        git_dir = get_current_repo_git_path()
        print("git directory ", git_dir)
        hooks_dir = git_dir / "hooks"

        if not git_dir.exists():
            raise GitPathNotFound()

        hooks_dir.mkdir(exist_ok=True)

        if hook.lower() == "mask":
            # pre-commit file
            pre_commit_script = hooks_dir / "pre-commit"
            code = [
                f"#!{str(pathlib.Path(sys.executable))}\n",
                "import subprocess\n",
                "subprocess.run('git-hooks mask', shell=True)",
            ]
            with pre_commit_script.open(mode="w") as script:
                script.writelines(code)
            print(TextColorizer.info(f"pre-commit is created in {hooks_dir}"))

            # mask.toml file
            config_toml = templates_dir / "mask.toml"
            shutil.copy2(config_toml, hooks_dir)
            print(TextColorizer.info(f"mask.toml is created in {hooks_dir}"))

            print(TextColorizer.success("Mask git hook is initiated successfully."))

    except NotSupportedHook as e:
        print(e)
    except GitPathNotFound as e:
        print(e)
    except Exception as e:
        print(e)


@cli.command()
def mask():
    """Executes the 'mask' hook"""
    masker = MaskGitHook(get_current_repo_git_path())
    masker.mask()


@cli.command()
def list():
    """Lists currently supported git hooks"""
    for hook in supported_hooks:
        print(hook)


if __name__ == "__main__":
    cli()
