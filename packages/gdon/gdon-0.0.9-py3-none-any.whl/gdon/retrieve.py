import os
import shutil
import json
import re
from datetime import datetime
from time import sleep

from duniterpy.key import SigningKey, ascii_armor

from gdon.constants import DEFAULT_FOLDER, BACKUP_FOLDER, WALLETS_FOLDER, PDF_BACKUP_FOLDER, SIGNED_EXTENSION, PDF_EXTENSION, COMMENT, MAX_ISSUERS
from gdon.diceware import diceware
from gdon.utils import check_date, backup_data, CheckConfig


from gdon.silkaj.money import get_amount_from_pubkey
from gdon.silkaj.network_tools import ClientInstance
from gdon.silkaj.tx_retrieve import handle_intermediaries_transactions, generate_and_send_transaction, get_list_input_for_transaction
from gdon.silkaj.auth import auth_by_scrypt_with_IDs, auth_by_scrypt
from gdon.silkaj.tools import coroutine, message_exit
from gdon.silkaj.constants import PUBKEY_PATTERN


class Retrieve():
    """
    Retrieve wallets from encrypted files
    """
    def __init__(self, folder=None, _file=None):
        """
        check given values and set self values.
        """

        conf = CheckConfig()
        conf.check()

        if folder == None and _file == None:
             self.folder = conf.wallets_folder
        elif folder != None and _file != None:
            message_exit("Erreur : Retrieve() ne peut recevoir folder ET _file")

        elif folder != None:
            self.folder = os.path.abspath(folder)
            if not os.path.isdir(self.folder):
                message_exit("Erreur : le dossier n'existe pas : {0}".format(self.folder))
        elif _file != None:
            self.file = os.path.abspath(_file)
            if not os.path.isfile(self.file):
                message_exit("Erreur : le  fichier n'existe pas : {0}".format(self.file))

    def open_file(self, file):
        with open(file) as wallets_json:
            return json.load(wallets_json)

    def get_key_list(self, retrieve_wallets):
        """
        create key for each wallet
        """
        issuers_keys = list()
        for wallet in retrieve_wallets:
            key = auth_by_scrypt_with_IDs(wallet['salt'], wallet['password'])
            issuers_keys.append(key)
        return issuers_keys

    def is_date_passed(self, wallets_doc):
        peremption_date = datetime.fromisoformat(wallets_doc["peremption_date"])
        today = datetime.now()
        if not today > peremption_date:
            return False
        return True

    def get_pubkey(self, pubkey):
        """
        get credentials for each creator account
        """
        while True:
            print("\nEntrez les identifiants pour les clef publique : {0}\nSi vous ne savez pas, entrez des identifiants vides.".format(pubkey))
            key = auth_by_scrypt(None)
            if re.search(pubkey, key.pubkey):
                return key
            else:
                answer = input("Mauvais identifiants ! Voulez-vous réessayer ? (o/n) : ")
                if answer == "n":
                    return None


    def sort_folder(self, retrieve_files):
        """
        sorts retrievable files
        """
        # get all files from folder
        file_list = list()
        for root, dirs, files in os.walk(self.folder):
            for doc in files:
                file_list.append(doc)
        # extract data
        for doc in file_list:
            i = os.path.join(self.folder , doc)
            if self.extract_files(i, retrieve_files):
                backup_data(i, doc)
        if retrieve_files == None:
            message_exit("Aucun don n'est périmé.")

    def extract_files(self, doc, retrieve_files):
        """
        extracts wallets data from each readable file and adds it to retrieve_files.
        each found pubkey will be a ["key"] for retrieve_files dict and will contain all relevant wallets data.
        """
        if os.path.isfile(doc):
            try:
                pubkey, content  = self.open_data(doc)
            except:
                print ("ERREUR : le fichier {0} n'est pas lisible".format(doc))
                return False
            if self.is_date_passed(content):
                try:
                    retrieve_files[pubkey].append(content)
                except:
                    retrieve_files[pubkey] = list()
                    retrieve_files[pubkey].append(content)
                print ("Récupération du fichier : {0} périmé le {1}".format(doc, content["peremption_date"]))
                return True
            else:
                print("Fichier non récupéré, périmera le {1} : {0} .".format(doc, content["peremption_date"]))
                return False

    @coroutine
    async def retrieve(self):
        """
        retrieve money from perished tips
        """
        client = ClientInstance().client
        error = False
        retrieve_files = dict()
        if hasattr(self, "folder"):
            self.sort_folder(retrieve_files)
        elif hasattr(self, "file"):
            self.extract_files(self.file, retrieve_files)

        key_list = list()
        for pubkey in retrieve_files:
            key = self.get_pubkey(pubkey)
            key_list.append(key)
        for key, pubkey in zip(key_list, retrieve_files):
            if key is not None:
                print("Récupération des pourboires créée par la clef {0}...".format(pubkey))
                for content in retrieve_files[pubkey]:
                    ok = await self.retrieve_wallets(content, key)
                    if ok is False:
                        error = True
        if error:
            print("ERREUR : Des erreurs sont survenues, certains dons ont pu ne pas être récupérés. Relisez bien les logs.")
        # closing the client instance
        await client.close()

    def open_data(self, _file):
        """
        open encrypted data
        """
        data_file = open(_file, "r")
        signed_data = data_file.read()
        pubkey = re.search(re.compile(PUBKEY_PATTERN), signed_data).group()
        data = ascii_armor.AsciiArmor.parse(signed_data, sender_pubkeys=[pubkey])
        data_file.close()
        return pubkey, json.loads(data["message"]["content"])

    async def retrieve_wallets(self, content, key):
        """
        send money from wallets
        """
        try :
            encrypted_wallets = content["wallets"]
            retrieving_wallets = ascii_armor.AsciiArmor.parse(encrypted_wallets, key) 
            retrieving_wallets = json.loads(retrieving_wallets["message"]["content"])
        except:
            print("ERREUR : Des dons, périmés le {0}, n'ont pas pu être récupérés, probablement à cause d'une modification du fichier ou d'un fichier mal formaté.".format(content["peremption_date"]))
            return False
        # send transactions
        while len(retrieving_wallets) != 0:
            _range, issuers, key_list, amount, listinput = 0, list(), list(), 0, list()
            wallet_list = list()
            if len(retrieving_wallets) > MAX_ISSUERS:
                for n in range (0,MAX_ISSUERS):
                    wallet_list.append (retrieving_wallets[n])
            else :
                wallet_list = retrieving_wallets
            issuers_keys = self.get_key_list(wallet_list)
            #create lists : keys, issuers, amount
            _range, intermediatetransaction = 0, 0
            for a in range (0, len(issuers_keys)):
                # print(a, _range) #debug
                # get inputs from all issuers
                listinput_and_amount = await get_list_input_for_transaction(_range, issuers_keys[a].pubkey, len(listinput))
                # print each empty G1Don
                if listinput_and_amount[1] == 0:
                    print("Ce don est vide ou a été récupéré : {0}".format(issuers_keys[a].pubkey))
                else:
                    _range += 1
                    key_list.append(issuers_keys[a])
                    issuers.append(issuers_keys[a].pubkey)
                    listinput.extend(listinput_and_amount[0])
                    amount = amount + listinput_and_amount[1]
                    intermediatetransaction = listinput_and_amount[2]
                # send transactions (intermediate if necessary)
                if intermediatetransaction or (issuers_keys[a] == issuers_keys[-1] and amount !=0):
                    # if a wallet has a lot of sources, we want to use all sources in many transactions.
                    while amount != 0:
                        total_listinput_and_amount = [listinput, amount, intermediatetransaction]
                        #amount = [amount]
                        await generate_and_send_transaction(
                            key_list,
                            issuers,
                            [amount],
                            total_listinput_and_amount,
                            [key.pubkey],
                            COMMENT,
                        )
                        key_list, issuers = [issuers_keys[a]], [issuers_keys[a].pubkey]
                        listinput, amount, intermediatetransaction = await get_list_input_for_transaction(0, issuers_keys[a].pubkey, 0)
                        sleep(1)
                    _range, issuers, key_list, amount, listinput = 0, list(), list(), 0, list()
            # delete already used wallets
            if not len(retrieving_wallets) == 0:
                limit = min(len(retrieving_wallets), MAX_ISSUERS)
                for n in range (0, limit):
                    retrieving_wallets.pop(0)

