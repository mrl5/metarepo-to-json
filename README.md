# metarepo-to-json
export [Funtoo meta-repo](https://github.com/funtoo/meta-repo) to JSON

## Getting started
0. Clone the repo
1. Create python3 virtualenv:
```
VENV_DIR="$HOME/.my_virtualenvs/metarepo2json"
mkdir -p "${VENV_DIR}"
python3 -m venv "${VENV_DIR}"
```
2. Switch to new virtualenv:
```
source "${VENV_DIR}/bin/activate"
```
3. Install requirements:
```
cd metarepo-to-json/
python3 setup.py install
```
4. **Export PYTHONPATH**:
```
export PYTHONPATH=./
```
5. RTFM :D
```
bin/get_kits_json.py --help
```
6. Run scripts:
```
bin/get_kits_json.py -s web
bin/get_kits_json.py -s fs
bin/get_kits_json.py
```
```
bin/get_categories_json.py -k browser-kit
bin/get_categories_json.py -s web --repo-web https://code.funtoo.org/bitbucket/projects/AUTO/repos/browser-kit/browse
bin/get_categories_json.py -s web --branch 3.34-prime --repo-web https://code.funtoo.org/bitbucket/projects/INDY/repos/gnome-kit/browse
bin/get_categories_json.py -s web --repo-web https://github.com/funtoo/browser-kit --commit 95b2af11f842b627943988f3c37dad5a09b3e9bd
bin/get_categories_json.py -s fs -k media-kit
bin/get_categories_json.py -s fs -k core-kit -c d68adcb7a1463bcf5be7127dfffe448fcf503276
```
```
bin/get_catpkgs_json.py -s web --category www-client --repo-web https://code.funtoo.org/bitbucket/projects/AUTO/repos/browser-kit/browse
bin/get_catpkgs_json.py -s web --branch 3.34-prime --category app-admin --repo-web https://code.funtoo.org/bitbucket/projects/INDY/repos/gnome-kit/browse
bin/get_catpkgs_json.py -s web --category app-admin --repo-web https://github.com/funtoo/gnome-kit --commit f1c94357c0681b6258020c0b82f9bd9b47f8cec4
bin/get_catpkgs_json.py -s fs -k core-kit --category sys-kernel -c d68adcb7a1463bcf5be7127dfffe448fcf503276
```
7. Easter egg:
```
bin/searchdesc.py --searchdesc javascript
```

## I want to contribute/learn more technical details
Check out [CONTRIBUTING](CONTRIBUTING.md)
