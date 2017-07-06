# create a new repo
```shell
$ mkdir test-repo
$ cd test-repo
$ git init
```

# add a new file to git

```shell
# create a new file
$ echo "Using git" > readme.md
# chech status
$ git status
```

The output of above command would be similar for following. You can see that `readme.md` is an untracked file.

```shell
# add individual file to git
$ git add readme.md
# add all file to git
$ git add --all
# add only updated file to git
$ git add -u
```