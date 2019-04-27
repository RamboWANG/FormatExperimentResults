# coding=utf-8

datasets_names = ["balance", "diabetes", "glass", "heart", "ionosphere", "iris", "vehicle", "wine", "yeast", "seed"]

for data_tag in datasets_names:
    filename = "b3x2_rep_"+data_tag+".R"
    f = open(filename, 'w')
    f.write('setwd("/share/home/wrb/rtest/bcv/R/")\n')
    f.write('source("tests/NIPS2019/rep_uci_3x2bcv_ge_yield_100.R", encoding="UTF-8")\n')
    f.write('ge.estimator.master("'+data_tag+'")')
    f.close()
    filename_brhs = "brhs4_rep_"+data_tag+".R"
    f = open(filename_brhs, 'w')
    f.write('setwd("/share/home/wrb/rtest/bcv/R/")\n')
    f.write('source("tests/NIPS2019/rep_uci_brhs4_ge_yield_100.R", encoding="UTF-8")\n')
    f.write('ge.estimator.master("' + data_tag + '")')
    f.close()
    pass