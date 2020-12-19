def disease(symptoms):
    import pickle
    loaded_model = pickle.load(open('disease_model.sav', 'rb'))
    import sklearn
    d = pickle.load(open('symptoms_label.txt', 'rb'))
    # l=['itching','skin_rash','nodal_skin_eruptions']
    arr=[]
    for i in d:
        if i in symptoms:
            arr.append(1)
        else:
            arr.append(0)

    # print(arr)
    # print(d,len(d))
 
   ##samaj nahi aa raha kya kar raha hu...par dekhte hai

    import numpy as np
    arr=np.array(arr).reshape(1,-1)
    result = loaded_model.predict(arr)
    return result

