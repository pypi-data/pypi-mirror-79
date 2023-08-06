"""
Copyright  2016-2019 Maël Azimi <m.a@moul.re>

Silkaj is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Silkaj is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with utils.silkaj. If not, see <https://www.gnu.org/licenses/>.
"""

from re import compile, search
import math
from time import sleep
#from click import command, option, FloatRange

#from tabulate import tabulate
from gdon.silkaj.network_tools import ClientInstance, HeadBlock
from gdon.silkaj.crypto_tools import check_public_key
from gdon.silkaj.tools import message_exit, CurrencySymbol, coroutine
from gdon.silkaj.auth import auth_method
#from gdon.silkaj.wot import is_member
from gdon.silkaj.money import (
    get_sources,
    get_amount_from_pubkey,
    UDValue,
    amount_in_current_base,
)
from gdon.silkaj.constants import SOURCES_PER_TX

from duniterpy.api.bma.tx import process
from duniterpy.documents import BlockUID, Transaction
from duniterpy.documents.transaction import OutputSource, Unlock, SIGParameter

# max size for tx doc is 100 lines. Formula for accepted field numbers is : (2 * IU + 2 * IS + O) <= ( MAX_LINES - FIX_LINES)
# with IU = inputs/unlocks ; IS = Issuers/Signatures ; O = Outouts.
MAX_LINES_IN_TX_DOC = 100
# 2 lines are necessary, and we block 1 more for the comment
FIX_LINES = 3
# assuming there is only 1 issuer and 2 outputs, max inputs is 46
MAX_INPUTS_PER_TX = 46
# assuming there is 1 issuer and 1 input, max outputs is 93.
MAX_OUTPUTS = 93


"""
#@command("tx", help="Send transaction")
#@option(
    "--amount",
    help="Quantitative value(s) : <value_1>:<value_2>:... If only one amount, it will be sent to all recipients.",
)
#@option(
    "--amountUD",
    help="Relative value(s) : <UDvalue_1>:<UDvalue_2>... If only one amount, it will be sent to all recipients.",
)
#@option("--allSources", is_flag=True, help="Send all sources")
#@option(
    "--output",
    required=True,
    help="Pubkey(s)’ recipients + optional checksum: <pubkey>[!checksum]:[<pubkey>[!checksum]]",
)
#@option("--comment", default="", help="Comment")
#@option(
    "--outputBackChange",
    help="Pubkey recipient to send the rest of the transaction: <pubkey[!checksum]>",
)
#@option("--yes", "-y", is_flag=True, help="Assume yes. Do not prompt confirmation")
"""

@coroutine
async def send_transaction(
    amount, amountud, allsources, output, comment, outputbackchange, yes
):
    """
    Main function
    """
    tx_amount = await transaction_amount(amount, amountud, allsources)
    key = auth_method()
    issuer_pubkey = key.pubkey

    pubkey_amount = await get_amount_from_pubkey(issuer_pubkey)
    outputAddresses = output.split(":")
    totalAmount = total_amount(tx_amount, outputAddresses)
    if allsources:
        tx_amount = list(pubkey_amount[0])
    check_transaction_values(
        comment,
        outputAddresses,
        outputbackchange,
        pubkey_amount[0] < totalAmount,
        issuer_pubkey,
    )

    if (
        yes
        or input(
            tabulate(
                await transaction_confirmation(
                    issuer_pubkey,
                    pubkey_amount[0],
                    tx_amount,
                    totalAmount,
                    outputAddresses,
                    outputbackchange,
                    comment,
                ),
                tablefmt="fancy_grid",
            )
            + "\nDo you confirm sending this transaction? [yes/no]: "
        )
        == "yes"
    ):
        await handle_intermediaries_transactions(
            key,
            issuer_pubkey,
            tx_amount,
            totalAmount,
            outputAddresses,
            comment,
            outputbackchange,
        )


