import cv2
import os
from os import remove, close
from shutil import move
from tempfile import mkstemp
import glob
import tkinter
import argparse
from tkinter import messagebox
# utility for selecting perfect rectangle on object of interest
class Marker(object):

    def __init__(self, descriptor_name = 'descriptor.txt',dir = 'samples'):
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.samples = os.path.join(self.root, dir)

        self.descriptor_dir = 'descriptors/'
        if not os.path.exists(self.descriptor_dir):
            os.makedirs(self.descriptor_dir)

        self.descriptor = os.path.join(self.descriptor_dir, descriptor_name)
        print('Result will be in: '+self.descriptor)
        self.drawing = False

    def draw_rect(self,event,x,y,flags,params):
        global x_init, y_init, top_left_pt, bottom_right_pt, img_orig, rect_final

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            x_init, y_init = x,y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                top_left_pt, bottom_right_pt = (x_init, y_init), (x,y)
                img[y_init:y, x_init:x] = 255 - img_orig[y_init:y, x_init:x]
                cv2.rectangle(img, top_left_pt, bottom_right_pt, (0,255,0),2)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            top_left_pt, bottom_right_pt = (x_init, y_init), (x,y)
            img[y_init:y, x_init:x] = 255 - img[y_init:y, x_init:x]
            cv2.rectangle(img,top_left_pt,bottom_right_pt, (0,255,0),2)
            #testing
            rect_final = (x_init,y_init,x ,y)
           # rect_final = (x_init, y_init, x - x_init, y - y_init)
            print(rect_final)
            self.save()

        # save
        # elif event == cv2.EVENT_RBUTTONDOWN:
        #     if not self.drawing:
        #         self.save()

    # save new img with rect position.
    # If same image is already there, it will just replace old coords
    def save(self):
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(self.descriptor) as old_file:
                found = False
                for line in old_file:
                    split = line.split('(')
                    if len(split) == 2 and img_name_only == line.split()[0]:
                        found = True
                        print('Replacing ',line)
                        line = "{0} {1}\n".format(img_name_only,rect_final)
                        print('With ',line)

                    new_file.write(line)

            # save new one
            if not found:
                print('Writing new image desc into ', img_name_only)
                new_file.write("{0} {1}\n".format(img_name_only,rect_final))

        close(fh)
        remove(self.descriptor)
        move(abs_path, self.descriptor)

    def save_negative(self):
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(self.descriptor) as old_file:
                found = False
                for line in old_file:
                    split = line.split('(')
                    if len(split) == 2 and img_name_only == line.split()[0]:
                        found = True
                        print('Replacing ',line)
                        line = "{0} {1}\n".format(img_name_only, 'negative')
                        print('With ',line)

                    new_file.write(line)

            # save new one
            if not found:
                print('Writing new image desc for ', img_name_only )
                new_file.write("{0} {1}\n".format(img_name_only, 'negative'))

        close(fh)
        remove(self.descriptor)
        move(abs_path, self.descriptor)


    def single(self, img_name):
        global img, img_orig, img_name_only
        img_name_only = img_name

        img_orig = cv2.imread(os.path.join(self.samples,img_name))
        img = img_orig.copy()



        while True:
            cv2.imshow('Input',img)
            c = cv2.waitKey(1)
            if c == 27:
                break

        cv2.destroyAllWindows()


    def all(self):
        global img, img_orig, img_name_only
        testing_images = glob.glob(self.samples + '/*.jpg')

        prefix_len = len(self.samples)

        if not os.path.exists(self.descriptor):
           open(self.descriptor,'a').close()

        cv2.namedWindow('Input')
        cv2.setMouseCallback('Input', self.draw_rect)

        for one in testing_images:
            img_name_only = one[prefix_len:]
            print('Reading: ',img_name_only)
            img_orig = cv2.imread(os.path.join(self.samples, one))
            img = img_orig.copy()

            while True:
                cv2.imshow('Input', img)
                c = cv2.waitKey(1)

                # save negative with N-key
                if c == 9:
                    self.save_negative()
                    break

                if c == 27 or c == 32:
                    break

        cv2.destroyAllWindows()

def argument_parse():
    parser = argparse.ArgumentParser(description='Nastroj na vytvorenie popisneho suboru idealnych detekcnych regionov')
    parser.add_argument('--dir',required=True ,help='Cesta k priecinku testovacich snimok')
    parser.add_argument('--name',required=False, default='descriptor.txt' ,help='Nazov vystupneho popisneho subora')

    args = parser.parse_args()
    return args

def marker_all(args):
    marker = Marker(dir=args.dir, descriptor_name=args.name)
    marker.all()

def marker_info():
    messagebox.showinfo("Info","Stlacenim tlacidla mysi oznacis, pustenim ulozis\nTAB - oznacis ako negative\nMedzernik / ESC - presun na dalsiu")

if __name__ == "__main__":
    args = argument_parse()

    top = tkinter.Tk()
    top.geometry("200x200")

    button = tkinter.Button(top, text="Mark All", command=lambda :marker_all(args))
    button.place(x=25, y=20)

    infoB = tkinter.Button(top, text="Marker Info", command=marker_info)
    infoB.place(x=20, y=50)

    top.mainloop()






