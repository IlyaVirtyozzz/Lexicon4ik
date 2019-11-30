from PIL import Image, ImageFilter
import os

W, H = 776.0, 344.0

dir_name = './to_edit'

files = os.listdir(path=dir_name)

for entry in files:
    full_path = os.path.join(dir_name, entry)

    myimage = Image.open(full_path)
    myimage.load()
    w, h = myimage.size

    blurred = myimage.filter(ImageFilter.GaussianBlur(radius=5))

    scale = W / min(h, w)

    myimage = myimage.resize((int(w * H / h), int(H)))
    blurred = blurred.resize((int(h * scale), int(w * scale)))

    x1 = int(.5 * blurred.size[0]) - int(.5 * myimage.size[0])
    y1 = int(.5 * blurred.size[1]) - int(.5 * myimage.size[1])
    x2 = int(.5 * blurred.size[0]) + int(.5 * myimage.size[0])
    y2 = int(.5 * blurred.size[1]) + int(.5 * myimage.size[1])

    blurred.paste(myimage, (x1, y1))

    x1_ = int(.5 * blurred.size[0]) - int(.5 * W)
    y1_ = int(.5 * blurred.size[1]) - int(.5 * H)
    x2_ = int(.5 * blurred.size[0]) + int(.5 * W)
    y2_ = int(.5 * blurred.size[1]) + int(.5 * H)

    blurred = blurred.crop((x1_, y1_, x2_, y2_))

    blurred.save("after_edit/" + entry)
