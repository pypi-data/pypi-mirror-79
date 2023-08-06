# Datacoral's Python Instrumentation using Snowplow

## Prerequisits

This section of the documentation is useful if you have the [Datacoral Events Connector][1] already added to your Datacoral Installation.  
Contact support@datacoral.co today, in oredr to set up your new Events Connector.  

[1]: https://docs.datacoral.com/ingest_connectors/events/home/

## Overview
Our default Collect Events Slice is compatible with the [Snowplow Tracker Protocol][2].

[2]: https://github.com/snowplow/snowplow/wiki/snowplow-tracker-protocol

Snowplow provides tracker or instrumentation libraries in several languages.  
We have incorporated those libraries and enhanced them to support:  
1. Pointing to your own Events HTTP Endpoint.  
2. Generate API Keys
3. Create multiple environments like dev/stage/prod so that events can be segregated based on the environment.
4. A browser js instrumentation, specifying [CORS Origins][3]  

[3]: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

## Contributing quickstart
> Assuming [Git][4] and [Datacoral CLI][5] are installed:

[4]: https://git-scm.com/
[5]: https://docs.datacoral.com/install_cli/  


## Installing datacoral-tracker-py
```
pip install datacoral-tracker-py
```

## Publishing (Tracking)

```python
from snowplow_tracker import SelfDescribingJson, Tracker, Emitter

# Initialize the emitter
emitter = Emitter("your-api-gatewat-FQDN-here", buffer_size=1)

# Initialize the tracker
tracker = Tracker(
    emitter,
    datacoral_env="dev",
    api_key=["your-api-key-here"],
    namespace="your-namespace-here",
    app_id="app-id-here",
    encode_base64=True
)

# Send a custom event with your own schema and contexts
data = {
    "foo": "bar",
    "metadata": {
        "sub": "data"
    }
}

sjson = SelfDescribingJson(
    schema="test",
    data=data)

tracker.track_unstruct_event(
    event_json=sjson)

```

## Additional Reading
- [Events Slice Overview][5]
- [Event from Python][5.1]

[5]: https://docs.datacoral.com/ingest_connectors/events/home/
[5.1]: https://docs.datacoral.com/ingest_connectors/events/python/


## Copyright and license
Licensed under the [Apache License, Version 2.0][4] (the "License");
you may not use this software except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

[4]: http://www.apache.org/licenses/LICENSE-2.0
