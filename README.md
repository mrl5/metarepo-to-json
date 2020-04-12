# metarepo-to-json
export [Funtoo meta-repo](https://github.com/funtoo/meta-repo) to JSON

## Install dependencies
* `eix` - https://github.com/vaeth/eix/ - Search and query ebuilds
* `libxslt` - http://www.xmlsoft.org/ - XSLT libraries and tools
* `jq` - https://stedolan.github.com/jq/ - A lightweight and flexible command-line JSON processor

```
emerge -avju dev-libs/libxslt app-portage/eix app-misc/jq
```

## Usage
1. Get `kit` jsons
```
sh workers/get_kits_json.sh
```
2. Get `category` jsons
```
sh workers/get_categories_json.sh -k <kit>
```
3. Get `package` json
```
sh workers/get_package_json.sh <eix_pakage_name>
```