def total_amount(tx_amount, outputAddresses):
    """
    Return total amount of transaction
    """
    if len(tx_amount) != len(outputAddresses) and len(tx_amount) != 1:
        message_exit(
            "--output list and --amount or --amoundUD list are not of same length"
        )
    if len(tx_amount) == 1:
        if isinstance(outputAddresses, str):
            total = tx_amount[0]
        else :
            total = tx_amount[0] * len(outputAddresses)
    if len(tx_amount) > 1:
        total = sum(tx_amount)
    return total


async def transaction_amount(amount, amountUD, allSources):
    """
    Check command line interface amount option
    Return transaction amounts (list)
    """
    if not (amount or amountUD or allSources):
        message_exit("--amount nor --amountUD nor --allSources is set")
    amounts = list()
    if amount:
        for amount in amount.split(":"):
            amount = round(float(amount) * 100)	# , -2) ## CAUTION ! "-2" is for testing purpose, on GTest. Change to `round ( float(amount) *100 )`
            amounts.append(amount)
        return amounts

    if amountUD:
        for amount in amountUD.split(":"):
            amount = round(
                float(amount) * await UDValue().ud_value)	# , -2)
#            )  # DEBUG : ", -1"  est pour GTest, à enlever ! # ajouter la gestion de UnitBase ?
            amounts.append(amount)
        return amounts


def check_transaction_values(
    comment, outputAddresses, outputBackChange, enough_source, issuer_pubkey
):
    checkComment(comment)
    for outputAddress in outputAddresses:
        if check_public_key(outputAddress, True) is False:
            message_exit(outputAddress)
    if outputBackChange:
        outputBackChange = check_public_key(outputBackChange, True)
        if check_public_key(outputBackChange, True) is False:
            message_exit(outputBackChange)
    if enough_source:
        message_exit(
            issuer_pubkey + " pubkey doesn’t have enough money for this transaction."
        )


async def display_amount(tx, message, amount, currency_symbol):
    """
    For transaction_confirmation,
    Displays an amount in unit and relative reference.
    """
    amount_UD = round((amount / await UDValue().ud_value), 4)
    tx.append(
        [
            message + " (unit | relative)",
            "{unit_amount} {currency_symbol}  ||  {UD_amount} UD".format(
                unit_amount=str(amount / 100),
                currency_symbol=currency_symbol,
                UD_amount=str(amount_UD),
            ),
        ]
    )


async def display_pubkey(tx, message, pubkey):
    """
    For transaction_confirmation,
    Displays a pubkey and the eventually associated id.
    """
    tx.append([message + " (pubkey)", pubkey])
    id = await is_member(pubkey)
    if id:
        tx.append([message + " (id)", id["uid"]])


async def display_output_and_amount(tx, outputAddresses, tx_amount, currency_symbol):
    """
    For transaction_confirmation,
    Displays the receiver(s) and the amount(s) of one or many output(s).
    """
    if len(tx_amount) == 1:
        for outputAddress in outputAddresses:
            await display_pubkey(tx, "to", outputAddress)
            await display_amount(tx, "amount", tx_amount[0], currency_symbol)
    if len(tx_amount) > 1:
        c = 0
        while c < len(outputAddresses):
            await display_pubkey(tx, "to", outputAddresses[c])
            await display_amount(tx, "amount", tx_amount[c], currency_symbol)
            c += 1


async def transaction_confirmation(
    issuer_pubkey,
    pubkey_amount,
    tx_amount,
    totalAmount,
    outputAddresses,
    outputBackChange,
    comment,
):
    """
    Generate transaction confirmation
    """

    currency_symbol = await CurrencySymbol().symbol
    tx = list()
    tx.append(
        ["pubkey’s balance before tx", str(pubkey_amount / 100) + " " + currency_symbol]
    )

    await display_amount(tx, "total amount", totalAmount, currency_symbol)

    tx.append(
        [
            "pubkey’s balance after tx",
            str(((pubkey_amount - totalAmount) / 100)) + " " + currency_symbol,
        ]
    )

    await display_pubkey(tx, "from", issuer_pubkey)
    await display_output_and_amount(tx, outputAddresses, tx_amount, currency_symbol)
    if outputBackChange:
        await display_pubkey(tx, "Backchange", outputBackChange)

    tx.append(["comment", comment])
    return tx


