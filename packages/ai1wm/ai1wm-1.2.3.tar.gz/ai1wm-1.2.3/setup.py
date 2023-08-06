from setuptools import setup


LONG_DESCRIPTION = '''
# Pack/Unpack All-in-One WP Migration Packages

This library provides helper classes for packing/unpacking WordPress [All-in-One WP Migration](
https://wordpress.org/plugins/all-in-one-wp-migration/) packages.

# Examples
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
'''

if __name__ == '__main__':
    setup(
        name='ai1wm',
        packages=['ai1wm'],
        version='1.2.3',
        license='MIT',
        description='Packs/Unpacks `All-in-One WP Migration` packages',
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        author='Sander Wang',
        author_email='sw.online@outlook.com',
        url='https://github.com/sanderwang/ai1wm',
        download_url='https://github.com/sanderwang/ai1wm/archive/1.2.3.tar.gz',
        keywords=['WordPress', 'All-in-One WP Migration'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
    )
