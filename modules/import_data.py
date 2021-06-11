import pandas as pd



def data(path):
    data = pd.read_csv(path,header=None)
    index_list = []
    for i in range(int(len(data)/2)):
        index_list.append("Vertical_No.{}".format(i+1))
        index_list.append("Rotation_No.{}".format(i+1))
    data.index = index_list

    return data

