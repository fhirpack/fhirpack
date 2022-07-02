# Contributing

Welcome to `fhirpack` contributor\'s guide.

This document focuses on getting any potential contributor familiarized
with the development processes, but [other kinds of
contributions](https://opensource.guide/how-to-contribute) are also
appreciated.

If you are new to using [git](https://git-scm.com) or have never
collaborated in a project previously, please have a look at
[contribution-guide.org](https://www.contribution-guide.org/). Other
resources are also listed in the excellent [guide created by
FreeCodeCamp](https://github.com/FreeCodeCamp/how-to-contribute-to-open-source)[^1].

Please notice, all users and contributors are expected to be **open,
considerate, reasonable, and respectful**. When in doubt, [Python
Software Foundation\'s Code of
Conduct](https://www.python.org/psf/conduct/) is a good reference in
terms of behavior guidelines.

Issue Reports
-------------

If you experience bugs or general issues with `fhirpack`, please have a
look on the [issue
tracker](https://gitlab.com/fhirpack/main/-/issues). If you
don\'t see anything useful there, please feel free to fire an issue
report.

> **_NOTE:_** Please don\'t forget to include the closed issues in your search. Sometimes a solution was already reported, and the problem is considered

New issue reports should include information about your programming
environment (e.g., operating system, Python version) and steps to
reproduce the problem. Please try also to simplify the reproduction
steps to a very minimal example that still illustrates the problem you
are facing. By removing other factors, you help us to identify the root
cause of the issue.

Documentation Improvements
--------------------------

You can help improve `fhirpack` docs by making them more readable and
coherent, or by adding missing information and correcting mistakes.

`fhirpack` documentation uses
[Sphinx](https://www.sphinx-doc.org/en/master/) as its main
documentation compiler. This means that the docs are kept in the same
repository as the project code, and that any documentation update is
done in the same way was a code contribution.

When working on documentation changes in your local machine, you can
compile them using `tox`:

```
tox -e docs
```

and use Python\'s built-in web server for a preview in your web browser
(`http://localhost:8000`):

```
python3 -m http.server --directory 'docs/_build/html'
```

Code Contributions
------------------

`fhirpack` is build around the `PACK` class which uses a custom subclass of
`pandas.DataFrame`, called `Frame`, as the main underlying
datastructure. Upon connecting to a server, the workflow follows the ETL
principle. In general, methods that extract FHIR resources can be found
inside the `extraction` directory. These methods expect a list of
either `fhirpy` resources, `fhirpy` references or FHIR-ID strings as
input. Alternatively, the methods can operate on a `Frame` object
according to the
[mixin](https://www.pythontutorial.net/python-oop/python-mixin/)
pattern. In this case, no other input is expected. All extraction
methods return `Frame` objects which can be used by the Transformer for
data manipulation or Loader for uploading.

You can use Jupyter, JupyterLab or VSCode\'s Jupyter Plugin to use and
improve `usage.py` and `minimal.py`. However, keep in mind to not upload
notebook outputs as they bloat the files and are irrelevant to the
reader. To prevent that, execute:

```
echo -e '[filter "strip-notebook-output"]\n\tclean = jupyter nbconvert \
--ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR' \
>> .git/config
```

within the repository. That line defines a clean for Jupyter notebooks
that git can then use for all `*.ipynb`.

### Submit an issue

Before you work on any non-trivial code contribution it\'s best to first
create a report in the [issue
tracker](https://gitlab.com/fhirpack/main/-/issues) to start a
discussion on the subject. This often provides additional considerations
and avoids unnecessary work.

### Create an environment

Before you start coding, we recommend creating an isolated [virtual
environment](https://realpython.com/python-virtual-environments-a-primer/)
to avoid any problems with your installed Python packages. This can
easily be done via either `virtualenv`:

```
virtualenv <PATH TO VENV>
source <PATH TO VENV>/bin/activate
```

or [Miniconda](https://docs.conda.io/en/latest/miniconda.html):

```
conda create -n fhirpack python=3.9.6 six virtualenv pytest pytest-cov
conda activate fhirpack
```

or [Pipenv](https://pipenv.pypa.io/en/latest/):

```
pipenv install fhirpack
pipenv 
```

### Clone the repository

1.  Create an user account on GitLab if you do not already have one.

2.  Fork the project
    [repository](https://gitlab.com/fhirpack/main): click on
    the *Fork* button near the top of the page. This creates a copy of
    the code under your account on GitLab.

3.  Clone this repository to your local disk from GitLab with:

    ```
    git clone https://gitlab.com/fhirpack/main.git
    ```

    or from GitHub with:

    ```
    git clone https://github.com/fhirpack/main.git
    ```

1.  You should run:

    ```
    pip install -U pip setuptools -e .
    ```

    to be able to import the package under development in the Python
    REPL.

2.  Verify you can run tests and build `fhirpack`:

    ```
    tox -e; tox -e build; tox -e clean
    ```

### Dependencies

This projetc relies on the followin python packages.

### Implement your changes

1.  Create a branch to hold your changes:

    ```
    git checkout -b my-feature
    ```

    and start making changes. Never work on the main branch!

2.  Start your work on this branch. Don\'t forget to add
    [docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
    to new functions, modules and classes, especially if they are part
    of public APIs.

3.  Test your Improvements:

    ```
    pytest -s --use-running-containers --docker-compose-no-build --pyargs fhirpack tests 
    tox
    ```

4.  Add yourself to the list of contributors in `AUTHORS.rst`.

5.  When you're done editing, do:

    ```
    git add <MODIFIED FILES>
    git commit
    ```

    to record your changes in [git](https://git-scm.com).

    > **_NOTE:_** Don\'t forget to add unit tests and documentation in case your contribution adds an additional feature and is not just a bugfix. Moreover, writing a [descriptive commit message](https://chris.beams.io/posts/git-commit) is highly recommended.

6.  Please check that your changes don\'t break any unit tests with:

    ```
    tox
    ```

    (after having installed `tox` with `pip install tox` or `pipx`).

    You can also use `tox` to run several other pre-configured tasks
    in the repository. Try `tox -av` to see a list of the available
    checks.

### Submit your contribution

1.  If everything works fine, push your local branch to GitLab with:

    ```
    git push -u origin my-feature
    ```

2.  Go to the web page of your fork and click \"Create merge request\" to
    send your changes for review.

### Troubleshooting

The following tips can be used when facing problems to build or test the
package:

1.  Make sure to fetch all the tags from the upstream
    [repository](https://gitlab.com/fhirpack/main). The
    command `git describe --abbrev=0 --tags` should return the version
    you are expecting. If you are trying to run CI scripts in a fork
    repository, make sure to push all the tags. You can also try to
    remove all the egg files or the complete egg folder, i.e., `.eggs`,
    as well as the `*.egg-info` folders in the `src` folder or
    potentially in the root of your project.

2.  Sometimes `tox` misses out when new dependencies are added,
    especially to `setup.cfg` and `docs/requirements.txt`. If you find
    any problems with missing dependencies when running a command with
    `tox`, try to recreate the `tox` environment using the `-r` flag.
    For example, instead of:

    ```
    tox -e docs
    ```

    Try running:

    ```
    tox -r -e docs
    ```

3.  Make sure to have a reliable `tox` installation that uses the
    correct Python version (3.9). When in doubt you can run:

    ```
    tox --version
    # OR
    which tox
    ```

    If you have trouble and are seeing weird errors upon running
    `tox`, you can also try to create a dedicated [virtual
    environment](https://realpython.com/python-virtual-environments-a-primer/)
    with a `tox` binary freshly installed. For example:

    ```
    virtualenv .venv
    source .venv/bin/activate
    .venv/bin/pip install tox
    .venv/bin/tox -e all
    ```

4.  [Pytest can drop
    you](https://docs.pytest.org/en/stable/how-to/failures.html#using-python-library-pdb-with-pytest)
    in an interactive session in the case an error occurs. In order to
    do that you need to pass a `--pdb` option (for example by running
    `tox -- -k <NAME OF THE FALLING TEST> --pdb`). You can also setup
    breakpoints manually instead of using the `--pdb` option.

Maintainer tasks
----------------

### Releases

If you are part of the group of maintainers and have correct user
permissions on [PyPI](https://pypi.org/), the following steps can be
used to release a new version for `fhirpack`:

1.  Make sure all unit tests are successful.
2.  Tag the current commit on the main branch with a release tag, e.g.,
    `v1.2.3`.
3.  Push the new tag to the upstream
    [repository](https://gitlab.com/fhirpack/main), e.g.,
    `git push upstream v1.2.3`
4.  Clean up the `dist` and `build` folders with `tox -e clean` (or
    `rm -rf dist build`) to avoid confusion with old builds and Sphinx
    docs.
5.  Run `tox -e build` and check that the files in `dist` have the
    correct version (no `.dirty` or [git](https://git-scm.com) hash)
    according to the [git](https://git-scm.com) tag. Also check the
    sizes of the distributions, if they are too big (e.g., \> 500KB),
    unwanted clutter may have been accidentally included.
6.  Run `tox -e publish -- --repository pypi` and check that everything
    was uploaded to [PyPI](https://pypi.org/) correctly.

[^1]: Even though, these resources focus on open source projects and
    communities, the general ideas behind collaborating with other
    developers to collectively create software are general and can be
    applied to all sorts of environments, including private companies
    and proprietary code bases.
