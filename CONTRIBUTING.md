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
1. So far not all information available via `eix -nv -x -e <package> --xml` are
   present in [package.schema.json]

Next, what you will need to do is:
1. Modify [JSON schema](metarepo2json/metarepo2json/schemas) (e.g. [kits.schema.json])
2. Modify the code: perhaps only getter changes in `*_utils.py` file(s) (e.g.
   for kits you will need to modify `get_kit()` in [utils])
3. Run/modify unit tests
4. For better example, study commit `bd287069701c82cc111b6b68521cf3f3b9ff91a5`


## HOWTO integrate with other plugins
**THIS IS A DRAFT, UNFORTUNATELY THIS IS STILL STANDALONE PROJECT THAT DOES NOT
USE OTHER PLUGINS**


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
[utils]: metarepo2json/metarepo2json/utils.py
