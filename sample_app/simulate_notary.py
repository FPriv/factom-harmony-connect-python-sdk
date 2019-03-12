# import module located on a parent folder, when you don't have a standard package structure
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib  # noqa
import datetime  # noqa
import json  # noqa
import sample_app.configure  # noqa
from factom_sdk import FactomClient  # noqa


def calculate_state(identities_keys):
    result = []
    for item in identities_keys["active_keys"]:
        if item["activated_height"] is None:
            # "Pending and Replacement Pending" if activated_height is null
            # and there is a pending key replacement for the same priority
            if identities_keys["pending_key"] is not None \
                    and item["priority"] == identities_keys["pending_key"]["priority"]:
                state = "Pending and Replacement Pending"
            else:
                # "Pending" if the activated height is null
                state = "Pending"
        else:
            # "Retired/replaced" if retired_height is not null
            if item["retired_height"] is not None:
                state = "Retired/replaced"
            else:
                # "Active and Replacement Pending" if activated_height is not null
                # retired_height is null and there is a pending key replacement for the same priority
                if identities_keys["pending_key"] is not None \
                        and item["priority"] == identities_keys["pending_key"]["priority"]:
                    state = "Active and Replacement Pending"
                else:
                    # "Active" if activated_height is not null and retired_height is null
                    state = "Active"
        result.append({
            "key": item["key"],
            "priority": item["priority"],
            "activated_height": item["activated_height"],
            "state": state
        })
    if identities_keys["pending_key"] is not None:
        result.append({
            "key": identities_keys["pending_key"]["key"],
            "priority": identities_keys["pending_key"]["priority"],
            "activated_height": identities_keys["pending_key"]["activated_height"],
            "state": "Pending"
        })
    result.sort(key=lambda x: x["priority"])
    return result


def simulate_notary():
    factom_client = FactomClient(sample_app.configure.BASE_URL,
                                 sample_app.configure.APP_ID,
                                 sample_app.configure.APP_KEY)

    # Create identity without key. System automatic generating 3 key pairs
    create_identity_chain_response = factom_client.identities.create(
        ["NotarySimulation", datetime.datetime.utcnow().isoformat()])
    original_key_pairs = create_identity_chain_response["key_pairs"]

    # We'll use this later for sign chain/entry
    identity_chain_id = create_identity_chain_response["chain_id"]

    # In this sample we will use the identity’s lowest priority key to sign
    key_to_sign = original_key_pairs[2]

    # Create a chain, by default the chain will be signed
    # You need to pass in the private key and the identity chain id
    create_chain_response = factom_client.chains.create(
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
    chain = factom_client.chains.get(create_chain_response["chain_id"], signature_validation=False)
    chain_created_time = chain["data"]["external_ids"][5]

    # This is the document from the customer,
    # It should be stored in a secure location such as an Amazon S3 bucket for later retrieval.
    # The blockchain is your means for ensuring it has not been tampered with.
    document_hash = hashlib.sha256()
    with open("./static/Factom_Whitepaper_v1.2.pdf", 'rb') as afile:
        buf = afile.read(65536)
        while len(buf) > 0:
            document_hash.update(buf)
            buf = afile.read(65536)
        document_hash = document_hash.hexdigest()

    document = {
        "link": "/document",
        "hash": document_hash
    }

    # Create an entry, by default the chain will be signed
    # So you need to pass in the private key and the identity chain id

    create_entry_response = factom_client.chains.entries.create(chain_id=chain["data"]["chain_id"],
                                                                signer_private_key=key_to_sign["private_key"],
                                                                signer_chain_id=identity_chain_id,
                                                                external_ids=["NotarySimulation",
                                                                              "DocumentEntry",
                                                                              "doc987"],
                                                                content=json.dumps({"document_hash": document_hash,
                                                                                    "hash_type": "sha256"
                                                                                    })
                                                                )

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
    get_entry_response = factom_client.chains.entries.get(chain["data"]["chain_id"],
                                                          create_entry_response["entry_hash"], False)
    entry_created_time = get_entry_response["data"]["external_ids"][5]

    # Search chain
    # Currently we only have 1 identity_chain_id to work with so pass in chain_created_time
    # to make sure search function only return one result
    chain_search_input = [identity_chain_id, "cust123", chain_created_time]
    chain_search_result = factom_client.chains.search(chain_search_input)

    # Get Chain with signature validation
    # by default all get chain/entry request will be automatically validating the signature
    chain_w_validation = factom_client.chains.get(chain_search_result["data"][0]["chain_id"])

    # Search entry
    # Currently we only have 1 identity_chain_id to work with so pass in entry_created_time
    # to make sure search function only return one result
    entry_search_input = ["DocumentEntry", "doc987", entry_created_time]
    entry_search_result = factom_client.chains.entries.search(chain_w_validation["chain"]["data"]["chain_id"],
                                                              entry_search_input)

    # Retrieve Blockchain Data aren't always necessary
    # because it is common practice to store the chain_id and entry_hash within your own database.
    # Get Entry with signature validation
    # by default all get chain/entry request will be automatically validating the signature
    entry_w_validation = factom_client.chains.entries.get(chain_w_validation["chain"]["data"]["chain_id"],
                                                          entry_search_result["data"][0]["entry_hash"])
    entry_content_json = entry_w_validation["entry"]["data"]["content"]

    # This is the document that was stored in your system
    # and you are now retrieving to verify that it has not been tampered with.
    document_hash_after = hashlib.sha256()
    with open("./static/Factom_Whitepaper_v1.2.pdf", 'rb') as afile:
        buf = afile.read(65536)
        while len(buf) > 0:
            document_hash_after.update(buf)
            buf = afile.read(65536)
        document_hash_after = document_hash_after.hexdigest()

    document_after = {
        "link": "/document",
        "hash": document_hash_after
    }

    # Proactive Security
    # To replace new key, you need to sign this request with above or same level private key.
    # In this case we are using same level private key.
    original_key_pair = original_key_pairs[1]
    replacement_entry_response = factom_client.identities.keys.replace(identity_chain_id,
                                                                       original_key_pair["public_key"],
                                                                       None,
                                                                       original_key_pair["private_key"])

    identity_chain = factom_client.identities.get(identity_chain_id)
    identity_keys = calculate_state({
        "active_keys": identity_chain["data"]["active_keys"],
        "pending_key": identity_chain["data"]["pending_key"]
    })

    return {
        "originalKeyPairs": original_key_pairs,
        "identityChainId": identity_chain_id,
        "document": document,
        "createdChainInfo": {
            "externalIds": chain["data"]["external_ids"],
            "chainId": chain["data"]["chain_id"]
        },
        "createdEntryInfo": {
            "externalIds": get_entry_response["data"]["external_ids"],
            "entryHash": get_entry_response["data"]["entry_hash"]
        },
        "chainSearchInput": chain_search_input,
        "chainSearchResult": chain_search_result["data"],
        "chainWValidation": {
            "chainId": chain_w_validation["chain"]["data"]["chain_id"],
            "externalIds": chain_w_validation["chain"]["data"]["external_ids"],
            "status": chain_w_validation["status"]
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
        "replaceKeyPair": replacement_entry_response["key_pair"],
        "replacementEntryResponse": replacement_entry_response,
        "identityKeys": identity_keys
    }
