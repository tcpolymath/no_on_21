from beem import Steem
from beem.blockchain import Blockchain
from beem.instance import set_shared_steem_instance
from beem.nodelist import NodeList
from beem.comment import Comment
from beem.account import Account
from beem.witness import Witness, WitnessesRankedByVote, WitnessesVotedByAccount
import time
import requests
import json

nodes = NodeList()
nodes.update_nodes()
steem = Steem(node=nodes.get_nodes())
set_shared_steem_instance(steem)
steem.wallet.unlock("YOUR BEEMPY PASSWORD HERE")
account = "YOUR USERNAME HERE"

print "Initialized"
while(1):
        i = 0
        votedlist = WitnessesVotedByAccount(account)
        for witness in votedlist:
                if "1111111111111111111" in witness["signing_key"]:
                        print "%s unsigned, unvoting" % witness["owner"]
                        Account(account).disapprovewitness(witness["owner"])
                elif "0.21" in witness["running_version"]:
                        print "Unvoting %s: %s" % (witness["owner"], witness["running_version"])
                        Account(account).disapprovewitness(witness["owner"])
                else:
                        i += 1
        for witness in WitnessesRankedByVote():
                if i > 29:
                        break
                if "1111111111111111111" in witness["signing_key"]:
                        continue
                if "0.20" in witness["running_version"]:
                        if witness["owner"] in votedlist:
                                continue
                        print "Voting for %s: %s" % (witness["owner"], witness["running_version"])
                        Account(account).approvewitness(witness["owner"])
                        i += 1
        time.sleep(300)