async def get_list_input_for_transaction(pubkey, TXamount, outputs_number):
    listinput, amount = await get_sources(pubkey)

    # check max inputs. For now we deal only with one issuer
    maxInputsNumber = max_inputs_number(outputs_number, 1)
    # generate final list source
    listinputfinal = []
    totalAmountInput = 0
    intermediatetransaction = False
    for input in listinput:
        listinputfinal.append(input)
        totalAmountInput += amount_in_current_base(input)
        TXamount -= amount_in_current_base(input)
        # if too much sources, it's an intermediate transaction
        if len(listinputfinal) >= maxInputsNumber and not len(listinputfinal) == 1:
            intermediatetransaction = True
        if (len(listinputfinal) >= MAX_INPUTS_PER_TX) or (TXamount <= 0):
            break
    if TXamount > 0 and not intermediatetransaction:
        message_exit("Error: you don't have enough money")
    return listinputfinal, totalAmountInput, intermediatetransaction


def max_inputs_number(outputs_number, issuers_number=1, comment=True):
    """
    Returns the maximum number of inputs.
    This function does not take care of backchange line.
    Formula is Inputs_Unlock number <= (MAX_LINES - FIX_LINES - Comment - Output_number - 2* Issuer_Signature_number)/2
    """
    if comment == True:
        comment = 1
    return (
        MAX_LINES_IN_TX_DOC
        - FIX_LINES
        - comment
        - (2 * issuers_number)
        - outputs_number
    ) / 2



# Créer une fonction handle_transactions_with_conditions
# qui gèrerait l'ajout de conditions spécifiques pour G1pourboire :
# SIG(0) || SIG(sender_pubkey) && CSV(time)
async def handle_intermediaries_transactions(
    key,
    issuers,
    tx_amount,
    totalAmount,
    outputAddresses,
    Comment="",
    OutputbackChange=None,
):
    client = ClientInstance().client
    while True:
        listinput_and_amount = await get_list_input_for_transaction(
            issuers, totalAmount, len(outputAddresses)
        )

        intermediatetransaction = listinput_and_amount[2]

        if intermediatetransaction:
            totalAmountInput = list()
            totalAmountInput.append (listinput_and_amount[1])
            await generate_and_send_transaction(
                key,
                issuers,
                totalAmount,
                totalAmountInput,
                listinput_and_amount,
                issuers,
                "Change operation",
            )
            sleep(1)  # wait 1 second before sending a new transaction
        else:
            await generate_and_send_transaction(
                key,
                issuers,
                totalAmount,
                tx_amount,
                listinput_and_amount,
                outputAddresses,
                Comment,
                OutputbackChange,
            )
            await client.close()
            break
        #return 0

async def handle_transactions_with_delay(
    key,
    issuers,
    tx_amount,
    totalAmount,
    outputAddresses,
    delay,
    Comment="",
    OutputbackChange=None,
):
    client = ClientInstance().client
    while True:
        listinput_and_amount = await get_list_input_for_transaction(
            issuers, totalAmount
        )

        intermediatetransaction = listinput_and_amount[2]

        if intermediatetransaction:
            totalAmountInput = list()
            totalAmountInput.append (listinput_and_amount[1])
            await generate_and_send_transaction(
                key,
                issuers,
                totalAmount,
                totalAmountInput,
                listinput_and_amount,
                issuers,
                "Change operation",
            )
            sleep(1)  # wait 1 second before sending a new transaction
        else:
            await generate_and_send_transaction_with_delay(
                key,
                issuers,
                totalAmount,
                tx_amount,
                listinput_and_amount,
                outputAddresses,
                delay,
                Comment,
                OutputbackChange,
            )
            await client.close()
            break


