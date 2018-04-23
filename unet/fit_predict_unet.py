'''
We use the same methods which was created by our team member Vyom Shrivastava during project 4 with Team Hastings.
'''

import numpy as np
from unet_model import unet
import argparse

#Importing keras function
from keras.models import Model
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, Conv2DTranspose
from keras.optimizers import Adam
from keras import backend as K


#getting command line argument
parser = argparse.ArgumentParser(description='paths')
parser.add_argument('--mode',type=str,help='fit or predict?')
parser.add_argument('--image_path',type=str,help='path of image npy array')
parser.add_argument('--mask_path',type=str,help='path of mask npy array')
parser.add_argument('--model_path',type=str,help='path of saved model')
parser.add_argument('--save_path',type=str,help='path to save model or prediction')
args = parser.parse_args()

def augment_data(image_path,mask_path,mode):
    '''
    loads images and mask as a numpy array, reshapes images and mask to 4 channels
    and normalzes image data
    
    Args:
        image_path:the path of the npy array containing images
                   type: String
        mask_path:      the path to npy array containing masks
                   type: String
    Return:
        numpy array of augmented mask and image
    '''
    image_array = np.load(image_path)    
    data_images = image_array - np.mean(image_array)
    data_images = data_images / np.std(image_array)
    
    if(mode=="fit"):
        mask_images = np.load(mask_path)
        return data_images, mask_images
    else:
        return data_images

#Augmenting data
if(args.mode=="fit"):
    images,mask = augment_data(args.image_path,args.mask_path,args.mode)
if(args.mode=="predict"):
    images = augment_data(args.image_path,args.mask_path,args.mode)

def fit(training_images,mask_images,save_path):
    model = unet()
    #Fitting and saving model
    model.fit(training_images, mask_images, batch_size=8, epochs=10, verbose=1, shuffle=True)
    model.save(save_path+"/"+"model.h5")

def predict(testing_images,model_path,save_result_path):
    #loading model and predicting mask
    model=unet()
    model.load_weights(model_path)

    prediction = model.predict(testing_images, batch_size=4,verbose=1)
    np.save(save_result_path+'/prediction.npy', prediction)

if(args.mode=="fit"):
    fit(images,mask,args.save_path)
if(args.mode=="predict"):
    predict(images,args.model_path,args.save_path)