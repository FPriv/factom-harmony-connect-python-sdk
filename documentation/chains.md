chains
------

#### get

Gets information about a specific chain from Connect.

**Parameters:**

| **Name**                     | **Type** | **Description**                                                                                                                                                                                                                                                                       | **SDK Error Message & Description**                                 |
|------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `chain_id`             | required | string </br> The unique identifier created for each chain.                                                                                                                                                                                                                            | **chain_id is required** </br> `chain_id` parameter was not provided. |
| `signature_validation` | optional | boolean (`true`/`false`/`custom function`) </br> Default value is `true`. </br> Indicates whether the SDK automatically validates </br> that the chain was signed based on our signing standard. </br> `custom function`: allows for validating the chain's signature  based on custom logic. |                                                                     |

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
| `external_ids`      | required </br> or </br> optional </br> | array of strings</br> Tags that can be used to identify your chain.</br> You can search for records that </br> contain a particular `external_ids` using</br>  Connect.</br>  **Note:** Since the Connect API requires </br> each array element to be Base64 encoded,</br>  the SDK will do so before </br>  making the API request.</br>    This parameter is only required for </br>  creating an unsigned chain</br>  (`automatic_signing` is set to `false`). | **at least 1 external_id is required.** </br> `external_ids` parameter was not </br>  provided when `automatic_signing` </br> was set to `false`. </br>**external_ids must be an array.**</br>  An invalid `external_ids` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `content`          | required                               | string </br>  This is the data that will make up the first </br>  entry in your new chain. It is customary </br> to use this space to describe the entries that </br>  are to follow in the chain.</br> **Note:** Since the Connect API requires the </br> `content` to be Base64 encoded, the SDK </br> will do so before making the API request.                                                                                                   | **content is required.**</br>    `content` parameter was not provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `signer_chain_id`    | required </br> or </br> optional </br> | string </br> The chain id of the signer identity.</br> **Note:** This parameter is optional for </br>creating an unsigned chain. </br> However, if `signer_private_key` is inputted </br> then `signer_chain_id` must also be inputted.                                                                                                                                                                                                                    | In case of creating a signed chain: </br> **signer_chain_id is required.** </br> `signer_chain_id` parameter was not provided. </br>  In case of creating an unsigned chain:  **signer_chain_id is required** </br> **when passing a signer_private_key.**   `signer_private_key` parameter was provided </br> but lacking `signer_chain_id` parameter.                                                                                                                                                                                                                                                                                                                                       |
| `signer_private_key` | required </br> or </br> optional </br> | base58 string in Idsec format</br> The private key signer would like to sign </br>  with. In fact, private key is used to </br>  generate the public key, which is included </br> as an external ID on the created signed entry. </br> **Note:** This parameter is optional for </br>  creating an unsigned chain. However, if </br> `signerChainId` is inputted then `signer_private_key` must also be inputted.                                     | In case of creating a signed chain:</br> **signer_private_key is required.**</br> `signer_private_key` parameter was not provided.</br>  **signer_private_key is invalid.** </br> An invalid `signer_private_key` parameter was </br> provided or key’s byte length is not equal to 41. </br> In case of creating an unsigned chain: </br> **signer_private_key is required when passing a signer_chain_id.** </br>   `signer_chain_id` parameter was provided but lacking </br> `signer_private_key` parameter.  </br>  **signer_private_key is invalid.**  `signer_chain_id` was provided but either an invalid </br> `signer_private_key` parameter was also provided </br> or key’s byte length is not equal to 41. |
| `callback_url`      | optional                               | string </br> The URL where you would like to receive the callback  </br>from Connect. </br> **Note:** If this is not specified, callbacks </br> will not be activated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | **callback_url is an invalid url format.** </br> An invalid `callbackUrl` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `callback_stages`   | optional                               | array of strings </br> The immutability stages you would like to be notified about.  </br> This list can include any or all of the three  </br> stages: `replicated`, `factom`, and </br> `anchored`. For example, when you </br> would like to trigger the callback from </br> Connect at `replicated` and `factom` </br> stage, you would send them in the </br> format: [‘replicated’, ‘factom’]. </br> **Note:** For this field to matter, the URL </br> must be provided. </br> If callbacks are activated (URL has </br> been specified) and this field is not </br> sent, it will default to `factom` and </br> `anchored`. | **callback_stages must be an array.** </br> An invalid `callback_stages` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

**Returns**

**Response**: Accepted

-   **chain_id:** string </br> This is the unique identifier created for each chain.  </br>**Note:** Chain ID is a hash based on the external IDs you choose. External IDs must be unique or else the chain creation will fail.
-   **entry_hash:** string </br> The SHA256 Hash of the first entry of this new chain.
-   **stage:** string </br> The immutability stage that this chain has reached.

#### list

Gets all of the chains on Factom.

**Parameters**

