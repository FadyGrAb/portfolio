from setuptools import setup, find_packages
import pathlib
from githooks.utils import TextColorizer

template_files = [str(file) for file in pathlib.Path("githooks/templates").iterdir()]


def show_info() -> None:
    print(
        TextColorizer.success(
            "Installation successful. Please type 'git-hooks --help` for more details."
        )
    )


setup(
    name="git-hooks",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "toml", "colorama"],
    data_files=[("", template_files)],
    entry_points={
        "console_scripts": ["git-hooks = githooks.scripts.git_hooks:cli"],
    },
)
