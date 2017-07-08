Git Basics
---

### Create a New Repo
```shell
$ mkdir test-repo
$ cd test-repo
$ git init
```

### Add a New File to Git

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

### Create a New Branch
```shell
# create a branch name "dev"
$ git checkout dev
```

### List all Branches
```shell
$ git branch
```

### Switch to a Specific Branch
```shell
# switch to master branch
$ git checkout master
```

### Creating a Branch from Existing Branch
```shell
# create branch feature-32 off dev
$ git chechout -b feature-32 dev
```

```
$ echo "Dfd" | git hash-object -w --stdin

$ git cat-file -p hash-value
               -t hash-value

$ git update-index --add --cachenfo 100644 hash fielname
$ git write-tree

$ git commit-tree
```

# Git Advanced Tutorial
* Commit By Hand
* Rebase
* Interactive Rebase
* Pull Requests
* External Diff Tools
* Advanced Logging
* Reflog
* Reset

### Commit By Hand

1. Create and Initialize a repo

```shell
$ mkdir git-advanced; cd git-advanced
$ git init
# hash simple text in git
# when following command execute you will see a hash in console
# let that hash be 45e0a4bc615eb1dac06f08043c1e1efa75311baf
$ echo "Git In Depth" | git hash-object -w --stdin
45e0a4bc615eb1dac06f08043c1e1efa75311baf

$ git cat-file -p 45e0a
Git In Depth

# update-index will register file content in the working tree
# to the index
$ git update-index --add --cacheinfo 100644 45e0a danger.txt

# Now try git status
$ git status
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

	new file:   danger.txt

Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	deleted:    danger.txt

# Use write-tree to create a tree object from the current index
```