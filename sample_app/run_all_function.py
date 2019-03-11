# import module located on a parent folder, when you don't have a standard package structure
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib  # noqa
import datetime  # noqa
import json  # noqa
import sample_app.configure  # noqa
from factom_sdk import FactomClient  # noqa

factom_client = FactomClient(sample_app.configure.BASE_URL,
                             sample_app.configure.APP_ID,
                             sample_app.configure.APP_KEY)

print("=================INFO=================")
print("factom_client.api_info.get")
factom_client.api_info.get()

print("=================IDENTITIES=================")
print("factom_client.identities.create")
create_identity_chain_response = factom_client.identities.create(
    ["NotarySimulation", datetime.datetime.utcnow().isoformat()])
original_key_pairs = create_identity_chain_response["key_pairs"]
identity_chain_id = create_identity_chain_response["chain_id"]
key_to_sign = original_key_pairs[2]

print("factom_client.identities.get")
factom_client.identities.get(identity_chain_id)

# Temporary comment
print("factom_client.identities.keys.get")
# factom_client.identities.keys.get(identity_chain_id, key_to_sign["public_key"])

print("factom_client.identities.keys.list")
factom_client.identities.keys.list(identity_chain_id)

print("factom_client.identities.keys.replace")
replace_key_pairs = [factom_client.utils.generate_key_pair() for _ in range(3)]
replacement_entry_responses = []
for i in range(len(replace_key_pairs)):
    new_key_pair = replace_key_pairs[i]
    original_key_pair = original_key_pairs[i]
    replacement_entry_responses.append(factom_client.identities.keys.replace(identity_chain_id,
                                                                             original_key_pair["public_key"],
                                                                             new_key_pair["public_key"],
                                                                             original_key_pair["private_key"]))

print("=================CHAINS=================")
print("factom_client.chains.create")
create_chain_response = factom_client.chains.create(
    "This chain represents a notary service's customer in the NotarySimulation, a sample implementation provided as"
    " part of the Factom Harmony SDKs. Learn more here: https://docs.harmony.factom.com/docs/sdks-clients",
    signer_chain_id=identity_chain_id,
    external_ids=["NotarySimulation", "CustomerChain", "cust123"],
    signer_private_key=key_to_sign["private_key"]
)
chain_id = create_chain_response["chain_id"]

print("factom_client.chains.get")
factom_client.chains.get(chain_id)

print("factom_client.chains.list")
factom_client.chains.list()

print("factom_client.chains.search")
factom_client.chains.search(["TestFunction", "CustomerChain", "cust123"])

print("=================ENTRIES=================")
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

print("factom_client.chains.entries.create")
create_entry_response = factom_client.chains.entries.create(chain_id=chain_id,
                                                            signer_private_key=key_to_sign["private_key"],
                                                            signer_chain_id=identity_chain_id,
                                                            external_ids=["NotarySimulation",
                                                                          "DocumentEntry",
                                                                          "doc987"],
                                                            content=json.dumps({"document_hash": document_hash,
                                                                                "hash_type": "sha256"
                                                                                })
                                                            )
entry_hash = create_entry_response["entry_hash"]

print("factom_client.chains.entries.get")
factom_client.chains.entries.get(chain_id, entry_hash)

print("factom_client.chains.entries.list")
factom_client.chains.entries.list(chain_id)

print("factom_client.chains.entries.get_first")
factom_client.chains.entries.get_first(chain_id)

print("factom_client.chains.entries.get_last")
factom_client.chains.entries.get_last(chain_id)

print("factom_client.chains.entries.search")
factom_client.chains.entries.search(chain_id, ["NotarySimulation",
                                               "DocumentEntry",
                                               "doc987"])
