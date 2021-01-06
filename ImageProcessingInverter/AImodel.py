import keras
from keras import layers
from keras import optimizers
import pydotplus
from tensorflow.keras.utils import plot_model
from importlib import reload
from PIL import Image
import numpy
import tensorflow as tf
import tensorflow
import matplotlib.pyplot as plt
import os
import shutil
from datetime import datetime
import os

from Config import Config
from Dataset import Dataset
from Transformation import Transformation

#AImodel class is a wrapper for keras.models specialized in dealing with IPI datasets.
class AImodel(object):
    #Initialized current time.
    today = datetime.now()
    #Default constructor
    def __init__(self,transformations:[Transformation]=None,config:Config=None):
        if transformations==None:
            return
        if config==None:
            return
        self.model:keras.models.Model = None
        self.transformations:[Transformation]=[]
        self.history = None
        self.config=config
        self.transformations=transformations
        self.validationSplit = 0.1
        self.currentpath = ""
        if(os.path.isfile(os.getcwd()+"\\modelCache\\model_"+str(self.config.transformationSteps)+".h5")):
            self.model = keras.models.load_model(os.getcwd()+"\\modelCache\\model_"+str(self.config.transformationSteps)+".h5")
            print("Model loaded from .h5")
        else:
            orgData_input = keras.Input(shape=(self.config.imageTrainSize,self.config.imageTrainSize,3),name="original")
            transfData_input = keras.Input(shape=(self.config.imageTrainSize,self.config.imageTrainSize,3),name="transformed")
            x = layers.concatenate([orgData_input,transfData_input],axis=1)

            x = layers.Conv2D(32, kernel_size=(3, 3),activation='linear',padding='same')(x)
            x = layers.LeakyReLU(alpha=0.1)(x)
            x = layers.MaxPooling2D((2, 2),padding='same')(x)
            x = layers.Dropout(0.25)(x)

            x = layers.Conv2D(64, (3, 3), activation='linear',padding='same')(x)
            x = layers.LeakyReLU(alpha=0.1)(x)
            x = layers.MaxPooling2D(pool_size=(2, 2),padding='same')(x)
            x = layers.Dropout(0.25)(x)

            x = layers.Conv2D(128, (3, 3), activation='linear',padding='same')(x)
            x = layers.LeakyReLU(alpha=0.1)(x)
            x = layers.MaxPooling2D(pool_size=(2, 2),padding='same')(x)
            x = layers.Dropout(0.4)(x)

            x = layers.Flatten()(x)
            x = layers.Dense(128, activation='linear')(x)
            x = layers.LeakyReLU(alpha=0.1)(x) 
            x = layers.Dropout(0.3)(x)


            pred = layers.Dense(len(transformations), activation='softmax',name="transformation")(x)
            self.model= keras.Model(inputs=[orgData_input,transfData_input],outputs=[pred])

            self.model.summary()

            self.model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.0005),
                loss=[keras.losses.SparseCategoricalCrossentropy(from_logits=True)],
                metrics = [keras.metrics.SparseCategoricalAccuracy()],
                loss_weights=[1.0,0.2]
                )
    
    #Function that loads a particular specialized model.
    def Build(self,steps=1):
        if(os.path.isfile(os.getcwd()+"\\modelCache\\model_"+str(steps)+".h5")):
            self.model = keras.models.load_model(os.getcwd()+"\\modelCache\\model_"+str(steps)+".h5")
            print("Model"+str(steps)+" loaded from .h5")
        else:
            print("Something went wrong while loading Model"+str(steps))

    #Function that converts dataset labels to ids. New id is equal to transformation index in transformations array.
    def LabelsToIds(self,dataset:Dataset,transformations:[Transformation]):
        collection = []
        for i in range(0,len(dataset.collectionLabels)):
            item = dataset.collectionLabels[i]
            for j in range(0,len(transformations)):
                if transformations[j].GetCode()==item:
                    collection.append(j)
                    break
        #collection = keras.utils.to_categorical(collection,len(transformations)) # needed for other networks, makes collection one-hot encoded
        return collection

    #Function that handles teaching the model on a given dataset.
    def Learn(self,dataset:Dataset):
        self.history = self.model.fit({"original":numpy.asarray(dataset.collectionOrg),"transformed":numpy.asarray(dataset.collectionTransf)},
                              {"transformation":numpy.asarray(self.LabelsToIds(dataset,self.transformations))},
                              epochs=self.config.Epochs, verbose=1, shuffle=True, validation_split=self.validationSplit)
        if(self.config.saveModel==True):
            self.model.save(os.getcwd()+"\\modelCache\\model_"+str(self.config.transformationSteps)+".h5")
        plt.plot(self.history.history['val_sparse_categorical_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.ylim([0.0,1.0])
        plt.legend(['train', 'test'], loc='upper left')
        #plt.show()
        if self.config.savePlots:
            h = str(AImodel.today.hour)+"_"
            m = str(AImodel.today.minute)
            self.currentpath = os.getcwd()+self.config.plotsOutFolder+"\\"+AImodel.today.strftime('%Y_%m_%d_')+ h +m
            if not os.path.isdir(self.currentpath):
                os.system("mkdir "+self.currentpath)
            if not os.path.isdir(self.currentpath):
                return None
            self.config.Save(self.currentpath+"\\"+"config.ini")
            plt.savefig(self.currentpath+"\\"+"ModelLearningPlot_Steps_"+str(self.config.transformationSteps)+"_Epochs_"+str(self.config.Epochs)+".png")

        plt.clf()
        return None

    #Function that evaluates the model based on the dataset that it was learned on. It takes a particular percentage of entries in the dataset.
    def Evaluate(self,dataset:Dataset,msg):
        orgs = dataset.collectionOrg[int(-(len(dataset.collectionOrg)*self.validationSplit)):]
        transf = dataset.collectionTransf[int(-(len(dataset.collectionOrg)*self.validationSplit)):]
        label = self.LabelsToIds(dataset,self.transformations)[int(-(len(dataset.collectionOrg)*self.validationSplit)):]
        evaluation = (self.model.evaluate({"original":numpy.asarray(orgs),"transformed":numpy.asarray(transf)},{"transformation":numpy.asarray(label)}))
        if self.config.savePlots:
            if not os.path.isdir(self.currentpath):
                os.system("mkdir "+self.currentpath)
            if not os.path.isdir(self.currentpath):
                return None
            f = open (self.currentpath + "\\EvaluationResults.txt","a")
            f.write(msg+"\n")
            f.write("Transformation steps:"+str(self.config.transformationSteps)+"\n")
            f.write("Loss:"+str(evaluation[0])+"\n")
            f.write("Accuracy:"+str(evaluation[1])+"\n")
            f.write("\n")
            f.write("\n")
            f.close()
        print(evaluation)
                   

    #Function that evaluates loaded model on given dataset that does not require to be a learned on dataaset.
    def EvaluateIndependent(self,dataset:Dataset,msg):
        orgs = dataset.collectionOrg
        transf = dataset.collectionTransf
        label = self.LabelsToIds(dataset,self.transformations)
        evaluation = (self.model.evaluate({"original":numpy.asarray(orgs),"transformed":numpy.asarray(transf)},{"transformation":numpy.asarray(label)}))
        if self.config.savePlots:
            if not os.path.isdir(self.currentpath):
                os.system("mkdir "+self.currentpath)
            if not os.path.isdir(self.currentpath):
                return None
            f = open (self.currentpath + "\\EvaluationResults.txt","a")
            f.write(msg+"\n")
            f.write("Transformation steps:"+str(self.config.transformationSteps)+"\n")
            f.write("Loss:"+str(evaluation[0])+"\n")
            f.write("Accuracy:"+str(evaluation[1])+"\n")
            f.write("\n")
            f.write("\n")
            f.close()
        print(evaluation)

    #Function that returns a prediction made by the model.
    def Predict(self,originalFile,transformedFile):
        pred = self.model.predict({"original":numpy.asarray(originalFile),"transformed":numpy.asarray(transformedFile)})
        return pred
       