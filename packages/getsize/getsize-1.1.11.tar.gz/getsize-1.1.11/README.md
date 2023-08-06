# getsize
Get and display the size of file and directory with binary prefixes

## Install

`$ pip install getsize`

## Usage

`$ getsize [OPTION] [FILE]...`

```
Options:
    -h - Show this help
    -v - Show version information
    -b - Bytes
    -k - KiB
    -m - MiB
    -g - GiB
    -t - TiB
    -p - PiB
    -e - EiB
    -z - ZiB
    -y - YiB
```

### Use as a module

```python
In [1]: import getsize

In [2]: gs = getsize.GetSize()

In [3]: gs.convSize(4096)
Out[3]: (4.0, 'KiB')

In [4]: gs.convSize(4096, 'KiB')
Out[4]: (4.0, 'KiB')

In [5]: gs.getSize(['README.md'])
790.000 Bytes README.md

In [6]: gs.getSize(['README.md'], 'KiB')
0.771 KiB README.md

In [7]: fs = gs.getArgSize('README.md')

In [8]: for file, size in fs:
   ...:     print(file, size)
   ...:
README.md 790

```
