# osdupy

A simple python client for the [OSDU](https://community.opengroup.org/osdu) data platform.

## Usage

### Installation

```bash
pip install osdupy
```

### Example

`sample.py`

```python
from getpass import getpass()
from osdu import client

password = getpass()
osdu = client.init(api_url, client_id, user, password)

# Search for records by query.
query = {
    "kind": f"opendes:osdu:*:*"
}
result = osdu.search.query_with_cursor(query, max_results=10)

# Get a record.
record_id = 'opendes:doc:01255650acef4930a04048dbb4b559d0'
result = osdu.storage.get_record(record_id)

```

See [tests](tests/tests.py) for more copmrehensive usage examples.