async def generate_and_send_transaction(
    key,
    issuers,
    totalAmount,
    tx_amount,
    listinput_and_amount,
    outputAddresses,
    Comment,
    OutputbackChange=None,
):
    """
    Display sent transaction
    Generate, sign, and send transaction document
    """
    intermediate_tx = listinput_and_amount[2]
    if intermediate_tx:
        print("Generate Change Transaction")
    else:
        print("Generate Transaction:")
    print("   - From:    " + issuers)
    if len(tx_amount) == 1:
        if isinstance(outputAddresses, str):
            display_sent_tx(outputAddresses, tx_amount[0])
        else:
            for outputAddress in outputAddresses:
                display_sent_tx(outputAddress, tx_amount[0])
    else:
        c = 0
        while c < len(outputAddresses):
            display_sent_tx(outputAddresses[c], tx_amount[c])
            c += 1
    client = ClientInstance().client
    transaction = await generate_transaction_document(
        issuers,
        totalAmount,
        tx_amount,
        listinput_and_amount,
        outputAddresses,
        Comment,
        OutputbackChange,
    )
    transaction.sign([key])
    response = await client(process, transaction.signed_raw())
    if response.status == 200:
        print("Transaction successfully sent.")
    else:
        message_exit(
            "Error while publishing transaction: {0}".format(await response.text())
        )

async def generate_and_send_transaction_with_delay(
    key,
    issuers,
    totalAmount,
    tx_amount,
    listinput_and_amount,
    outputAddresses,
    delay,
    Comment,
    OutputbackChange=None,
):
    """
    Display sent transaction
    Generate, sign, and send transaction document
    """
    intermediate_tx = listinput_and_amount[2]
    if intermediate_tx:
        print("Generate Change Transaction")
    else:
        print("Generate Transaction:")
    print("   - From:    " + issuers)
    if len(tx_amount) == 1:
        if isinstance(outputAddresses, str):
            display_sent_tx(outputAddresses, tx_amount[0])
        else:
            for outputAddress in outputAddresses:
                display_sent_tx(outputAddress, tx_amount[0])
    else:
        c = 0
        while c < len(outputAddresses):
            display_sent_tx(outputAddresses[c], tx_amount[c])
            c += 1
    client = ClientInstance().client
    transaction = await generate_transaction_document_with_delay(
        issuers,
        totalAmount,
        tx_amount,
        listinput_and_amount,
        outputAddresses,
        delay,
        Comment,
        OutputbackChange,
    )
    transaction.sign([key])
    response = await client(process, transaction.signed_raw())
    if response.status == 200:
        print("Transaction successfully sent.")
    else:
        message_exit(
            "Error while publishing transaction: {0}".format(await response.text())
        )


def display_sent_tx(outputAddress, amount):
    print("   - To:     ", outputAddress, "\n   - Amount: ", int(amount) / 100)

