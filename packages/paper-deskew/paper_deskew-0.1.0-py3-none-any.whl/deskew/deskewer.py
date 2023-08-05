import os
import numpy as np
import argparse
from PIL import Image
import cv2
import uuid
import gdown

class Deskewer():
    def __init__(self):
        url = url = 'https://drive.google.com/uc?id={}'.format('1LdwPLAMgqed167rsU-iVeqnLHnGU_htE')

        self.bin = gdown.download(url, output='/tmp/deskew', quiet=True)
        os.chmod(self.bin, 0o0777)

    def deskew(self, img):
        img = Image.fromarray(img)
        
        outpath = '/tmp/{}.jpg'.format(uuid.uuid4())
        inpath = '/tmp/{}.jpg'.format(uuid.uuid4())
        img.save(inpath)
        cmd = '{} -b ffffff -o {} {} >/dev/null 2>&1'.format(self.bin, outpath, inpath)
        os.system(cmd)
        out_img = Image.open(outpath)
        out_img = np.asarray(out_img)

        return out_img

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', required=True, help='path to pdf')
    args = parser.parse_args()
    
    deskewer = Deskewer()
    img = Image.open(args.img)
    img = np.array(img)

    img = deskewer.deskew(img)
    print(img.shape)

if __name__ == '__main__':
    main()
