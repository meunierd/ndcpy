# ndcpy

A Python wrapper for ndc leveraging native Python types.

## Supported Version

Currently the only supported version is `Ver.0 alpha06`.

## Installation

```bash
pip install ndcpy
```

## Usage

Assuming ndc is on your PATH you can simply:

```python
from ndc import NDC

ndc = NDC()
```

If ndc isn't on your PATH, you can provide a path to the client object:

```python
ndc = NDC('~/path/to/ndc')
```

You can list the files in an image:

```python
ndc.list('image.hdi')
ndc.list('image.hdi', 'SOME/PATH')
```

You can search for a file by a pattern:

```python
ndc.find('image.hdi', '*.EXE')
ndc.find('image.hdi', '*.EXE', 'SOME/PATH')
```

...which will return a single result or `None`.

Alternatively, you can use `find_all` which will return a (potentially empty)
list of results.

Extract a file from an image with the `get` method:

```python
ndc.get('image.hdi', 'path/to/file')
```

Or you can insert with `put`:

```python
ndc.put('image.hdi', 'local/path', 'image/path')
```

To create a directory, use `put_directory`:

```python
ndc.put_directory('image.hdi', 'DIRECTORYNAME', 'image/path')
```

and lastly to delete a file:

```python
ndc.delete('image.hdi', 'image/path/to/file')
```
