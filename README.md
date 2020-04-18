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
python3 scripts/get_kits_json.py --help
```
6. Run scripts:
```
python3 scripts/get_kits_json.py -s web
python3 scripts/get_kits_json.py -s fs
```
```
python3 scripts/get_categories_json.py -s web --repo-web https://code.funtoo.org/bitbucket/projects/AUTO/repos/browser-kit/browse
python3 scripts/get_categories_json.py -s web --branch 3.34-prime --repo-web https://code.funtoo.org/bitbucket/projects/INDY/repos/gnome-kit/browse
python3 scripts/get_categories_json.py -s fs /var/git/meta-repo/kits/media-kit/
```

## I want to contribute/learn more technical details
Check out [CONTRIBUTING](CONTRIBUTING.md)
