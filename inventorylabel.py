from PIL import Image, ImageFont, ImageDraw
import qrcode
import sys

fontBig = ImageFont.truetype("Roboto-Regular.ttf", size=28)
fontSmall = ImageFont.truetype("Roboto-Regular.ttf", size=24)

# Wide tape (24mm) is 128px
# Line 1: My name
# Line 2: Artist name
# Line 3: Product Name
# Line 4: ID + Contact
# QR Code to the left of lines
def genWide(invid="N/A", prod="N/A"):

    textName = "Lukas 'DrLuke' Jackowski"
    sizeName = fontBig.getsize(textName)

    textArt = "VJ Pyree"
    sizeArt = fontBig.getsize(textArt)

    textID = "{%s}" % invid
    sizeID = fontBig.getsize(textID)

    textProd = prod
    sizeProd = fontSmall.getsize(textProd)

    textURL = "drluke.space/lost?id=%s" % invid
    sizeUrl = fontSmall.getsize(textURL)

    img = Image.new("1", (128 + max([sizeName[0], sizeArt[0] + sizeID[0], sizeProd[0], sizeUrl[0]]) + 12, 128), 1)
    draw = ImageDraw.Draw(img)

    draw.text((128 + 2, 2), textName, font=fontBig)
    draw.text((128 + 2, 2 + sizeName[1] + 4), textArt, font=fontBig)
    draw.text((128 + 2 + sizeName[0] - sizeID[0], 2 + sizeName[1] + 4), textID, font=fontBig)
    draw.text((128 + 2, 2 + sizeName[1] + 4 + sizeArt[1]), textProd, font=fontSmall)
    draw.text((128 + 2, 2 + sizeName[1] + 4 + sizeArt[1] + 4 + sizeProd[1]), textURL, font=fontSmall)

    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=0,
    )
    qr.add_data('https://drluke.space/lost?id=%s' % invid)
    qr.make(fit=False)

    qrimg = qr.make_image()
    img.paste(qrimg, (int((128-qrimg.size[0]) / 2), int((128-qrimg.size[1]) / 2)))

    img.save("out.png")

if len(sys.argv) > 3:
    genWide(sys.argv[1], sys.argv[2] + " - " + " ".join(sys.argv[3:]))
    print("-> ptouch-print --image out.png")
else:
    print("USAGE:")
    print("python inventorylabel.py ID VENDOR PRODUCTNAME")
    print("(All additional args after Productname will be concatenated with a space)")
    print("e.g. python inventorylabel.py beef1234 FluffCo. Foobar 3000")






