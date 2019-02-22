# import module located on a parent folder, when you don't have a standard package structure
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
import datetime
import json
from factom_sdk import FactomClient


def simulate_notary():
    factom_client = FactomClient("https://durable.sandbox.harmony.factom.com/v1/", "aabe7d81",
                                 "502a5c77f8f600b9ec32e94fbe008f11")

    # Create initial key pairs, sdk will create 3 key pairs by default
    # You can change the number of key pair by passing number_of_key_pair=3 to the params
    # Create single key pair by using factom_client.key_util.create_key_pair()
    original_key_pairs = factom_client.identity.create_identity_key_pair()

    # For now Identity API is not completed so hardcoded 3 key pairs from API document
    original_key_pairs = [
        {
            "private_key": "idsec1rxvt6BX7KJjaqUhVMQNBGzaa1H4oy43njXSW171HftLnTyvhZ",
            "public_key": "idpub2Cktw6EgcBVMHMXmfcCyTHndcFvG7fJKyBpy3sTYcdTmdTuKya"
        },
        {
            "private_key": "idsec2bH9PmKVsqsGHqBCydjvK6BESQNQY7rqErq1EAV84Tx3NWRiyb",
            "public_key": "idpub2JegfdBQBnqbXGKMMD89v8N81e4DpvERHWTJp6zvWaoAVi8Jnj"
        },
        {
            "private_key": "idsec35TeMDfgZMfTzinqEqHxt4BFLSAbwQBwsZeXmFG3otjfkDBF8u",
            "public_key": "idpub2SrEYac7YQd6xQJKHt7hMWTgzBLDeyPYsK9jwJyQx5bfZvcxE9"
        }
    ]

    public_keys = [val["public_key"] for val in original_key_pairs]

    # Create identity with original_key_pairs created above
    create_indentity_chain_response = factom_client.identity.create_identity(
        ["NotarySimulation", datetime.datetime.utcnow().isoformat()], public_keys)

    # We'll use this later for sign chain/entry
    identity_chain_id = create_indentity_chain_response["chain_id"]

    # In this sample we will use the identity’s lowest priority key to sign
    key_to_sign = original_key_pairs[2]

    # Create a chain, by default the chain will be signed
    # You need to pass in the private key and the identity chain id
    create_chain_response = factom_client.chains.create_chain(
        "This chain represents a notary service's customer in the NotarySimulation, a sample implementation provided as"
        " part of the Factom Harmony SDKs. Learn more here: https://docs.harmony.factom.com/docs/sdks-clients",
        signer_chain_id=identity_chain_id,
        external_ids=["NotarySimulation", "CustomerChain", "cust123"],
        signer_private_key=key_to_sign["private_key"]
    )

    # Get chain info to show external Ids have been passed to the API.
    # External Ids processed by SDK automatically when creating new chain/entry. External Ids will include:
    # [
    #  "Chain Type",
    #  "Chain Schema Version",
    #  "Your Identity Chain ID",
    #  "Signature Public Key"
    #  "Signature"
    #  "Time stamp"
    #  "Additional external Ids"
    # ]
    # In order to display the External Ids array then we need to get chain. However, we don't need
    # to validate the signature so in this step pass in signature_validation=False
    chain = factom_client.chain(create_chain_response["chain_id"], signature_validation=False)
    chain_created_time = chain.data["external_ids"][5]

    # This is the document from the customer,
    # It should be stored in a secure location such as an Amazon S3 bucket for later retrieval.
    # The blockchain is your means for ensuring it has not been tampered with.
    with open("./static/Factom_Whitepaper_v1.2.pdf", 'rb') as afile:
        buf = afile.read(65536)
        hasher = hashlib.sha256()
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(65536)
        document_hash = hasher.hexdigest()

    document = {
        "link": "/document",
        "hash": document_hash
    }

    # Create an entry, by default the chain will be signed
    # So you need to pass in the private key and the identity chain id

    create_entry_response = chain.create_entry(signer_private_key=key_to_sign["private_key"],
                                               signer_chain_id=identity_chain_id,
                                               external_ids=["NotarySimulation", "DocumentEntry", "doc987"],
                                               content=json.dumps({
                                                   "document_hash": document_hash,
                                                   "hash_type": "sha256"
                                               }))

    # Get entry info to show external Ids have been passed to the API.
    # External Ids processed by SDK automatically when creating new entry. External Ids will include:
    # [
    #  "Entry Type",
    #  "Entry Schema Version",
    #  "Your Identity Chain ID",
    #  "Signature Public Key"
    #  "Signature"
    #  "Time stamp"
    #  "Additional external Ids"
    # ]
    # In order to display the External Ids array then we need to get entry. However, we don't need
    # to validate the signature so in this step pass in signature_validation=False
    get_entry_response = chain.get_entry_info(create_entry_response["entry_hash"], signature_validation=False)
    entry_created_time = get_entry_response["data"]["external_ids"][5]

    # Search chain
    # Currently we only have 1 identity_chain_id to work with so pass in chain_created_time
    # to make sure search function only return one result
    chain_search_input = [identity_chain_id, "cust123", chain_created_time]
    chain_search_result = factom_client.chains.search_chains(chain_search_input)

    # Get Chain with signature validation
    # by default all get chain/entry request will be automatically validating the signature
    chain_w_validation = factom_client.chain(chain_search_result["data"][0]["chain_id"])

    # Search entry
    # Currently we only have 1 identity_chain_id to work with so pass in entry_created_time
    # to make sure search function only return one result
    entry_search_input = ["DocumentEntry", "doc987", entry_created_time]
    entry_search_result = chain_w_validation.search_entries(entry_search_input)

    # Retrieve Blockchain Data aren't always necessary
    # because it is common practice to store the chain_id and entry_hash within your own database.
    # Get Entry with signature validation
    # by default all get chain/entry request will be automatically validating the signature
    entry_w_validation = chain_w_validation.get_entry_info(entry_search_result["data"][0]["entry_hash"])
    entry_content_json = entry_w_validation["entry"]["data"]["content"]

    # This is the document that was stored in your system
    # and you are now retrieving to verify that it has not been tampered with.
    with open("./static/Factom_Whitepaper_v1.2.pdf", 'rb') as afile:
        buf = afile.read(65536)
        hasher = hashlib.sha256()
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(65536)
        document_hash_after = hasher.hexdigest()

    document_after = {
        "link": "/document",
        "hash": document_hash_after
    }

    # Proactive Security
    replace_key_pairs = factom_client.identity.create_identity_key_pair()

    # To replace new key, you need to sign this request with above or same level private key.
    # In this case we are using same level private key.
    replacement_entry_responses = []
    for i in range(len(replace_key_pairs)):
        new_key_pair = replace_key_pairs[i]
        original_key_pair = original_key_pairs[i]
        replacement_entry_responses.append(factom_client.identity.create_identity_key_replacement(identity_chain_id,
                                                                                                  original_key_pair[
                                                                                                      "public_key"],
                                                                                                  new_key_pair[
                                                                                                      "public_key"],
                                                                                                  original_key_pair[
                                                                                                      "private_key"]))

    identity_keys = factom_client.identity.get_all_identity_keys(identity_chain_id)

    return {
        "originalKeyPairs": original_key_pairs,
        "identityChainId": identity_chain_id,
        "document": document,
        "createdChainInfo": {
            "externalIds": chain.data["external_ids"],
            "chainId": chain.data["chain_id"]
        },
        "createdEntryInfo": {
            "externalIds": get_entry_response["data"]["external_ids"],
            "entryHash": get_entry_response["data"]["entry_hash"]
        },
        "chainSearchInput": chain_search_input,
        "chainSearchResult": chain_search_result["data"],
        "chainWValidation": {
            "chainId": chain_w_validation.data["chain_id"],
            "externalIds": chain_w_validation.data["external_ids"],
            "status": chain_w_validation.status
        },
        "entrySearchInput": entry_search_input,
        "searchEntryResults": entry_search_result,
        "entryWValidation": {
            "entryHash": entry_w_validation["entry"]["data"]["entry_hash"],
            "external_ids": entry_w_validation["entry"]["data"]["external_ids"],
            "content": entry_w_validation["entry"]["data"]["content"],
            "status": entry_w_validation["status"],
            "entryContentJSON": entry_content_json,
        },
        "documentAfter": document_after,
        "replaceKeyPairs": replace_key_pairs,
        "replacementEntryResponses": replacement_entry_responses,
        "identityKeys": identity_keys
    }
