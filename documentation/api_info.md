api_info
-------

### get

Gets general information about the Connect API.

**Sample:**
```python
factom_client.api_info.get()
```
**Returns**</br>

**Response:** OK
-   **version:** string </br> Current version of the Connect API.
-   **links**: object </br> Links to internal paths of the application.
	-   **links.chains:** string </br> The link to chain API.
```python
{  
   'version':'1.0.17',
   'links':{  
      'chains':'/v1/chains'
   }
}
```
