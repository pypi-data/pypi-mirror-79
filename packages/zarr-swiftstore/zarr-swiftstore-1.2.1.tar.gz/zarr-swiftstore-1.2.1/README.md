# zarr-swiftstore
openstack swift object storage backend for zarr. It enables direct access to
object storage to read and write zarr datasets.

## Install

```bash
git clone https://github.com/siligam/zarr-swiftstore.git
cd zarr-swiftstore
python setup.py install
```

## Usage

SwiftStore authentication requires (authurl, user, key) or (preauthurl, preauthtoken)
values. Alternative way of providing these values is through environment variables
(ST_AUTH, ST_USER, ST_KEY) or (OS_STORAGE_URL, OS_AUTH_TOKEN).

In the following examples the authentication information is provided through
environment variables.

1. using zarr

```python
import os
import zarr
from zarrswift import SwiftStore

auth = {
    "preauthurl": os.environ["OS_STORAGE_URL"],
    "preauthtoken": os.environ["OS_AUTH_TOKEN"],
}

store = SwiftStore(container='demo', prefix='zarr-demo', storage_options=auth)
root = zarr.group(store=store, overwrite=True)
z = root.zeros('foo/bar', shape=(10, 10), chunks=(5, 5), dtype='i4')
z[:] = 42
```

2. using xarray

```python
import xarray as xr
import numpy as np
from zarrswift import SwiftStore

ds = xr.Dataset(
        {"foo": (('x', 'y'), np.random.rand(4, 5))},
        coords = {
          'x': [10, 20, 30, 40],
          'y': [1, 2, 3, 4, 5],
        },
}

store = SwiftStore(container='demo', prefix='xarray-demo', storage_options=auth)
ds.to_zarr(store=store, mode='w', consolidated=True)

# load
ds = xr.open_zarr(store=store, consolidated=True)
```

## Test
To run test, set environment variable ZARR_TEST_SWIFT=1
```bash
export ZARR_TEST_SWIFT=1
pytest -v zarrswift
```
