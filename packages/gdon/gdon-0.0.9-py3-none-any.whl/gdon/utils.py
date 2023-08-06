import datetime
import os
import json
import re

from gdon.constants import DEFAULT_FOLDER, WALLETS_FOLDER, BACKUP_FOLDER, PDF_BACKUP_FOLDER, PDF_EXTENSION, SIGNED_EXTENSION, CONF_FILE, HTTP_PORT
from gdon.silkaj.constants import G1_DEFAULT_ENDPOINT

def check_date(given_date):
    """
    check if a given peremption date is correctly formatted.
    if in the past, asks for user validation.
    """
    infos_date = given_date.split("/")
    if len(infos_date) != 3 or len(infos_date[2]) != 4 or len(infos_date[0]) != 2 or len(infos_date[1]) != 2:
        print ("Erreur : le champs <date> doit être de forme JJ/MM/YYYY")
        exit
    today = datetime.datetime.now()
    date = datetime.datetime(int(infos_date[2]), int(infos_date[1]), int(infos_date[0]))
    if today > date:
        while True:
            answer = input("La date donnée est passée. Voulez-vous continuer (O/n) ? : ")
            if answer == "n" or answer == "N":
                print ("Veuillez recommencer.")
                exit(0)
            elif answer == "o" or answer == "O" or answer == "":
                break
            else:
                print("La réponse doit être O ou n.")
    return datetime.date(int(infos_date[2]), int(infos_date[1]), int(infos_date[0]))


class CheckConfig():
    """
    check that the config exists. If not, create relevant folders.
    """
    def __init__(self):

        self.config_file = os.path.expanduser(CONF_FILE)
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.mkdir(os.path.dirname(self.config_file))
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                conf = json.loads(f.read())
                folder = conf["folder"]
        else :
            folder = os.path.expanduser(DEFAULT_FOLDER)

        self.folder = os.path.expanduser(folder)
        self.wallets_folder = os.path.expanduser(folder + WALLETS_FOLDER)
        self.backup_folder = os.path.expanduser(folder + BACKUP_FOLDER)

    def __call__(self):
        return self

    def check(self, node=G1_DEFAULT_ENDPOINT):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        if not os.path.exists(self.wallets_folder):
            os.makedirs(self.wallets_folder)
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.mkdir(os.path.dirname(self.config_file))
        if not os.path.exists(self.config_file):
            f = open(self.config_file, "x")
            f.close()
            self.write_conf(node[0], node[1], self.folder)

    def get_conf(self):
        if not os.path.exists(self.config_file):
            self.check()
        with open(self.config_file, "r") as f:
            return json.loads(f.read())

    def display_conf(self):
        if not os.path.exists(self.config_file):
            self.check()
        with open(self.config_file, "r") as f:
            conf = json.loads(f.read())
            print ("\nConfiguration :\nnode : {0}\nport : {1}\ndossier : {2}\n".format(conf["node"], conf["port"], conf["folder"]))


    def check_conf(self, node: str, port: int, folder:str):
        conf = self.get_conf()
        if node == None:
            node = conf["node"]
            if port == None:
                port = conf["port"]

        if folder != None:
            folder = os.path.abspath(folder) + "/"
        elif folder == None:
            folder = conf["folder"]

        self.write_conf(node, port, folder)
        self.check()

    def write_conf(self, given_node, port, folder):
        conf = dict()
        conf["node"] = str(given_node)
        conf["port"] = str(int(port))
        conf["folder"] = str(folder)
        with open(self.config_file, "w") as f:
            f.write(json.dumps(conf, indent=4))
        print("Configuration enregistrée : \n node : {0}\n port : {1}\n dossier : {2}".format(given_node, str(port), folder))



def backup_data(data, name):
    """
    Backups the signed files to .backup
    If there is a corresponding pdf file in the conf folder, move it to the .backup/year/pdf folder.
    Takes as inputs the full path and the name of the signed document.
    """

    conf = CheckConfig()
    conf.check()

    # check that the backup folder exists
    year = str(datetime.datetime.now().year)
    backup_folder = os.path.join(conf.backup_folder, year)
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # create the backup path and move the file
    backup = os.path.join(backup_folder, name)
    os.rename(data, backup)
    print("{0} --> {1}/".format(name, backup_folder))

    # check if there is a pdf file in the default wallets folder, and move it to the backups pdf folder
    if re.search(SIGNED_EXTENSION, name):
        pdf_file = name.replace(SIGNED_EXTENSION, PDF_EXTENSION)
        pdf_folder = os.path.join(backup_folder, PDF_BACKUP_FOLDER)
        pdf_orig = os.path.expanduser(conf.folder + pdf_file)
        if os.path.isfile(pdf_orig):
            # check for pdf_folder and create it
            if not os.path.exists(pdf_folder):
                os.makedirs(pdf_folder)
            os.rename(pdf_orig, pdf_folder + pdf_file)
        print("{0} -->  {1}".format(pdf_file, pdf_folder))

