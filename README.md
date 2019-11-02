
# ***_Guide to Git***

## Getting Started

Follow these one-time steps to get started.

1. Fork the original repo
![Fork](pics/fork.PNG)

2. Clone in the repo (replacing `USERNAME` with yours):
```
git clone https://github.com/USERNAME/intravideo_search.git
```

3. Add a reference to the master branch of the remote repo called upstream:
```
git remote add upstream https://github.com/suchak1/intravideo_search.git
```

## Contributing

Note that each pull request should be a self-contained small change.
For example,
- implementing one function
- fixing a bug
- writing test cases for one function
- updating a document
- changing the build pipeline

In order to contribute to the repo, one should follow this consistent step-by-step process.

1. Switch to your local master branch:
	```
	git checkout master
	```

2. Pull in any changes from remote master
	```
	git pull upstream master
	```

3. Create a new branch to house your proposed changes:
	```
	git checkout -b TYPE/short-descript-name
	```

   where `short-descript-name` is the name of the change you are making.

    For example: `add_gui_render` for a branch implementing the render function in the GUI class.

    Also, `TYPE` is the type of change.

    For example, `TYPE` = one of the following:
    - `doc` - documentation related change
    - `feature` - new implementation
    - `bug` - fix existing implementation
    - `test` - test case addition or change


	So, the full branch name would be: `feature/add_gui_render`.
    The command would be: `git checkout -b feature/add_gui_render`

4. Implement your local changes and save.
5. (Optional Step)
	Add any files you want to ignore to the `.gitignore`.
	Secret credentials or local debugging files fall in this category.
6. Check the tracking status of all the files in the repo with
	```
	git status
	```
	Note the result: if there are any files in the Untracked Files category that you would like added to the repo, then `git add` them in the next step.
7. (Optional Step)
	Add files that are brand new with `git add FILEPATH`.
	Similarly, you can remove files from the repo with `git rm FILEPATH`
	If you are simply modifying existing files, then don't worry about adding them explicitly here. That will be handled in the next step.
8. Now, commit with
	```
	git commit -am "MESSAGE"`
	```
	where `MESSAGE` is a descriptive message about the change.

	The `-am` flag will automatically add modified files (files that already exist in the repo).  
	Don't be afraid to commit as much as possible. In fact, committing often makes it easier to track down specific commits that introduce bugs and potential alternative code routes.
9. When you're ready to make a pull request and show others your work, use
	```
	git push
	```
	This will probably give you an error message and a new command mentioning
	`--set-upstream` . Run this new command instead to fix the error.
10. Visit the link in the output of the previous command, and follow the PR template to submit a pull request. Once you click save, you will be able to see how your changes fare against the existing test suite.

	You can also request other group members to review your work.

	Once you
    - fill in the Proposed Changes section in the PR
	- incorporate in others suggestions
	- gain approval from at least 2 other group members
	- pass all tests

	you can hit "Squash and Merge."


***Congrats!*** You have now made a commit in the remote `master` branch.


## Notes

Atom or VSCode is recommended as an IDE.

Again, to pull in recent changes from the remote master branch the command is

```
git pull upstream master
````

Sometimes, recent changes in remote master will affect your work. In this case, you will run into merge conflicts errors that must be resolved. This is because git doesn't know whether you want to keep the changes in your code or replace them with someone else's (latest code from remote master).

In Atom, a merge conflict looks like this:
![](pics/conflict.PNG)

Just click `Use me` next to `HEAD` (or maybe your branch name) if you would like to keep your code or `Use me` next to `master` if you would like to replace your conflicting code with the latest from remote master.

Other IDEs / text editors may not be as intuitive.
