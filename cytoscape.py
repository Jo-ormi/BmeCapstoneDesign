import pandas as pd
import numpy as np
from scipy.stats import hypergeom

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

def predict_cy(drug_a, drug_b):

    drug_a = str(drug_a.upper())
    drug_b = str(drug_b.upper())

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

    drugs = [drug_a, drug_b]
    uniprots = []

    du_df = pd.read_csv("data/uniprot links.csv")

    for drug in drugs:
      find_row = du_df[(du_df['DrugBank ID'] == drug)]
      if find_row.empty:
          pass
      else:
          # print(find_row)
          # print(len(find_row))
          i = 0
          while i < len(find_row):
            ID = find_row.iloc[i]['UniProt ID']  # 셀에서 값만 추출
            uniprots.append(ID)
            i += 1


    one = []
    intersection_uniprots = []
    for u in uniprots:
        if u not in one:
            one.append(u)
        else:
            if u not in intersection_uniprots:
                intersection_uniprots.append(u)

    # print(intersection_uniprots)
    # print(uniprots)
    # print(len(uniprots))


    ue_df = pd.read_csv('data/ensp_uniprot.txt', delimiter ='\t')
    uz_df = pd.read_csv("data/Uniprot_to_entrez_id.csv")
    ensp = []
    entez = []

    for uniprot in intersection_uniprots:
        find_row = ue_df[(ue_df['Uniprot'] == uniprot)]
        find_row2 = uz_df[(uz_df['Uniprot'] == uniprot)]
        if find_row.empty:
          # print("empty")
          pass

        else:
          # print(find_row)
          # print(len(find_row))
          i = 0
          while i < len(find_row):
            ID = find_row.iloc[i]['ENSP']  # 셀에서 값만 추출
            ensp.append(ID)
            i += 1

        if find_row2.empty:
            # print("empty")
            pass
        else:
            # print(find_row2)
            # print(len(find_row2))
            j = 0
            while j < len(find_row2):
                ID2 = find_row2.iloc[j]['Entrez_id']  # 셀에서 값만 추출
                entez.append(ID2)
                j += 1

    ensp = list(set(ensp))
    entez = list(set(entez))



    print(entez)
    print(len(entez))

    print(ensp)
    print(len(ensp))

    str_df = pd.read_csv('data/and_network.txt', delimiter =',', header=None)
    pair = []
    result = []

    # print(str_df)
    c = 1
    for e in ensp:

        find_row = str_df[(str_df[0] == e)]
        # print(find_row)
        if find_row.empty:
            # print("empty")
            pass
        else:
            pair.append(e)
            i = 0
            while i < len(find_row):
                ID = find_row.iloc[i][1]  # 셀에서 값만 추출
                pair.append(ID)
                i += 1
            result.append(pair)
            pair = []

    unit_result = []
    temp_result = []
    pair = []
    for temp_r in result:
        # print(temp_r)
        for r in temp_r:
            # print(r)
            find_row = ue_df[(ue_df['ENSP'] == r)]
            if find_row.empty:
              # print("empty")
              pass

            else:
                # print(find_row)
                # print(len(find_row))
                i = 0
                while i < len(find_row):
                    ID = find_row.iloc[i]['Uniprot']  # 셀에서 값만 추출
                    temp_result.append(ID)
                    i += 1

        unit_result.append(temp_result)
        temp_result = []


    # ensp = ','.join(ensp)

    # print(result)
    # print(len(result))
    # print(unit_result)
    # print(len(unit_result))


    inter_result = []
    for r in unit_result:
        r = ','.join(r)
        inter_result.append(r)

    print(inter_result)

    # 하이퍼

    hy_df1 = pd.read_csv("data/go_id_term.csv", names=['id', 'term'])
    hy_df2 = pd.read_csv("data/entrez_go.csv", names=['id_', 'entrez'])

    hy_df2_list = hy_df2['id_'].values.tolist()
    g_entrez = list(set(hy_df2_list))

    drug_entez = entez
    Go_temp = []
    GO_result = []

    for g in g_entrez:
        GO_entez = []
        find_row = hy_df2[(hy_df2['id_'] == g)]
        if find_row.empty:
            pass
        else:
            i = 0
            while i < len(find_row):
                GO_ID = find_row.iloc[i]['entrez']
                GO_entez.append(GO_ID)
                i += 1
            N = 20237
            n = len(list(GO_entez))
            G = len(drug_entez)
            x = set(GO_entez).intersection(set(drug_entez))
            x = len(list(x))

            if n < x:
                raise ValueError("Cannot observe more good elements than the sample size")
            if N < n:
                raise ValueError("Population size cannot be smaller than sample")
            if N < G:
                raise ValueError("Number of good elements can't exceed the population size")
            if G < x:
                raise ValueError("Number of observed good elements can't exceed the number in the population")

            plower = hypergeom.cdf(x, N, G, n)
            pupper = hypergeom.sf(x - 1, N, G, n)
            pvalue = 2 * np.min([plower, pupper, 0.5])

            if pvalue != 1:
                Go_temp.append(pvalue)
                Go_temp.append(g)
                print(Go_temp)
                GO_result.append(Go_temp)
            Go_temp = []
    print(GO_result)
    GO_result.sort()
    print(GO_result)
    print(len(GO_result))

    cnt = 0
    top_10 = []
    for r in GO_result:
        top_10.append(r)
        cnt += 1
        if cnt == 10:
            break

    print(top_10)

    top10_result = []
    for t in top_10:
        temp = []
        find_row = hy_df1[(hy_df1['id'] == t[1])]
        if find_row.empty:
            pass
        else:
            i = 0
            while i < len(find_row):
                term = find_row.iloc[i]['term']
                temp.append(t[0])
                temp.append(term)
                i += 1
            top10_result.append(temp)

    print(top10_result)



    return [drug_a+' ('+drug_a_name+')', drug_b+' ('+drug_b_name+')', intersection_uniprots, inter_result, top10_result]

if __name__ == '__main__':
    predict_cy('DB01068', 'DB00951')

