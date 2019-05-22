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
| `app_id`             | optional | string</br>  This is the override parameter that allows user to specify a different API Application ID (which you can see by clicking on any of the applications in the application list that you see upon logging into  https://account.factom.com).               |
| `app_key `            | optional | string </br> This is the override parameter that allows user to specify a different API Application Key (which you can see by clicking on any of the applications in the application list that you see upon logging into  https://account.factom.com).              |
| `base_url `           | optional | string </br> This is the override parameter that allows user to specify a different API Base URL for your application (which you can see by clicking on any of the applications in the application list the you see upon logging into  https://account.factom.com). |


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
