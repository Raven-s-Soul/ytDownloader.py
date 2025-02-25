# ytDownloader.py
>[!NOTE]
>A simple YouTube downloader using `Pytubefix`, `FFmpeg` and `Node.js`.
>
>**No fancy gui** just a single link to paste in a console.

> [!IMPORTANT]
>
> `Node.js` is needed for the proof of origin (PO) token.
> 
>>Without it, format URL requests from affected customers may return HTTP error 403, error with bot detection, or result in your account or IP address being blocked. [source](https://pytubefix.readthedocs.io/en/latest/user/po_token.html)

## How to Use

### 1. Install Python
>Ensure that Python is installed on your system. You can download it from [here](https://www.python.org/downloads/) or `winget`, `brew`, `apt`, ...

### 2. Install Node.js
>Ensure that Node.js is installed on your system. You can download it from [here](https://nodejs.org/en/download) or ...

### 3. Install Dependencies
>Once Python is installed, you need to install the required dependencies as **administrator**. 
> - Make sure the paths are working. 
>You can do this by running the following command in your terminal:
>
>```bash
>pip install -r requirements.txt
>```

### 4. Running the Script
>[!TIP]
>>- Double-click the script to run it.
>>- Alternatively, run it from the terminal as:
>>
>| Command | Explanation |
>| :-- | :-- |  
>|`ytDownloader.py`|Will prompt for input|
>|`py ytDownloader.py`|Will prompt for input|
>|`ytDownloader.py <link>` |Provide a YouTube link to download the video|
>|`ytDownloader.py -h`|Show help message for usage details|


### Expert Users
>[!CAUTION]
> Put the `ytDownloader.py` script into your system's `path/bin`, making it usable in every folder.
