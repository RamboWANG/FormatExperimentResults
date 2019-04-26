# coding=utf-8

datasets_names = ["iris", "vowel", "seed", "heart", "balance"]
hsizes = {"iris":[3,10,20], "vowel":[5,10,20], "seed":[5,10,20], "heart":[5,10,20], "balance":[5,10,20]}

for data_tag in datasets_names:
    hsize_vec = hsizes[data_tag]
    for hsize in hsize_vec:
        for diff in ["T", "F"]:
            filename = "b3x2_"+data_tag+"_"+str(hsize)+"_"+diff+".R"
            f = open(filename, 'w')
            f.write('setwd("/share/home/wrb/rtest/bcv/R/")\n')
            f.write('source("tests/NIPS2019/st_uci_mlp_3x2bcv_ge_yield.R", encoding="UTF-8")\n')
            f.write('ge.estimator.master("'+data_tag+'",'+str(hsize)+',diff='+diff+')')
            f.close()
            filename_brhs = "brhs_"+data_tag+"_"+str(hsize)+"_"+diff+".R"
            f = open(filename_brhs, 'w')
            f.write('setwd("/share/home/wrb/rtest/bcv/R/")\n')
            f.write('source("tests/NIPS2019/st_uci_mlp_brhs4_ge_yield.R", encoding="UTF-8")\n')
            f.write('ge.estimator.master("'+data_tag+'",'+str(hsize)+',diff='+diff+')')
            f.close()
        pass