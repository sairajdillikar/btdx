[![PyPI Latest Release](https://img.shields.io/pypi/v/data-exchange.svg)](https://pypi.org/project/data-exchange/)


The DX class is designed to interact with the MKDX API for posting and retrieving sensor data. 
Below is a guide on how to use the class effectively.

1. **Initialization** To use the DX class, you need to initialize it with your API key, feed ID, and optionally a version number.
   
   ```python
   from DX import DX  # Make sure to import the DX class from the module
   api_key = "your_api_key"     # Your API key
   feed_id = "your_feed_id"     # The feed ID you want to interact with
   version = 1                  # Optional: Version number (default is 1)
   dx = DX(api_key, feed_id, version)
   ```

2. **Posting Data** You can post data to a specific stream by calling the post method. You need to provide the stream ID and the data you want to post.

    ```python
    stream_id = "100"           # The ID of the stream you want to post data to
    data =  "AQI: 2"         # The value you want to post
    dx.post(stream_id=stream_id, data=data)
    ```

3. **Getting Data** To retrieve data from a specific stream, use the get method. You can specify the stream ID and whether you want to display the data. You can also pass optional parameters such as agregate.

    ```python
    stream_id = "100"           # The ID of the stream you want to get data from
    # Retrieve and display data
    dx.get(stream_id=stream_id, display=True)
    # Retrieve last 100 values and display data
    dx.get(stream_id=stream_id, display=True, agregate=True)
    ``` 