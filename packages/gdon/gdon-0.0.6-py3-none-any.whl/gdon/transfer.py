import os
import json
import datetime

from duniterpy.key import SigningKey, ascii_armor

from gdon.diceware import diceware
from gdon.silkaj.money import get_amount_from_pubkey
from gdon.silkaj.tx import handle_intermediaries_transactions
from gdon.silkaj.tools import coroutine
from gdon.constants import COMMENT

class Transfer:
    """Create a transfer wallet, send amount to tips"""

    def __init__(self, amount, pages, wallets, peremption_date):
        self.wallets = wallets
        self.pages = pages
        self.Tips_Amount = amount
        self.date = peremption_date


    @coroutine
    async def transfer(self, key):
        """
        sends tips.
        """
        total_amount = int(100 * self.Tips_Amount * 6 * self.pages)
        # create outputs list
        outputAddresses = []
        for w in self.wallets:
            outputAddresses.append (w["pubkey"])
        # send to tips
        outputbackchange = None
        amount_tx = int (self.Tips_Amount * 100)
        tx_amount = list()
        tx_amount.append(amount_tx)
        issuers = key.pubkey
        await handle_intermediaries_transactions(
            key,
            issuers,
            tx_amount,
            total_amount,
            outputAddresses,
            COMMENT,
            outputbackchange,
        )