class BackupRetrieve():
    """
    prepare the retrieval of backups.
    """
    def __init__(self, year):

        conf = CheckConfig()
        conf.check()

        year = self.check_year(year)
        self.orig = os.path.join(conf.backup_folder, year)
        self.dest = os.path.join(conf.folder, year)
        if not os.path.isdir(self.orig):
            message_exit("ERREUR : {0} n'a pas de dossier correspondant dans {1}.".format(year, self.orig))
        if os.path.exists(self.dest):
            try:
                shutil.rmtree(self.dest)
            except:
                message_exit("ERREUR : le dossier {0} n'a pas pu être supprimé. Supprimez-le et recommencez.".format(self.dest))
        shutil.copytree(self.orig, self.dest)
        print("Récupération des backups {0}".format(year))
        print("Dossier {0} copié dans {1}".format(self.orig, self.dest))
        print("Si le processus ne se termine pas, vous pouvez le relancer.")

    def __call__(self):
        return self

    def delete(self):
        try:
            shutil.rmtree(self.dest)
        except:
            message_exit("ERREUR : le dossier {0} n'a pas pu être supprimé. Supprimez-le manuellement.".format(self.dest))

    def check_year(self, year):
        if re.search(re.compile("^[0-9]{4}$"), year):
            return str(year + "/")
        message_exit("ERREUR : {0} n'est pas une année valide.".format(str(year)))
