from PIL import Image, ImageFont, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from duniterpy.key import SigningKey, ascii_armor
from gdon.diceware import diceware
from gdon.silkaj.constants import G1_SYMBOL

import os
import json
import qrcode
import datetime

recto_file = "objects/recto.png"
verso_file = "objects/verso.png"
typo_file = "objects/Roboto-Medium.ttf"

class Generator:
    """Generate some wallets, create the pdf to print"""

    def __init__(self, output, wallets, amount, date, pages=1):
        self.pages = pages
        self.output = output
        self.wallets = wallets
        self.amount = amount
        self.date = date
        self.c = None

        # set objects dir
        par_dir = os.path.abspath(os.path.dirname(__file__))
	#wordlist_path = os.path.join(parent_dir, wordlist)
        self.recto = os.path.join(par_dir, recto_file)
        self.verso = os.path.join(par_dir, verso_file)
        self.typo = os.path.join(par_dir, typo_file)

    def generate(self):
        """
        generate tips wallets ; then create the pdf file
        """
        for i in range(self.pages):
            for j in range(6):  # 6 wallets per pages
                self.new_wallet()

        self.make_pdf()

    def new_wallet(self):
        """
        generate one wallet with the associated images
        """
        # Generating credentials
        salt = diceware(3, separator="-", camelcase=False)
        password = diceware(3, separator="-", camelcase=False)
        # Generating key from credentials
        key = SigningKey.from_credentials(salt, password)
        # Url to redirect to in the public QR code
        account_url = "https://demo.cesium.app/#/app/wot/tx/" + key.pubkey + "/"
        # Generating wif data
        key.save_wif_file("privatekey.wif")
        wif_data = open("privatekey.wif").readlines()[-1].split(": ")[1]
        #try add a \n after wif
#        wif_data.join(["\n"])
        os.remove("privatekey.wif")
        # Creating the QR codes
        qr_pub = qrcode.make(account_url)
        qr_priv = qrcode.make(wif_data)
        # Open images
        recto = Image.open(self.recto)
        verso = Image.open(self.verso)
        # Pasting QR codes
        recto.paste(qr_pub.resize((200, 200)), (435, 15))  # 36))
        verso.paste(qr_priv.resize((180, 180)), (580, 6))
        # Setting font
#        font = ImageFont.truetype("objects/Roboto-Medium.ttf", 18)
        font = ImageFont.truetype(self.typo, 18)
        # Writing amount
        if self.amount > 0:
            draw = ImageDraw.Draw(recto)
            txt = "\n".join([str(self.amount) + G1_SYMBOL])
            draw.text(
                (1090, 150),
                txt,
                (0, 0, 0),
                font=ImageFont.truetype(self.typo, 30),
            )
        # Writing date
        write_date = "{0}/{1}/{2}".format(self.date.day, self.date.month, self.date.year)
        draw = ImageDraw.Draw(recto)
        draw.text(
            (665, 230),
            write_date,
            (0, 0, 0),
            font=font,
        )
        # Writing public key
        draw = ImageDraw.Draw(recto)
        txt = "\n".join([key.pubkey[i : i + 10] for i in range(0, len(key.pubkey), 10)])
        draw.text((665, 80), txt, (0, 0, 0), font=font)
        # Writing private keys
        draw = ImageDraw.Draw(verso)
        draw.text((570, 230), "ID : " + salt, (0, 0, 0), font=font)
        draw.text((570, 250), "PW : " + password, (0, 0, 0), font=font)
        # Add data to wallets
        self.wallets.append(
            {
                "salt": salt,
                "password": password,
                "pubkey": key.pubkey,
                "date": 0,
                "recto": recto,
                "verso": verso,
                "transfer": "false",
            }
        )

    def gen_page(self, wallets):
        """
        generate a pdf page from a wallet list with relevant images.
        """
        # Create a new canvas
        if self.c == None:
            self.c = canvas.Canvas(self.output)
        # Size of wallets. You may not edit those values until you know what you do
        width = 19 * cm
        height = width * 302 / 1270
        # Print recto
        for i, w in enumerate(wallets):
            self.c.drawInlineImage(
                w["recto"], (21 * cm - width) / 2, 24.2 * cm - i * height, width, height
            )
        self.c.showPage()
        # And verso
        for i, w in enumerate(wallets):
            self.c.drawInlineImage(
                w["verso"], (21 * cm - width) / 2, 24.2 * cm - i * height, width, height
            )
        self.c.showPage()

    def make_pdf(self):
        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i : i + n]

        # Create pages
        for wallets in chunks(self.wallets, 6):
            self.gen_page(wallets)
        self.c.save()
