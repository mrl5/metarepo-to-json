# For contributors
This project uses **P**lugin **O**riented **P**rogramming paradigm by
incorporating [SaltStack pop library]

I decided to use `git-flow` branching model which is nicely described here:
https://nvie.com/posts/a-successful-git-branching-model/

## TL;DR:
0. fork the repo and `git clone` your fork
1. use `develop` branch:
```
git checkout develop
```
2. then create your own branch (e.g. `feature/STH` or `bugfix/STH`) - keep `STH`
   short, commit messages are for details:
```
git checkout -b feature/more-ebuild-details
```
3. after changes do the PR into the `develop` branch


## HUBs, POPs, WTF?
0. `pop` book: https://pop-book.readthedocs.io/en/latest/
1. `pop` tutorial: https://pop.readthedocs.io/en/latest/tutorial/quickstart.html
2. `pop-config`: https://pop-config.readthedocs.io/en/latest/topics/quickstart.html#the-config-dictionary
3. `pop` patterns: https://pop.readthedocs.io/en/latest/topics/sub_patterns.html


## Kudos box
1. [Daniel Robbins] a [Funtoo Linux] BDFL: for sharing the knowledge, external
POP references and a codebase of [funtoo-metatools]


## Dev dependencies
```
pip install -r requirements-dev.txt
```


## Unit tests
1. Location: [tests/](tests)
2. Howto run tests:
```
export PYTHONPATH=./
pytest
```


## Kit/Cat/Package does not provide all needed info
Feel free to do a PR:
1. So far not all information available in `ego kit` are present in [kits.schema.json]
2. So far not all information available via `eix -nv -x -e <package> --xml` are
   present in [package.schema.json]

Next, what you will need to do is:
1. Modify [JSON schema](metarepo2json/metarepo2json/schemas) (e.g. [kits.schema.json])
2. Modify the code: perhaps only getter changes in `*_utils.py` file(s) (e.g.
   for kits you will need to modify `get_kit()` in [kits utils])
3. Run/modify unit tests
4. For better example, study this commit: `#todo`


## HOWTO integrate with other plugins
In this example we will integrate with `pkgtools` plugin which is inside
[funtoo-metatools] Git project

1. Add Git submodule:
```
git submodule add https://code.funtoo.org/bitbucket/scm/~drobbins/funtoo-metatools.git
cd metarepo2json/
ln -s ../funtoo-metatools/pkgtools/ pkgtools
cd ..
git add metarepo2json/
```
2. Add new plugin into `DYNE` in `conf.py`
3. For better example, study this commit: `#todo`


## HOWTO integrate with other Git webservices
For now only `github` and `code.funtoo.org` are supported. To introduce new git
webservice check `supported_git_webservices` variable in `get_raw_file_uri()`
function from [kits utils]

Make sure to write a unit tests, there are examples in `test_*.py` files from
[tests/](tests) directory


[SaltStack pop library]: https://gitlab.com/saltstack/pop/pop
[Daniel Robbins]: https://github.com/danielrobbins
[Funtoo Linux]: https://www.funtoo.org
[funtoo-metatools]: https://code.funtoo.org/bitbucket/users/drobbins/repos/funtoo-metatools/browse
[kits.schema.json]: metarepo2json/metarepo2json/schemas/kit.schema.json
[package.schema.json]: metarepo2json/metarepo2json/schemas/package.schema.json
[kits utils]: metarepo2json/metarepo2json/kits/utils.py
