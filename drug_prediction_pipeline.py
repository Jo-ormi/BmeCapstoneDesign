#Running this program
#python drug_prediction_pipeline.py $work_dir $drug_a $drug_B

#importing library
from keras.models import Sequential
from keras.models import load_model
from pandas import DataFrame as df
import pandas as pd
import numpy as np
import tensorflow as tf
import sys


def search(drug):
    df = pd.read_csv("data/drug links.csv")

    kind = ['Name','CAS Number','Drug Type','KEGG Compound ID','KEGG Drug ID','PubChem Compound ID','PubChem Substance ID'
        ,'ChEBI ID','PharmGKB ID','HET ID','UniProt ID','UniProt Title','GenBank ID','DPD ID','RxList Link','Pdrhealth Link',
            'Wikipedia ID','Drugs.com Link','NDC ID','ChemSpider ID','BindingDB ID','TTD ID']
    df = df.apply(lambda x: x.astype(str).str.upper())
    for k in kind:
        find_row = df[(df[k] == drug)]
        if find_row.empty:
            pass
        else:
            # print(find_row)
            ID = find_row.iloc[0]['DrugBank ID']  # 셀에서 값만 추출

            # print(ID)
            return ID

def search_name(drug):
    df = pd.read_csv("data/drug links.csv")

    find_row = df[(df['DrugBank ID'] == drug)]
    if find_row.empty:
        pass
    else:
        # print(find_row)
        drug_name = find_row.iloc[0]['Name']  # 셀에서 값만 추출

        print(drug_name)
        return drug_name


def predict(A, B):
    #User Input
    work_dir = './'
    drug_a = str(A.upper())
    drug_b = str(B.upper())

    if drug_a.find('DB') != 0:
        drug_a = search(drug_a)
    else:
        pass

    if drug_b.find('DB') != 0:
        drug_b = search(drug_b)
    else:
        pass

    if drug_a.find('DB') == 0:
        drug_a_name = search_name(drug_a)
    else:
        pass

    if drug_b.find('DB') == 0:
        drug_b_name = search_name(drug_b)
    else:
        pass


    #model load
    model_loc = work_dir + "pretrained_model.h5"
    model = load_model(model_loc)

    #load_ddi_type data
    drug_type_loc = work_dir + "ddi_type_description.csv"
    drug_type = pd.read_csv(drug_type_loc)

    drug_type_dic = {}
    for i in range(0,len(drug_type)) :
        ddi_num = drug_type.iloc[i,0]
        description = drug_type.iloc[i,1]
        drug_type_dic[ddi_num] = description

    #ssp load
    ssp_loc = work_dir + "SSP_pca.txt"
    ssp = pd.read_csv(ssp_loc, delimiter = "\t")

    ssp_dic={}
    for i in range(0,len(ssp)) :
        drug = ssp.iloc[i,0]
        ssp_temp = list(ssp.iloc[i,1:202])
        ssp_dic[drug] = ssp_temp

    #psp load
    psp_loc = work_dir + "PSP_pca.txt"
    psp = pd.read_csv(psp_loc, delimiter = "\t")

    psp_dic={}
    for i in range(0,len(psp)) :
        drug = psp.iloc[i,0]
        psp_temp = list(psp.iloc[i,1:302])
        psp_dic[drug] = psp_temp

    #Check whether drug has structure & CTET protein information
    index = 1
    error = None
    if drug_a not in ssp_dic.keys() :
        error = drug_a + " don't have structure information"
        index = 0
    if drug_a not in psp_dic.keys() :
        error = drug_a + " don't have CTET protein information"
        index = 0
    if drug_b not in ssp_dic.keys() :
        error = drug_b + " don't have structure information"
        index = 0
    if drug_b not in psp_dic.keys() :
        error = drug_b + " don't have CTET protein information"
        index = 0

    if index == 1 :
        drug_a_ssp = ssp_dic[drug_a]
        drug_a_psp = psp_dic[drug_a]
        drug_b_ssp = ssp_dic[drug_b]
        drug_b_psp = psp_dic[drug_b]
        input_temp = drug_a_ssp + drug_a_psp + drug_b_ssp + drug_b_psp
        input_df = df([input_temp])
        network_input = input_df.astype(float)


    #model prediction
    test_result = model.predict(network_input)
    temp_list = test_result[0].tolist()
    confidence = max(temp_list)
    answer = temp_list.index(max(temp_list))
    result = [drug_a, drug_b, answer, confidence]
    result

    #Print Result
    # print("\n\nResult\n")
    # print("DDI between", drug_a, "and",drug_b, "is DDI type",result[2])
    # print("Description of DDI : ", drug_type_dic[result[2]])
    # print("Confidence Level : {:.2f}%".format(result[3]*100))

    res = "DDI between"+ drug_a + "and" + drug_b + "is DDI type" + str(result[2]) + "\nDescription of DDI : " + str(drug_type_dic[result[2]]) + "\nConfidence Level : " + str(round(result[3]*100,2))
    return [error, drug_a+' ('+drug_a_name+')', drug_b+' ('+drug_b_name+')', str(result[2]), str(drug_type_dic[result[2]]), str(round(result[3]*100,2))]

if __name__ == '__main__':
    predict('Acetaminophen', 'Zolpidem')