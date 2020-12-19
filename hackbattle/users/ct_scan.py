def predict_ct(path):
    import pickle
    import cv2
    from tensorflow.keras.models import load_model
    import numpy as np

    loaded_model = load_model('xception_ct.h5')
    path=path[1:]
    # path='covid1.png'
    # print(path)
    image = cv2.imread(str(path)) # read file 

    # print(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(224,224))
    image=image.reshape(-1,224, 224, 3)
    image = np.array(image) / 255

    pred=loaded_model.predict(image)
    print(pred)
    if pred[0][1]<0.5:
        print('covid')
        return 'covid'
    else:
        print('no covid')
        return 'no covid'

