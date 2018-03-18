#from __future__ import print_function
import tensorflow as tf
import skimage.transform
from skimage.io import imsave, imread
import os 
#from os import walk 

class Colorizer:

    def __init__(self):
        self.first = True;
    
    def load_image(self, path, is_batch = False):
        imgs=[]
        if(is_batch):
            for file in path:
                img = imread(file)
                # crop image from center
                short_edge = min(img.shape[:2])
                yy = int((img.shape[0] - short_edge) / 2)
                xx = int((img.shape[1] - short_edge) / 2)
                crop_img = img[yy : yy + short_edge, xx : xx + short_edge]
                # resize to 224, 224
                img = skimage.transform.resize(crop_img, (224, 224))
                # desaturate image
                imgs.append(((img[:,:,0] + img[:,:,1] + img[:,:,2]) / 3.0).reshape(1, 224, 224, 1))
        else:
            img = imread(path)
            # crop image from center
            short_edge = min(img.shape[:2])
            yy = int((img.shape[0] - short_edge) / 2)
            xx = int((img.shape[1] - short_edge) / 2)
            crop_img = img[yy : yy + short_edge, xx : xx + short_edge]
            # resize to 224, 224
            img = skimage.transform.resize(crop_img, (224, 224))
            # desaturate image
            imgs.append(((img[:,:,0] + img[:,:,1] + img[:,:,2]) / 3.0).reshape(1, 224, 224, 1))
        return imgs
    
    def colorize(self, file_name, is_batch = False):
        shark_gray = self.load_image(file_name, is_batch)
        print("loaded image and reshaped it")
        model_dir = os.path.realpath(__file__).replace('forward.py','colorize.tfmodel')
        with open(model_dir, mode='rb') as f:
            fileContent = f.read()
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(fileContent)
        with tf.Graph().as_default():
            grayscale = tf.placeholder("float", [1, 224, 224, 1])
            tf.import_graph_def(graph_def, input_map={ "grayscale": grayscale }, name='')
            
            print("starting session...")
            with tf.Session() as sess:
                tf.global_variables_initializer().run()
                print("initialised variables")
                inferred_rgb = sess.graph.get_tensor_by_name("inferred_rgb:0")
                print("got needed tensor")
                if(is_batch):
                    for i, name in enumerate(shark_gray):
                        inferred_batch = sess.run(inferred_rgb, feed_dict={ grayscale: name })
                        dot = file_name[i].rfind('.')
                        old_name, format = file_name[i][0:dot], file_name[i][dot:] 
                        new_name = old_name +"_color."+format
                        print("got predictions")
                        imsave(new_name, inferred_batch[0])
                        print("saved image "+new_name)
                else:
                    inferred_batch = sess.run(inferred_rgb, feed_dict={ grayscale: shark_gray[0] })
                    dot = file_name.rfind('.')
                    old_name, format = file_name[0:dot], file_name[dot:] 
                    new_name = "temp." + format
                    print("got predictions")
                    imsave(new_name, inferred_batch[0])
                    return new_name
                    print("saved image "+new_name)
            print("finished session")


#f = []
#dir = "C:\\1\\"
c = Colorizer()
#for (dirpath, dirnames, filenames) in walk(dir):
#    print(filenames)
#    for file in filenames:
#       print(dir+file)
#        c.colorize(dir + file, False) 
#    break

c.colorize("C:\\app_ui_\\1.jpg", False) 