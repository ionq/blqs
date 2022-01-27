# Contributing to Blqs

We welcome contributions to blqs.

First let's get the legal work out of the way. To contribute to blqs,
one needs to sign a Contributor License Agreement. This ensures that you
have agreed that you have the right to contribute the code you would like
to contribute. To receive IonQ's CLA, please contact @mjk or email opensource@ionq.com.

## Setup for development

In order to setup for development of blqs, we recommend the following workflow:

1. Fork the blqs repo.  Navigate to the top level of the blqs repo,
[https://github.com/ionq/blqs](https://github.com/ionq/blqs) and click
on the fork button to create a new fork. This creates a repo under your username
`https://github.com/USERNAME/blqs`.

2. Get a local copy of your fork.
```
git clone git@github.com:USERNAME/blqs.git
cd blqs
```

3. At this point you will have a remote in your forked git repo called `origin`. 
Add a remote called `upstream` which points to the original github repo.
```
git remote add upstream https://github.com/ionq/blqs.git
```
You can examine your remotes by running `git remote -v`.

4. Sync your local git with `upstream`:
```
git fetch upstream
git checkout main
git merge upstream/main
```

5. Create a virtual environment.  We recommend using `virtualenvwrapper` which
can be installed on linux machines using
```
apt-get install virtualenvwrapper
```
See [virtualenvwrapper docs](https://virtualenvwrapper.readthedocs.io/en/latest/)
for more details of isntalling virtualenvwrapper. Next create a virtualenv:
```
mkvirtualenv blqs
```
You should be in the environment `(blqs)` should appear on your command line.
If not run `activate blqs` to get into the virtual environment. Next install
requirements:
```
pip install -r blqs/requirements.txt
pip install -r blqs/ci/requirements-dev.txt
cat blqs_cirq/requirements.txt | grep -v blqs | xargs pip install
```
Finally add the blqs and blqs_cirq paths to your virtualenv
```
add2virtualenv blqs
add2virtualenv blqs_cirq
```

6. Check your install by running test, lint, and type checking:
```
./ci/check.sh

```


## Contributing a Pull Request

1. Make sure that you are in the virtual environment you created above (if not,
run `activate blqs` to get into the environment).

2. Sync your local main to the main on `upstream`:
```
git checkout main
git fetch upstream
git merge upstream/main
```

3. Create a local branch
```
git checkout -b yourbranchname
```
Now proceed to create your changes and commit them.  

4. Test your changes. Run
```
./ci/check.sh
```
To run tests, to run lint, check types, and check format. If your file is not
formatted, you can run `./ci/format.sh`.  If your code passes all test,
you are ready to subit a pull requestion.

5. Commit your changes, and push your branch to your fork at `origin`
```
git add .
git commit -m "My commit message"
git push origin yourbranchname
```

6. Navigate to `https://githbut.com/ionq/blqs` and you should see the option
to create a pull request from your forked branch.  Create this.  A reviewer
will review your code and may make suggestions for changes to your code.  You
can make those changes locally, commit them, and then push a new version of your
branch:
```
git add .
git commit -m "Describe changes"
git push origin yourbranchname
```

7. Once your PR is approved, it will be merged into the main branch. Congrats
on contributing to blqs!
