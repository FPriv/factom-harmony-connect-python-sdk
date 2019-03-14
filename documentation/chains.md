chains
------

#### get

Gets information about a specific chain from Connect.

**Parameters:**

| **Name**                     | **Type** | **Description**                                                                                                                                                                                                                                                                       | **SDK Error Message & Description**                                 |
|------------------------------|----------|------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `chain_id`                   | required | string </br> The unique identifier created for each chain.                                                                                                                                                                                                                            | **chain_id is required** </br> `chain_id` parameter was not provided. |
| `signature_validation`       | optional | boolean (`true`/`false`/`custom function`) </br> Default value is `true`. </br> Indicates whether the SDK automatically validates that the chain was signed based on our signing standard. </br> `custom function`: allows for validating the chain's signature  based on custom logic. |  


**Returns:**

**Response:** OK
-   **data:** object
    -   **data.chain_id:** string </br> The unique identifier created for each chain.
    -   **data.content:** string </br> The data that was stored in the first entry of this chain.
    -   **data.external_ids:** array of strings </br> Tags that have been used to identify the first entry of this chain.
    -   **data.stage:** string </br> The immutability stage that this chain has reached.
    -   **data.entries:** object
        -   **data.entries.href:** string </br> An API link to all of the entries in this chain.
    -   **data.eblock:** object </br> Represents the Entry Block that contains the first entry of this chain. This will be null if the chain is not at least at the `factom` immutability stage.
	    -   **data.eblock.keymr:** string </br> The Key Merkle Root for this entry block.
	    -   **data.eblock.href:** string </br> An API link to retrieve all information about this entry block.
	-   **data.dblock:** object </br> Represents the Directory Block that relates to this chain. This will be null if the chain is not at least at the `factom` immutability stage.
		-   **data.dblock.keymr:** string </br> The Key Merkle Root for this directory block.
		-   **data.dblock.height:** integer </br> The Factom blockchain height of this directory block.
		-   **data.dblock.href:** string </br> An API link to retrieve all information about this directory block.
	-   **data.created_at:** string </br> The time at which the chain was created. Sent in [ISO 8601 Format](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.ssssssZ`. This will be null if the chain is not at least at the `factom` immutability stage.
-   **status:** string </br> The result of signature validation.</br>
Displays an empty string ("") when `signature_validation` is set to `false`.
</br> Or displays a function's result when `signature_validation` is set to `custom function`.
</br> In case `signature_validation` is set to `true` then one of the following values will be returned based on an automatic comparison of the expected SignedChain structure outlined in our signing standard.
    -   **not_signed/invalid_chain_format:** A chain that was not signed or did not conform to the SignedChain structure.
    -   **invalid_signature:** A chain was created in the proper SignedChain structure, but the signature does not match the attached key.
    -   **retired_height:** A chain that conformed to the SignedChain structure and the signature was verified with the listed key, but
    that key was retired for the signer identity at a height lower than when this chain reached the `factom` immutability stage.
    -   **valid_signature:** A chain that conformed to the SignedChain structure and the signature was verified with the listed key. That key was also active for the signer identity at the height when this chain reached the `factom` immutability stage.

#### create

Creates a new chain with or without signature:

-   When the Factom SDK is initialized, if `automatic_signing` =  `true`; in order to create a signed chain, you need to pass:
    -   `signer_chain_id`
    -   `signer_private_key`
-   When the Factom SDK is initialized, if `automatic_signing` = `false`, SDK creates an unsigned chain and therefore it does not require these parameters.

**Parameters**


| **Name**                  | **Type**                               | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                      | **SDK Error Message & Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|---------------------------|----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `external_ids`            | required </br> or </br> optional </br> | array of strings</br> Tags that can be used to identify your chain. You can search for records that contain a particular `external_ids` using Connect.</br>  **Note:** Since the Connect API requires each array element to be Base64 encoded, the SDK will do so before making the API request. This parameter is only required for creating an unsigned chain (`automatic_signing` is set to `false`). | **at least 1 external_id is required.** </br> `external_ids` parameter was not provided when `automatic_signing` was set to `false`. </br>**external_ids must be an array.**</br>  An invalid `external_ids` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `content`                 | required                               | string </br>  This is the data that will make up the first entry in your new chain. It is customary to use this space to describe the entries that are to follow in the chain.</br> **Note:** Since the Connect API requires the `content` to be Base64 encoded, the SDK will do so before making the API request.                                                                                | **content is required.**</br>    `content` parameter was not provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `signer_chain_id`         | required </br> or </br> optional </br> | string </br> The chain id of the signer identity.</br> **Note:** This parameter is optional for creating an unsigned chain. However, if `signer_private_key` is inputted then `signer_chain_id` must also be inputted.                                                                                                                                                                                | In case of creating a signed chain: </br></br> **signer_chain_id is required.** </br> `signer_chain_id` parameter was not provided. </br></br>In case of creating an unsigned chain:</br></br>  **signer_chain_id is required when passing a signer_private_key.**</br> `signer_private_key` parameter was provided but lacking `signer_chain_id` parameter.                                                                                                                                                                                                                                                                                                                                       |
| `signer_private_key`      | required </br> or </br> optional </br> | base58 string in Idsec format</br> The private key signer would like to sign with. In fact, private key is used to generate the public key, which is included as an external ID on the created signed entry. </br> **Note:** This parameter is optional for creating an unsigned chain. However, if `signerChainId` is inputted then `signer_private_key` must also be inputted.                                     | In case of creating a signed chain:</br></br> **signer_private_key is required.**</br> `signer_private_key` parameter was not provided.</br>  **signer_private_key is invalid.** </br> An invalid `signer_private_key` parameter was provided or key’s byte length is not equal to 41. </br></br> In case of creating an unsigned chain: </br></br> **signer_private_key is required when passing a signer_chain_id.** </br>   `signer_chain_id` parameter was provided but lacking `signer_private_key` parameter.  </br>  **signer_private_key is invalid.**  </br> `signer_chain_id` was provided but either an invalid `signer_private_key` parameter was also provided or key’s byte length is not equal to 41. |
| `callback_url`            | optional                               | string </br> The URL where you would like to receive the callback from Connect. </br> **Note:** If this is not specified, callbacks will not be activated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | **callback_url is an invalid url format.** </br> An invalid `callbackUrl` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `callback_stages`         | optional                               | array of strings </br> The immutability stages you would like to be notified about. This list can include any or all of the three stages: `replicated`, `factom`, and `anchored`. For example, when you would like to trigger the callback from Connect at `replicated` and `factom` stage, you would send them in the format: [‘replicated’, ‘factom’]. </br> **Note:** For this field to matter, the URL must be provided. If callbacks are activated (URL has been specified) and this field is not sent, it will default to `factom` and `anchored`. | **callback_stages must be an array.** </br> An invalid `callback_stages` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |


**Returns**

**Response**: Accepted

-   **chain_id:** string </br> This is the unique identifier created for each chain.  </br>**Note:** Chain ID is a hash based on the external IDs you choose. External IDs must be unique or else the chain creation will fail.
-   **entry_hash:** string </br> The SHA256 Hash of the first entry of this new chain.
-   **stage:** string </br> The immutability stage that this chain has reached.

#### list

Gets all of the chains on Factom.

**Parameters**

| **Name**        | **Type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                | **SDK Error Message & Description**                                            | 
|-----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `limit`  | optional | integer </br>  The number of items you would like to return back in each stage. The default value is 15.                                                                                                                                                                                                                                                                          | **limit must be an integer.**</br>   An invalid `limit` format was provided.  |   
| `offset` | optional | integer </br>  The offset parameter allows you to select which item you would like to start from when a list is returned from Connect. For example, if you have already seen the first 15 items and you would like the next set, you would send an offset of 15. `offset=0` starts from the first item of the set and is the default position.   | **offset must be an integer.**  </br>  An invalid `offset` format was provided. |   
| `stages` | optional | array of strings </br>  The immutability stages you want to restrict results to. You can choose any from `replicated`, `factom`, and `anchored`. The default value are these three stages: `replicated`, `factom`, and `anchored`. </br>  **Note**: If you would like to search among multiple stages, you would send them in the format: [‘replicated’, ‘factom’]. | **stages must be an array.**</br>  An invalid `stages` format was provided.   |   


**Returns**

**Response:** OK
-   **data:** array of objects </br> An array that contains the chains on this page.
    -   **data[].chain_id:** string </br> The ID for this chain on the Factom blockchain.
    -   **data[].external_ids:** array of strings </br> The external IDs attached to this chain on the Factom blockchain.
    -   **data[].href:** string </br> An API link to retrieve all information about this chain.
    -   **data[].stage:** string </br> The immutability stage that this chain has reached.
    -   **data[].created_at:** string </br> The time when the chain was created. Sent in [ISO 8601 Format](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.ssssssZ`. This will be null if the chain is not at least at the `factom` immutability stage.
-   **offset:** integer </br> The index of the first chain returned from the total set, which starts from 0.
-   **limit:** integer </br> The number of chains returned.
-   **count:** integer </br> The total number of chains seen.

#### search

Finds all of the chains with `external_ids` that match what you entered. 

**Parameters**

| **Name**             | **Type** | **Description**                                                                                                                                                                                                                                                                                                                                                                            | **SDK Error Message & Description**                                                                                                                                                        |   
|----------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `external_ids` | required | array of strings </br>  A list of external IDs associated with the chains user would like to search by.                                                                                                                                                                                                                                                                              | **at least 1 external_ids is required.**</br>  `external_ids` parameter was not provided.</br>   **external_ids must be an array.** </br>  An invalid `external_ids` format was provided. |   
| `limit`       | optional | integer </br> The number of items you would like to return back in each stage. The default value is 15.                                                                                                                                                                                                                                                                             | **limit must be an integer.** </br> An invalid `limit` format was provided.                                                                                                          |   
| `offset`      | optional | integer </br>  The offset parameter allows you to select which item you would like to start from when a list is returned from Connect. For example, if you have already seen the first 15 items and you would like the next set, you would send an offset of 15. `offset=0` starts from the first item of the set and is the default position. | **offset must be an integer.**</br>  An invalid `offset` format was provided.                                                                                                       |   


##### 

**Returns:**

**Response:** OK
-   **data:** array of objects </br> An array that contains the chains on this page.
    -   **data[].chain_id:** string </br> The ID for this chain on the Factom blockchain.
    -   **data[].external_ids:** array of strings </br> The external IDs attached to this chain on the Factom blockchain.
    -   **data[].href:** string </br> An API link to retrieve all information about this chain.
    -   **data[].stage:** string </br> The level of immutability that this chain has reached.
    -   **data[].created_at:** string </br> The time at which this chain was created. Sent in [ISO 8601 Format](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.ssssssZ`. This will be null if the chain is not at least at the `factom` immutability stage.
-   **offset:** integer </br> The index of the first chain returned from the total set, which starts from 0.
-   **limit:** integer </br> The number of chains returned.
-   **count:** integer </br> The total number of chains seen.

#### entries

##### get

Gets information about a specific entry on Connect.

**Parameters:**

| **Name**                     | **Type** | **Description**                                                                                                                                                                                                                                                                                                        | **SDK Error Message & Description**                                            |
|------------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `chain_id`             | required | string </br>  The chain identifier.                                                                                                                                                                                                                                                                                    | **chain_id is required.**</br>  `chain_id` parameter was not provided.   |
| `entry_hash`           | required | string </br> The SHA256 hash of the entry.                                                                                                                                                                                                                                                                             | **entry_hash is required.** </br> `entry_hash` parameter was not provided. |
| `signature_validation` | optional | boolean (`true`/`false`/`custom function`) </br>  The default value is `true`. Indicates whether the SDK automatically validates that the entry was signed based on our signing standard. </br> `custom function`: allows for validating the entry's signature based on custom logic.|                                                                                |


**Returns:**

**Response:** OK
-   **data:** object
    -   **data.entry_hash:** string </br> The SHA256 Hash of this entry.
    -   **data.chain:** object </br> An object that contains the Chain Hash (ID) as well as a URL for the chain.
        -   **data.chain.chain_id:** string </br> The ID for this chain on the Factom blockchain.
        -   **data.chain.href:** string </br> An API link to retrieve all information about this chain.
    -   **data.created_at:** string </br> The time when this entry was created. Sent in [ISO 8601 Format](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ssssssZ`.
    -   **data.external_ids:** array of strings </br> Tags that can be used to identify your entry. You can search for records that contain a particular external ID using Connect.</br> **Note**: Since the Connect API Base64 encodes these values for transport, each array element will be decoded for you by the SDK.
    -   **data.content:** string </br> This is the data that is stored by the entry.</br>  **Note**: Since the Connect API Base64 encodes these values for transport, `content` will be decoded for you by the SDK.
    -   **data.stage:** string </br> The level of immutability that this entry has reached.
    -   **data.dblock:** object </br> Represents the Directory Block that relates to this entry. This will be null if the chain is not at least at the `factom` immutability stage.
		-   **data.dblock.keymr:** string </br> The Key Merkle Root for this directory block.
		-   **data.dblock.height:** integer </br> The Factom blockchain height of this directory block.
		-   **data.dblock.href:** string </br> An API link to retrieve all information about this directory block.
	-   **data.eblock:** object </br> Represents the Entry Block that contains the entry. This will be null if the entry is not at least at the `factom` immutability stage.
		- **data.eblock.keymr:** string</br> The Key Merkle Root for this entry block.
		- **data.eblock.href:** string</br> An API link to retrieve all information about this entry block.
-   **status:** string </br> The result of signature validation.</br>
Displays an empty string ("") when `signature_validation` is set to `false`.</br>
Or displays a function's result when `signature_validation` is set to `custom function`.</br>
In case `signature_validation` is set to `true` then one of the following values will be returned based on an automatic comparison of the expected SignedEntry structure outlined in our signing standard.
    - **not_signed/invalid_entry_format:** An entry that was not signed or did not conform to the SignedEntry structure.
    - **invalid_signature:** An entry was created in the proper SignedEntry structure, but the signature does not match the attached key.
    - **retired_height:** An entry that conformed to the SignedEntry structure and the signature was verified with the listed key, but that key was retired for the signer identity at a height lower than when this entry reached the `factom` immutability stage.
    - **valid_signature:** An entry that conformed to the SignedEntry structure and the signature was verified with the listed key. That key was also active for the signer identity at the height when this entry reached the `factom` immutability stage.

##### create

Creates a new entry for the selected chain with or without signature:

-   When the Factom SDK is initialized, if `automatic_signing` = `true`; in order to create a signed entry, you need to pass:
    -   `signer_chain_id`
    -   `signer_private_key`
-   When the Factom SDK is initialized, if `automatic_signing` =
    `false`, SDK creates an unsigned entry and therefore it does
    not require these parameters.

**Parameters:**

| **Name**                  | **Type**                         | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | **SDK Error Message & Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|---------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `chain_id`          | required                         | string </br>  The chain identifier.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | **chain_id is required.**</br>  `chain_id` parameter was not provided.</br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `external_ids`      | required</br>  or</br>  optional | array of strings </br> Tags that can be used to identify your entry. You can search for records that contain a particular external ID using Connect.</br>  **Note:** Since the Connect API requires each array element to be Base64 encoded, the SDK will do so before making the API request. This parameter is only required for creating an unsigned entry (`automatic_signing` is set to `false`).                                                                                                                                                       | **at least 1 external_id is required.**</br> `external_ids` parameter was not provided when `automatic_signing` is set to `false`.</br>  **external_ids must be an array.**</br>  An invalid `external_ids` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `content`          | required                         | string</br> This is the data that will be stored directly on the blockchain. Please be sure that no private information is entered here.</br> **Note:** The value in `content` parameter will be encoded in Base64 format by Connect SDK.                                                                                                                                                                                                                                                                                                                                                        | **content is required.**</br> `content` parameter was not provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `signer_chain_id`    | required</br> or</br> optional   | string</br> The chain ID of the signer identity.</br>  **Note:** This parameter is optional for creating an unsigned entry. However, if `signer_private_key` is inputted then `signer_chain_id` must also be inputted.                                                                                                                                                                                                                                                                                                                                                                                       | In case of creating a signed entry:</br></br> **signer_chain_id is required.**</br> `signer_chain_id` parameter was not provided.</br></br>  In case of creating an unsigned entry:</br></br>  **signer_chain_id is required when passing a signer_private_key.**</br> `signer_private_key` was provided but lacking `signer_chain_id` parameter.                                                                                                                                                                                                                                                                                                                                                                                                   |
| `signer_private_key` | required</br>  or</br>  optional | a base58 string in Idsec format</br> The private key signer would like to sign with. In fact, private key is used to generate the public key, which is included as an external ID on the created signed entry.</br>   **Note:** This parameter is optional for creating an unsigned entry. However, if `signer_chain_id` is inputted then `signer_private_key` must also be inputted.                                                                                                                                                                                               | In case of creating a signed entry:</br></br>  **signer_private_key is required.**</br> `signer_private_key` parameter was not provided.</br>  **signer_private_key is invalid.**</br> An invalid `signer_private_key` parameter was provided or key's byte length is not equal to 41. </br></br>  In case of creating an unsigned entry:</br></br>  **signer_private_key is required when passing a signer_chain_id.**</br> `signer_chain_id` was</br>  provided but lacking `signer_private_key` parameter.</br>  **signer_private_key is invalid.**</br>  `signer_chain_id` was provided but an invalid `signer_private_key` parameter was provided or key's byte length is not equal to 41.  |
| `callback_url`      | optional                         | string</br> the URL you would like the callbacks to be sent to </br> **Note:** If this is not specified, callbacks will not be activated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | **callback_url is an invalid url format.**</br> An invalid `callback_url` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `callback_stages`   | optional                         | array of strings</br>  The immutability stages you would like to be notified about. This list can include any or all of these three stages: `replicated`, `factom`, and `anchored`. For example, when you would like to trigger the callback from Connect from `replicated` and `factom` then you would send them in the format: ['replicated', 'factom'].</br> **Note:** For this field to matter, the URL must be provided. If callbacks are activated (URL has been specified) and this field is not sent, it will default to `factom` and `anchored`. | **callback_stages must be an array.**</br> An invalid `callback_stages` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |


**Returns:**

**Response**: Accepted
-   **entry_hash** string </br>
    The SHA256 Hash of the entry you just created. You can use this hash
    to reference this entry in the future.
-   **stage:** string </br> The current immutability stage of the new entry.

##### list

Gets list of all entries contained on a specified chain.

**Parameters:**

| **Name**         | **Type** | **Description**                                                                                                                                                                                                                                                                                                                                                                            | **SDK Error Message & Description**                                                    |
|------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| `chain_id` | required | string </br>  The chain identifier.                                                                                                                                                                                                                                                                                                                                                        | **chain_id is required.**</br>  `chain_id` parameter was not provided.</br>              |
| `limit`   | optional | integer </br> The number of items you would like back in each page. The default value is 15.                                                                                                                                                                                                                                                                                        | **limit must ben an integer.**</br> An invalid `limit` format was provided.</br>  |
| `offset`  | optional | integer</br> The offset parameter allows you to select which item you would like to start from when a list is returned from Connect. For example, if you have already seen the first 15 items and you would like the next set, you would send an offset of 15. `offset=0` starts from the first item of the set and is the default position. | **offset must be an integer.**</br> An invalid `offset` format was provided.|
| `stages`  | optional | array of strings</br> The immutability stages you want to restrict results to. You can choose any from `replicated`, `factom`, and `anchored`. The default value are these three stages: `replicated`, `factom` and `anchored`.</br>  **Note:** If you would like to search among multiple stages, you would send them in the format ['replicated', 'factom'].  | **stages must be an array.**</br>  An invalid `stages` format was provided. |

**Returns:**

**Response:** OK

-   **data:** array of objects </br> An array that contains the entries on this page.
    -   **data[].entry_hash:** string </br> The SHA256 Hash of this entry.
    -   **data[].chain:** object </br> An object that contains the Chain Hash (ID) as well as a URL for the chain.
        -   **data[].chain.chain_id:** string </br> The ID for this chain on the Factom blockchain.
        -   **data[].chain.href:** string </br> An API link to retrieve all information about this chain.
    -   **data[].created_at:** string </br> The time at which this entry was created. Sent in [ISO 8601 Format](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ssssssZ`.
    -   **data[].href:** string </br>  An API link to retrieve all information about this entry.
-   **offset:** integer </br> The index of the first entry returned from the total set starting from 0.
-   **limit:** integer </br> The number of entries returned per page.
-   **count:** integer </br> The total number of entries seen.

##### get_first

Retrieves the first entry that has been saved to this chain.

**Parameters:**

| **Name**                     | **Type** | **Description**                                                                                                                                                                                                                                                                                                   | **SDK Error Message & Description**                                       |
|------------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `chain_id`             | required | string </br>  The chain identifier.                                                                                                                                                                                                                                                                               | **chain_id is required.**</br>  `chain_id` parameter was not provided.</br> |
| `signature_validation` | optional | boolean (`true`/`false`/`custom function`)</br> Default value is `true`.</br>  Indicates whether the SDK automatically validates that the entry was signed based on our signing standard.</br>   `custom function`: allows for validating the entry's signature based on custom logic. |                                                                           |

##### Returns:

**Response:** OK

-   **data:** object
    -   **data.entry_hash:** string </br> The SHA256 Hash of this entry.
    -   **data.chain:** object </br> An object that contains the Chain Hash (ID) as well as a URL for the chain.
        -   **data.chain.chain_id:** string </br> The ID for this chain on the Factom blockchain.
        -   **data.chain.href:**: string </br> An API link to retrieve all information about this chain.
    -   **data.created_at:** string </br> The time at which this entry was created. Sent in [ISO 8601 Format](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ssssssZ`.
    -   **data.external_ids:** array of strings </br> Tags that can be used to identify your entry. You can search for records that contain a particular external ID using Connect. </br> **Note:** Since the Connect API Base64 encodes these values for transport, each array element will be decoded for you by the SDK.
    -   **data.content:** string </br> This is the data that is stored by the entry. </br> **Note:** Since the Connect API Base64 encodes these values for transport, `content` will be decoded for you by the SDK.
    -   **data.stage:** string </br> The level of immutability that this entry has reached.
    -   **data.dblock:** object </br> Represents the Directory Block that relates to this entry. This will be null if the chain is not at least at the `factom` immutability stage.
		-   **data.dblock.keymr:** string </br> The Key Merkle Root for this directory block.
		-   **data.dblock.height:** integer </br> The Factom blockchain height of this directory block.
		-   **data.dblock.href: :** string </br> An API link to retrieve all information about this directory block.
	-   **data.eblock**: object </br> Represents the Entry Block that contains the entry. This will be null if the entry is not at least at the `factom` immutability stage.
		-   **data.eblock.keymr:** string </br> The Key Merkle Root for this entry block.
		-   **data.eblock.href**: string </br> An API link to retrieve all information about this entry block.
-   **status:** string </br> The result of signature validation.</br>
Displays an empty string ("") when `signature_validation` is set to `false`.</br>
Or displays a function's result when `signature_validation` is set to `custom function`.</br>
In case `signature_validation` is set to `true` then one of the following values will be returned based on an automatic comparison of the expected SignedEntry structure outlined in our signing standard.
    - **not_signed/invalid_entry_format:** An entry that was not signed or did not conform to the SignedEntry structure.
    - **invalid_signature:** An entry was created in the proper SignedEntry structure, but the signature does not match the attached key.
    - **retired_height:** An entry that conformed to the SignedEntry structure and the signature was verified with the listed key, but that key was retired for the signer identity at a height lower than when this entry reached the `factom` immutability stage.
    - **valid_signature:** An entry that conformed to the SignedEntry structure and the signature was verified with the listed key. That key was also active for the signer identity at the height when this entry reached the `factom` immutability stage.

##### get_last

Gets the last entry that has been saved to this chain.

**Parameters:**

| **Name**                     | **Type** | **Description**                                                                                                                                                                                                                                                                                                   | **SDK Error Message & Description**                                       |
|------------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `chain_id`             | required | string </br>  The chain identifier.                                                                                                                                                                                                                                                                               | **chain_id is required.**</br>  `chain_id` parameter was not provided.</br> |
| `signature_validation` | optional | boolean (`true`/`false`/`custom function`)</br> Default value is `true`.</br> Indicates whether the SDK automatically validates that the entry was signed based on our signing standard.</br> `custom function`: allows for validating the entry's signature based on custom logic. |                                                                           |

##### Returns:

**Response:** OK

-   **data:** object
    -   **data.entry_hash:** string </br> The SHA256 Hash of this entry.
    -   **data.chain:** object </br> An object that contains the Chain Hash (ID) as well as a URL for the chain.
        -   **data.chain.chain_id:** string </br> The ID for this chain on the Factom blockchain.
        -   **data.chain.href:**: string </br> An API link to retrieve all information about this chain.
    -   **data.created_at:** string </br> The time at which this entry was created. Sent in [ISO 8601 Format](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ssssssZ`.
    -   **data.external_ids:** array of strings </br> Tags that can be used to identify your entry. You can search for records that contain a particular external ID using Connect. </br> **Note:** Since the Connect API Base64 encodes these values for transport, each array element will be decoded for you by the SDK.
    -   **data.content:** string </br> This is the data that is stored by the entry. </br> **Note:** Since the Connect API Base64 encodes these values for transport, `content` will be decoded for you by the SDK.
    -   **data.stage:** string </br> The level of immutability that this entry has reached.
    -   **data.dblock:** object </br> Represents the Directory Block that relates to this entry. This will be null if the chain is not at least at the `factom` immutability stage.
		-   **data.dblock.keymr:** string </br> The Key Merkle Root for this directory block.
		-   **data.dblock.height:** integer </br> The Factom blockchain height of this directory block.
		-   **data.dblock.href: :** string </br> An API link to retrieve all information about this directory block.
	-   **data.eblock**: object </br> Represents the Entry Block that contains the entry. This will be null if the entry is not at least at the `factom` immutability stage.
		-   **data.eblock.keymr:** string </br> The Key Merkle Root for this entry block.
		-   **data.eblock.href**: string </br> An API link to retrieve all information about this entry block.
-   **status:** string </br> The result of signature validation.</br>
Displays an empty string ("") when `signature_validation` is set to `false`.</br>
Or displays a function's result when `signature_validation` is set to `custom function`.</br>
In case `signature_validation` is set to `true` then one of the following values will be returned based on an automatic comparison of the expected SignedEntry structure outlined in our signing standard.
    - **not_signed/invalid_entry_format:** An entry that was not signed or did not conform to the SignedEntry structure.
    - **invalid_signature:** An entry was created in the proper SignedEntry structure, but the signature does not match the attached key.
    - **retired_height:** An entry that conformed to the SignedEntry structure and the signature was verified with the listed key, but that key was retired for the signer identity at a height lower than when this entry reached the `factom` immutability stage.
    - **valid_signature:** An entry that conformed to the SignedEntry structure and the signature was verified with the listed key. That key was also active for the signer identity at the height when this entry reached the `factom` immutability stage.

##### search

Finds all of the entries with `external_ids` that match what you entered. 

**Parameters:**

| **Name**             | **Type** | **Description**                                                                                                                                                                                                                                                                                                                                                                            | **SDK Error Message & Description**                                                                                                                                                 |
|----------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `chain_id`     | required | string </br>  The chain identifier.                                                                                                                                                                                                                                                                                                                                                        | **chain_id is required.**</br>  `chain_id` parameter was not provided.</br>                                                                                                           |
| `external_ids` | required | array of strings</br> A list of external IDs.</br> **Note:** Since the Connect API requires each array element to be Base64 encoded, the SDK will do so before making the API request.                                                                                                                                                                                   | **at least 1 external_id is required.**</br> `external_ids` parameter was not provided. </br>  **external_ids must be an array.**</br> An invalid `external_ids`parameter was provided. |
| `limit`       | optional | integer</br> The number of items you would like to return back in each page. The default value is  15.                                                                                                                                                                                                                                                                              | **limit must be an integer.**</br> An invalid `limit` format was provided.</br>                                                                                                      |
| `offset`      | optional | integer</br> The offset parameter allows you to select which item you would like to start from when a list is returned from Connect. For example, if you have already seen the first 15 items and you would like the next set, you would send an offset of 15. `offset=0` starts from the first item of the set and is the default position. | **offset must be an integer.**</br> An invalid `offset` format was provided.                                                                                              |

**Returns:**

**Response:** OK

-   **data:** array of objects
	-   **data[].entry_hash:** string </br> The SHA256 Hash of this entry.
    -   **data[].external_ids:** array of strings </br> Tags that can be used to identify your entry.</br> **Note:** Since the Connect API Base64 encodes these values for transport, each array element will be decoded for you by the SDK.
    -   **data[].stage:** string </br> The level of immutability that this entry has reached.
    -   **data[].href:** string </br> An API link to retrieve all information about this entry.
-   **offset:** integer </br> The index of the first item returned from the total set, which starts from 0.
-   **limit:** integer </br> The number of entries returned per page.
-   **count:** integer </br> The total number of entries seen.
