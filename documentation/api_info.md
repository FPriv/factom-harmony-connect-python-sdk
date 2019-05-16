api_info
-------

### get <a name="info_get">

Gets general information about the Connect API.

**Sample**
```python
factom_client.api_info.get()
```
**Parameters**

| **Name**                 | **Type** | **Description**                                                                                                                                                                                                                                                                                                                               | **SDK Error Message & Description** |
|--------------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
| `client_overrides`  | optional                               | dict </br>  This is the override parameter that allows user to specify which instantiation of the SDK to be overridden simply by adding `client_overrides[key]`.</br> Keys are allowed to be overridden are: </br>- app_id </br>- app_key</br>- base_url</br>                                   |


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