| **Name**        | **Type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                | **SDK Error Message & Description**                                            |   |
|-----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|---|
| `limit`  | optional | integer </br>  The number of items you would like to </br> return back in each stage. The default value </br>  is 15.                                                                                                                                                                                                                                                                          | **limit must be an integer.**</br>   An invalid `limit` format was </br> provided.  |   |
| `offset` | optional | integer </br>  The offset parameter allows you to select </br> which item you would like to start from </br> when a list is returned from Connect. </br> For example, if you have already seen the </br> first 15 items and you would like the next set,</br>  you would send an offset of 15. `offset=0` starts </br> from the first item of the set and is the default</br>  position.   | **offset must be an integer.**  </br>  An invalid `offset` format was </br> provided. |   |
| `stages` | optional | array of strings </br>  The immutability stages you want to </br> restrict results to. You can choose any </br>  from `replicated`, `factom`, and `anchored`. </br> The default value are these three stages: </br> `replicated`, `factom`, and `anchored`. </br>  **Note**: If you would like to search among</br> multiple stages, you would send them in </br> the format: [‘replicated’, ‘factom’]. | **stages must be an array.**</br>  An invalid `stages` format was </br> provided.   |   |


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

| **Name**             | **Type** | **Description**                                                                                                                                                                                                                                                                                                                                                                            | **SDK Error Message & Description**                                                                                                                                                        |   |
|----------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|
| `external_ids` | required | array of strings </br>  A list of external IDs associated with the </br> chains user would like to search by.                                                                                                                                                                                                                                                                              | **at least 1 external_ids is required.**</br>  `external_ids` parameter was not provided.</br>   **external_ids must be an array.** </br>  An invalid `external_ids` format was </br> provided. |   |
| `limit`       | optional | integer </br> The number of items you would like to </br> return back in each stage. The default value</br> is 15.                                                                                                                                                                                                                                                                             | **limit must be an integer.** </br> An invalid `limit` format was </br> provided.                                                                                                          |   |
| `offset`      | optional | integer </br>  The offset parameter allows you to select </br> which item you would like to start from </br> when a list is returned from Connect. </br> For example, if you have already seen the </br> first 15 items and you would like the next set,</br> you would send an offset of 15. `offset=0` starts </br> from the first item of the set and is the default</br> position. | **offset must be an integer.**</br>  An invalid `offset` format was </br>  provided.                                                                                                       |   |


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
| `chain_id`             | required | string </br>  The chain identifier.                                                                                                                                                                                                                                                                                    | **chain_id is required.**</br>  `chain_id` parameter was not provided.</br>      |
| `entry_hash`           | required | string </br> The SHA256 hash of the entry.                                                                                                                                                                                                                                                                             | **entry_hash is required.** </br> `entry_hash` parameter was not </br> provided. |
| `signature_validation` | optional | boolean (`true`/`false`/`custom function`) </br>  The default value is `true`. </br> Indicates whether the SDK </br> automatically validates that the entry </br> was signed based on our signing standard. </br> `custom function`: allows for </br> validating the entry's signature </br> based on custom logic.</br> |                                                                                |


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
| `external_ids`      | required</br>  or</br>  optional | array of strings </br> Tags that can be used to identify your</br> entry. You can search for records that</br>  contain a particular external ID using</br>  Connect.</br>  **Note:** Since the Connect API requires</br>  each array element to be Base64</br>  encoded, the SDK will do so before</br>  making the API request.</br>  This parameter is only required for</br>   creating an unsigned entry</br>  (`automatic_signing` is set to `false`).</br>                                                                                                                                                           | **at least 1 external_id is required.**</br> `external_ids` parameter was not</br>  provided when `automatic_signing` is</br> set to `false`.</br>  **external_ids must be an array.**</br>  An invalid `external_ids` format was</br>  provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `content`          | required                         | string</br> This is the data that will be stored directly</br>  on the blockchain. Please be sure that no</br>  private information is entered here.</br>   **Note:** The value in `content` parameter will</br>  be encoded in Base64 format by Connect</br>  SDK.                                                                                                                                                                                                                                                                                                                                                        | **content is required.**</br>   `content` parameter was not provided.</br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `signer_chain_id`    | required</br> or</br> optional   | string</br> The chain ID of the signer identity.</br>  **Note:** This parameter is optional for</br>  creating an unsigned entry.</br>  However, if `signer_private_key` is inputted</br>  then `signer_chain_id` must also be inputted.                                                                                                                                                                                                                                                                                                                                                                                       | In case of creating a signed entry:</br> **signer_chain_id is required.**</br> `signer_chain_id` parameter </br> was not provided.</br>  In case of creating an unsigned entry:</br>  **signer_chain_id is</br> required when passing a</br> signer_private_key.**</br> `signer_private_key` was</br>  provided but lacking</br>  `signer_chain_id` parameter.                                                                                                                                                                                                                                                                                                                                                                                                   |
| `signer_private_key` | required</br>  or</br>  optional | a base58 string in Idsec format</br> The private key signer would like to sign</br>  with. In fact, private key is used to</br>  generate the public key, which is included</br>  as an external ID on the created signed</br>  entry.</br>   **Note:** This parameter is optional for</br>   creating an unsigned entry.</br>  However, if `signer_chain_id` is inputted</br>  then `signer_private_key` must also be inputted.                                                                                                                                                                                               | In case of creating a signed entry:</br>  **signer_private_key is required.**</br> `signer_private_key` parameter </br> was not provided.</br>  **signer_private_key is invalid.**</br> An invalid</br>  `signer_private_key`</br>  parameter was provided</br>  or key's byte length is not</br> equal to 41. </br>  In case of creating an unsigned</br>  entry:</br>  **signer_private_key is</br> required when passing a</br> signer_chain_id.**</br> `signer_chain_id` was</br>  provided but lacking</br>  `signer_private_key`</br>  parameter.</br>  **signer_private_key is invalid.**</br>  `signer_chain_id` was</br>  provided but an invalid</br>  `signer_private_key`</br> parameter was provided</br> or key's byte length is not</br> equal to 41.</br>  |
| `callback_url`      | optional                         | string</br> the URL you would like the callbacks to</br> be sent to</br> **Note:** If this is not specified, callbacks will</br> not be activated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | **callback_url is an invalid url</br> format.**</br> An invalid `callback_url` format</br>  was provided </br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `callback_stages`   | optional                         | array of strings</br>  The immutability stages you would like to</br>  be notified about. This list can include any</br> or all of these three stages: `replicated`,</br>  `factom`, and `anchored`. For example,</br>  when you would like to trigger the</br>  callback from Connect from `replicated`</br> and `factom` then you would send them in</br> the format: ['replicated', 'factom'].</br> **Note:** For this field to matter, the URL</br> must be provided.</br> If callbacks are activated (URL has</br> been specified) and this field is not</br> sent, it will default to `factom` and</br> `anchored`. | **callback_stages must be an array.**</br> An invalid `callback_stages` format </br>  was provided </br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |


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
| `limit`   | optional | integer </br> The number of items you would like back</br> in each page. The default value is 15.</br>                                                                                                                                                                                                                                                                                          | **limit must ben an integer.**</br> An invalid `limit` format was</br>  provided.</br>  |
| `offset`  | optional | integer</br> The offset parameter allows you to select</br> which item you would like to start from</br> when a list is returned from</br>  Connect. For example, if you have</br>  already seen the first 15 items and you</br>  would like the next set, you would send</br>  an offset of 15. `offset=0` starts from the</br>  first item of the set and is the default</br>  position. | **offset must be an integer.**</br> An invalid `offset` format was</br>  provided.</br> |
| `stages`  | optional | array of strings</br> The immutability stages you want to</br>  restrict results to. You can choose any</br>  from `replicated`, `factom`, and `anchored`.</br>  The default value are these three stages:</br>  `replicated`, `factom` and `anchored`.</br>  **Note:** If you would like to search among</br>  multiple stages, you would send them in</br>  the format ['replicated', 'factom'].  | **stages must be an array.**</br>  An invalid `stages` format was</br>   provided.</br> |

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
| `signature_validation` | optional | boolean (`true`/`false`/`custom function`)</br> Default value is `true`.</br>  Indicates whether the SDK</br> automatically validates that the entry</br> was signed based on our signing</br>  standard.</br>   `custom function`: allows for validating</br> the entry's signature based on custom</br>  logic. |                                                                           |

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
| `signature_validation` | optional | boolean (`true`/`false`/`custom function`)</br> Default value is `true`.</br>  Indicates whether the SDK</br> automatically validates that the entry</br> was signed based on our signing</br>  standard.</br>   `custom function`: allows for validating</br> the entry's signature based on custom</br>  logic. |                                                                           |

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
| `external_ids` | required | array of strings</br> A list of external IDs.</br> **Note:** Since the Connect API requires</br>  each array element to be Base64</br>  encoded, the SDK will do so before</br>  making the API request.                                                                                                                                                                                   | **at least 1 external_id is required.**</br> `external_ids` parameter was not provided. </br>  **external_ids must be an array.**</br> An invalid `external_ids`parameter was provided. |
| `limit`       | optional | integer</br> The number of items you would like to</br>  return back in each page. The default value is</br>  15.                                                                                                                                                                                                                                                                              | **limit must be an integer.**</br> An invalid `limit` format was provided.</br>                                                                                                      |
| `offset`      | optional | integer</br> The offset parameter allows you to select</br>  which item you would like to start from</br>  when a list is returned from</br>  Connect. For example, if you have</br>  already seen the first 15 items and you</br>  would like the next set, you would send</br>  an offset of 15. `offset=0` starts from the</br>  first item of the set and is the default</br>  position. | **offset must be an integer.**</br>  An invalid `offset` format was provided.</br>                                                                                                   |

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