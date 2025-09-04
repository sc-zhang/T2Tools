from t2tools.utils.io import TRFData
from t2tools.utils.message import Message
from os import path, listdir


def trf2bed(trf_dir, out_dir):
    Message.info("Loading trf results")
    trf_loader = TRFData()
    for trf_file in listdir(trf_dir):
        if trf_file.endswith(".dat"):
            trf_loader.add_dat(path.join(trf_dir, trf_file))

    with open(path.join(out_dir, "trf_total.bed"), "w") as fout:
        for _ in trf_loader.get_bed_list():
            fout.write("%s\n" % ("\t".join(map(str, _))))

    return trf_loader
