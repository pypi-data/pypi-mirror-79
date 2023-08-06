import datetime
import re
import os
import json
from tabulate import tabulate

from gdon.generator import Generator
from gdon.transfer import Transfer
from gdon.constants import DEFAULT_FOLDER, WALLETS_FOLDER, BACKUP_FOLDER, PDF_EXTENSION, SIGNED_EXTENSION, CONF_FILE, MAX_PAGES, NAME
from gdon.utils import CheckConfig, check_date
from gdon.silkaj.tools import coroutine, message_exit
from gdon.silkaj.auth import auth_by_scrypt
from gdon.silkaj.constants import G1_SYMBOL
from duniterpy.key import SigningKey, ascii_armor


# Generate and fill Tips
class Creating:
    """Generating, filling wallets"""

    def __init__(self, amount, given_date, pages=1):
        if pages > MAX_PAGES:
            message_exit("Erreur : Ğ1Don gère un maximum de 10 pages.")
        self.pages = pages
        self.amount = amount
        conf = CheckConfig()
        conf.check()
        self.folder, self.wallets_folder, self.backup_folder = conf.folder, conf.wallets_folder, conf.backup_folder
        self.output = datetime.datetime.now().strftime(
            "Ğ1Don_%Y-%m-%dT%Hh%M"
        )
        self.pdf_output = self.folder + self.output + PDF_EXTENSION
        self.signed_output = self.wallets_folder + self.output + SIGNED_EXTENSION
        if os.path.isfile(self.pdf_output) or os.path.isfile(self.signed_output):
            message_exit("ERREUR : {0}{1}/{2} existe déjà. Attendez une minute et recommencez.".format(self.output, PDF_EXTENSION, SIGNED_EXTENSION))
        self.wallets = []
        # Check date format
        self.date = check_date(given_date)
        self.key = auth_by_scrypt(None)

    def __call__(self):
        return self

    def create(self):
        """ Generating, filling wallets."""

        if self.key and self.pages <= MAX_PAGES:
            print ("\nCréation des Ğ1Dons...")
            Generator(self.pdf_output, self.wallets, self.amount, self.date, self.pages).generate()
            print ("Enregistrement des portefeuilles sur :\n{0}\n".format(self.pdf_output))
            if not self.confirmation():
                os.remove(self.pdf_output)
                message_exit("OK, à bientôt !")
            try:
                self.save_json()
                transfer = Transfer(self.amount, self.pages, self.wallets, self.date)
                if self.amount > 0:
                    print ("Transferts...")
                    transfer.transfer(self.key)
            except:
                self.transfer_error()

    def transfer_error(self):
        """
        transfer the newly created files to the backup folder.
        """
        os.rename(self.pdf_output, self.backup_folder + self.output + PDF_EXTENSION)
        os.rename(self.signed_output, self.backup_folder + self.output + SIGNED_EXTENSION) 
        print ("\nERREUR : Quelque chose s'est mal passé durant le transfert.\nLes fichiers {0}{1}/{2} ont été déplacés dans le dossier {3}.\nVérifiez que votre clef publique est la bonne.\nVérifiez que le noeud Duniter est disponible.\nVérifiez si le transfert a eu lieu.".format(self.output, PDF_EXTENSION, SIGNED_EXTENSION, self.backup_folder))

    def save_json(self):
        """
        write wallets data in an encrypted json file.
        """
        # create and encrypt wallet list
        wallet_data = [
            {
                "pubkey": w["pubkey"],
                "salt": w["salt"],
                "password": w["password"],
            }
            for w in self.wallets
        ]
        clear_json = json.dumps(wallet_data)
        encrypted_wallets = ascii_armor.AsciiArmor.create(clear_json, self.key.pubkey)

        # add date and creator info
        data = {
            "creator_pubkey": self.key.pubkey,
            "peremption_date": self.date.isoformat(),
            "wallets": encrypted_wallets,
        }
        data = json.dumps(data)
        # sign the whole document
        signed_data = ascii_armor.AsciiArmor.create(data, signing_keys=[self.key])
        with open(
            self.signed_output, "a"
        ) as f:
            f.write(signed_data)


    def confirmation(self):
        tx=list()
        tx.append(["Compte créateur", self.key.pubkey])
        tx.append(["Ğ1Dons", "Montant"])
        for i, w in enumerate(self.wallets):
            tx.append([w["pubkey"], str(self.amount) + " " + G1_SYMBOL])
        tx.append(["Total", str(self.amount * len(self.wallets)) + " " + G1_SYMBOL])

        print(
            "Provisionner les", NAME, ":\n" +
            tabulate(tx, tablefmt="fancy_grid"),
        )
        answer = input("\nEnvoyer la transaction ? (O/n) : ")
        if answer == "O" or answer == "o" or answer == "" :
            return True
        return False
