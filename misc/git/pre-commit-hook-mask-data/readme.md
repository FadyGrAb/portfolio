# PRE-COMMIT Git hook to mask user defined data before commits
> This is still a proof of concept. I've created it for educational purposes. Further work is still needed.
## Motivation:
When I commit code to public repos, I usually mask my sensitive data manually which is not practical nor scalable. So I needed a way to automate that at each git commit.

## How git hooks work:
When using git, it can execute scripts before and after some git commands. You can read all about them form [here](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).  

The ***pre-commit*** hook is run first, before you even type in a commit message. It’s used to inspect the snapshot that’s about to be committed.  

## Implementation details:
It's actually a straight forward process, you put the "***pre-commit***" script in your project's `.git/hooks` directory (usually at your project's root) accompanied by "***mask.toml***" config file which is basically telling the script *what* and *how* to mask your data with an optional *ignore* files list that won't be skipped from the checks. The script will check only the modified files.

## Setup and usage:
1. This is a **Python** scripts that needs Python installed on your system.  
2. Install **toml** package
```sh
pip install toml
```
(or you can use the requirements.txt in this repo `pip install -r requirements.txt`)  

3. Copy the "***pre-commit***" script and "***mask.toml***" to `.git/hooks`.  
4. Edit "***mask.toml***" as follows:
```toml
[show]                  # The sensitive data you want to mask.
12345678 = 4            # This will show only the last 4 characters i.e. "****5678"
asdirDkjcEDDcllsl = 0   # This will show 0 characters i.e. full mask "******************"

[ignore]                # The list of files to ignore
files=["ignoreme.html", "ignoreme2.html"]
```
You write your piece of sensitive data in the [show] table and specify how many characters you want to show from it (from the right). If you write 0, it will be a full mask.  

5. To activate the pre-commit script, just commit as usual (if there are untracked files, you should add them first to the git staging area `git add example.file`)
```sh
git commit -am "test commit"
```

## Example:
1. Create a new directory and CD into it
```sh
mkdir my-project
cd my-project
```
2. Run `git init` in this directory. Notice the new `.git` directory that is created.
3. Copy both the "***pre-commit***" script and "***mask.toml***" to `.git/hooks`. 
4. Edit the "***mask.toml***" as follows:
```toml
[show]
123456789104 = 4            
asdirDkjcEDDcllsllksjdfoiiEDSfkk = 0

[ignore]
files=[]
```
5. Add the following file (config.json) to your project's root directory:
```json
{
    "MyAcountNumber": "123456789104",
    "MySecreteKey": "asdirDkjcEDDcllsllksjdfoiiEDSfkk"
}
```
6. Run `git add .`
7. Commit your changes `git commit -m "mask commit"`
8. After the commit you will get the "[GIT HOOK PRE-COMMIT] Sensitive data masked" message the the (config.json) will be
```json
{
    "MyAcountNumber": "*********9104",
    "MySecreteKey": "********************************"
}
```
## Things to consider:
- This script can run on Windows as git (on windows) use a bash emulator. So the "SHEBANG" will be the path to your Python executable in this emulator. One way to find it is by starting ***Git bash*** from start menu and enter the `which python` command.
- This script lacks proper exception handling (for now) so please don't strain it too much :)
- To disable this script, just rename it or add a file extension to it.
- You can add the full path of a file to be ignored in the [ignore] table starting from your project's root directory.
- The `.git` directory isn't pushed to Github with a push, [check here](https://github.com/git-guides/git-push). So in theory, my sensitive data should be safe. But further research is needed.
## Further work to be done:
- [ ] Proper exception handling.
- [ ] Packaging.
- [ ] Testing.
- [ ] Add more features to mask.toml.



