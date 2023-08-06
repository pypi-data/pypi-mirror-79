# Pack/Unpack All-in-One WP Migration Packages

This library provides helper classes for packing/unpacking WordPress [All-in-One WP Migration](
https://wordpress.org/plugins/all-in-one-wp-migration/) packages.

# Installation

```shell script
pip install ai1wm
```

# Usage
## Unpack a File

```shell script
python -m ai1wm /path/to/the/source/wpress/file /path/to/the/destination/dir
```

## Pack a Directory

```shell script
python -m ai1wm /path/to/the/source/dir /path/to/the/destination/wpress/file
```

# Coding Examples
## Unpack a File

```python
from ai1wm import Ai1wmPackage

package = Ai1wmPackage('/path/to/the/destination/dir')
package.unpack_from('/path/to/the/source/wpress/file')
```

## Pack a Directory

```python
from ai1wm import Ai1wmPackage

package = Ai1wmPackage('/path/to/the/source/dir')
package.pack_to('/path/to/the/destination/wpress/file')
```
