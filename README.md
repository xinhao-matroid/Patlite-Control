Adopted from https://github.com/PATLITE-Corporation/LA6-POE_windows_python_example/tree/main

# Patlite Control

```python
from patlite_control import PatliteControl
from patlite_control.messages import RunControlCommandData
from patlite_control.actions import RunControlCommandRequest, ClearCommandRequest, GetDataCommandRequest, GetDetailDataCommandRequest
from patlite_control.constants import LEDUnit, BUZZERUnit
# Connect to LA-POE
with PatliteControl('192.168.86.106', 10000) as p:
    data = RunControlCommandData(
        LEDUnit.ON,
        LEDUnit.OFF,
        LEDUnit.OFF,
        LEDUnit.OFF,
        LEDUnit.OFF,
        BUZZERUnit.PATTERN2,
    )
    req = RunControlCommandRequest(data)
    res = p.send_request(req)
    print(res)
    print(res.is_bad_response())

    # Beep for 1 second
    import time
    time.sleep(1)

    req = ClearCommandRequest()
    res = p.send_request(req)
    print(res.is_bad_response())

    # Get info 
    req = GetDataCommandRequest()
    res = p.send_request(req)
    print(res)

    req = GetDetailDataCommandRequest()
    res = p.send_request(req)
    print(res)
```