
"""
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

MIT License

Copyright (c) 2024 by Shobhit Maniar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
"""

import requests
import json
from datetime import datetime, timedelta, timezone

class DX:
    def __init__(self, api_key:str, feed_id:str, version:float=1, delta:float|None =None):
        """
        Initializes the DX class.

        :param api_key: Required. API key for authentication.
        :param feed_id: Required. Feed ID for the data feed.
        :param version: Optional. Version of the API. Default is 1.
        :param delta: Optional. Time difference for event time. Default is 0 minutes.
        """
        self.api_key = api_key
        self.feed_id= feed_id
        self.version = version if version else 1
        self.url = "https://api.mkdx.btcsp.co.uk/data-service/sensors/feeds/"
        self.header = {
            "accept": "application/json",
            "x-api-key": f"{self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.delta = timedelta(minutes=delta) if delta is not None else timedelta(minutes=0)
            
    def get_current_time(self):
        """Return the current time in the required format."""
        return (datetime.now(timezone.utc) + self.delta).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


    def post(self, stream_id:int, data:str):
        """
        Sends a POST request to the ingestion URL.

        :param stream_id: Required. Stream ID to send the data.
        :param data: Required. The data to be posted.
        """
        self.post_stream_id = stream_id
        self.data = data
        if not self.api_key:
            print("Please enter your API key.")
            return None
        
        self.ingest_url= f"https://ing.mkdx.btcsp.co.uk/datahub-adapter/sensors/feeds/{self.feed_id}/{self.version}"
        self.time_now = self.get_current_time()
        # Create the JSON payload
        self.json = {
            "data": [
                {
                    "streamId": self.post_stream_id,  # Use the streamId
                    "value": self.data,
                    "eventTime": self.time_now
                }
            ]
        }

        try:
            response = requests.post(self.ingest_url, headers=self.header, json=self.json)
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get(self, stream_id:str, display:bool=False, agregate:bool|None = None):
        """
        Sends a GET request to fetch the data stream.

        :param stream_id: Required. Stream ID to fetch the data.
        :param display: Optional. If True, display the fetched data. Default is False.
        """
        self.get_stream_id = stream_id
        if not self.api_key:
            print("Please enter your API key.")
            return None
        self.agregate = agregate if agregate is not None else False
        if self.agregate:
            self.get_url = f"https://api.mkdx.btcsp.co.uk/data-service/sensors/feeds/{self.feed_id}/{self.version}/datastream/{self.get_stream_id}/datapoints?limit=100"
        else:
            self.get_url = f"https://api.mkdx.btcsp.co.uk/data-service/sensors/feeds/{self.feed_id}/{self.version}/datastream/{self.get_stream_id}"

        try:
            response = requests.get(self.get_url, headers=self.header)
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
            if display:
                self.display_data(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def display_data(self, data):
        """Prints the pollution data in a readable format."""
        if data:
            print(json.dumps(data, indent=4))  # Pretty print the JSON data
        else:
            print("No data to display.")
