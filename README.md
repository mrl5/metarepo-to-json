# metarepo-to-json
export [Funtoo meta-repo](https://github.com/funtoo/meta-repo) to JSON

## Install dependencies
* `eix` - https://github.com/vaeth/eix/ - Search and query ebuilds
* `libxslt` - http://www.xmlsoft.org/ - XSLT libraries and tools
* `jq` - https://stedolan.github.com/jq/ - A lightweight and flexible command-line JSON processor

```
emerge -avju dev-libs/libxslt app-portage/eix app-misc/jq
```
