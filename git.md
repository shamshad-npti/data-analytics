# Create a New Repo
```shell
$ mkdir test-repo
$ cd test-repo
$ git init
```

# Add a New File to Git

```shell
# create a new file
$ echo "Using git" > readme.md
# chech status
$ git status
```

The output of above command would be similar for following. You can see that `readme.md` is an untracked file.

```
Untracked files:
  (use "git add <file>..." to include in what will be committed)

	git.md
	----
	----
```

```shell
# add individual file to git
$ git add readme.md
# add all file to git
$ git add --all
# add only updated file to git
$ git add -u
```

### Use `commit` command to commit a change

```shell
$ git commit -m "Initial commit"
```

### See commit log with `log` command

```shell
$ git log
```