async def generate_transaction_document(
    issuers,
    totalAmount,
    tx_amount,
    listinput_and_amount,
    outputAddresses,
    Comment="",
    OutputbackChange=None,
):

    listinput = listinput_and_amount[0]
    totalAmountInput = listinput_and_amount[1]

    head_block = await HeadBlock().head_block
    currency_name = head_block["currency"]
    blockstamp_current = BlockUID(head_block["number"], head_block["hash"])
    curentUnitBase = head_block["unitbase"]

    if not OutputbackChange:
        OutputbackChange = issuers

    # if it's not a foreign exchange transaction, we remove units after 2 digits after the decimal point.
    if issuers not in outputAddresses:
        totalAmount = (totalAmount // 10 ** curentUnitBase) * 10 ** curentUnitBase

    # Generate output
    ################
    listoutput = []
    if len(tx_amount) == 1:
    # Outputs to himself (change operation)
        if isinstance(outputAddresses, str):
            generate_output(listoutput, curentUnitBase, tx_amount[0], outputAddresses)
    # Outputs to receiver (if not himself)
        else:
            for outputAddress in outputAddresses:
                generate_output(listoutput, curentUnitBase, tx_amount[0], outputAddress)
    else:
        c = 0
        while c < len(outputAddresses):
            generate_output(
                listoutput, curentUnitBase, tx_amount[c], outputAddresses[c]
            )
            c += 1
    # Outputs to himself
    rest = totalAmountInput - totalAmount
    generate_output(listoutput, curentUnitBase, rest, OutputbackChange)

    # Unlocks
    unlocks = generate_unlocks(listinput)

    # Generate transaction document
    ##############################

    return Transaction(
        version=10,
        currency=currency_name,
        blockstamp=blockstamp_current,
        locktime=0,
        issuers=[issuers],
        inputs=listinput,
        unlocks=unlocks,
        outputs=listoutput,
        comment=Comment,
        signatures=[],
    )

async def generate_transaction_document_with_delay(
    issuers,
    totalAmount,
    tx_amount,
    listinput_and_amount,
    outputAddresses,
    delay,
    Comment="",
    OutputbackChange=None,
):

    listinput = listinput_and_amount[0]
    totalAmountInput = listinput_and_amount[1]

    head_block = await HeadBlock().head_block
    currency_name = head_block["currency"]
    blockstamp_current = BlockUID(head_block["number"], head_block["hash"])
    curentUnitBase = head_block["unitbase"]

    if not OutputbackChange:
        OutputbackChange = issuers

    # if it's not a foreign exchange transaction, we remove units after 2 digits after the decimal point.
    if issuers not in outputAddresses:
        totalAmount = (totalAmount // 10 ** curentUnitBase) * 10 ** curentUnitBase

    # Generate output
    ################
    listoutput = []
    if len(tx_amount) == 1:
    # Outputs to himself (change operation)
        if isinstance(outputAddresses, str):
            generate_output(listoutput, curentUnitBase, tx_amount[0], outputAddresses)
    # Outputs to receiver (if not himself)
        else:
            for outputAddress in outputAddresses:
                generate_output_with_delay(listoutput, curentUnitBase, tx_amount[0], outputAddress, delay, issuers)
    else:
        c = 0
        while c < len(outputAddresses):
            generate_output_with_delay(
                listoutput, curentUnitBase, tx_amount[c], outputAddresses[c], delay, issuers
            )
            c += 1
    # Outputs to himself
    rest = totalAmountInput - totalAmount
    generate_output(listoutput, curentUnitBase, rest, OutputbackChange)

    # Unlocks
    unlocks = generate_unlocks(listinput)

    # Generate transaction document
    ##############################

    return Transaction(
        version=10,
        currency=currency_name,
        blockstamp=blockstamp_current,
        locktime=0,
        issuers=[issuers],
        inputs=listinput,
        unlocks=unlocks,
        outputs=listoutput,
        comment=Comment,
        signatures=[],
    )


def generate_unlocks(listinput):
    unlocks = list()
    for i in range(0, len(listinput)):
        unlocks.append(Unlock(index=i, parameters=[SIGParameter(0)]))
    return unlocks


def generate_output(listoutput, unitbase, rest, recipient_address):
    while rest > 0:
        outputAmount = truncBase(rest, unitbase)
        rest -= outputAmount
        if outputAmount > 0:
            outputAmount = int(outputAmount / math.pow(10, unitbase))
            listoutput.append(
                OutputSource(
                    amount=str(outputAmount),
                    base=unitbase,
                    condition="SIG({0})".format(recipient_address),
                )
            )
        unitbase = unitbase - 1


def generate_output_with_delay(listoutput, unitbase, rest, recipient_address, delay, sender_address):
    while rest > 0:
        outputAmount = truncBase(rest, unitbase)
        rest -= outputAmount
        if outputAmount > 0:
            outputAmount = int(outputAmount / math.pow(10, unitbase))
            listoutput.append(
                OutputSource(
                    amount=str(outputAmount),
                    base=unitbase,
                    condition="(SIG({recipient}) || (SIG({sender}) && CSV({delay})))".format(recipient=recipient_address, sender=sender_address, delay=delay),
                )
            )

        unitbase = unitbase - 1


def checkComment(Comment):
    if len(Comment) > 255:
        message_exit("Error: Comment is too long")
    regex = compile(
        "^[0-9a-zA-Z\ \-\_\:\/\;\*\[\]\(\)\?\!\^\+\=\#@\&\~\#\{\}\|\\\<\>\%\.]*$"
    )
    if not search(regex, Comment):
        message_exit("Error: the format of the comment is invalid")


def truncBase(amount, base):
    pow = math.pow(10, base)
    if amount < pow:
        return 0
    return math.trunc(amount / pow) * pow
