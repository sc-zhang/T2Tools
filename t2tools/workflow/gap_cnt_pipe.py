from t2tools.utils.io import Fasta
from t2tools.utils.message import Message
import re


def main(args):
    input_fasta = args.fasta
    output_file = args.output

    if output_file:
        Message.info("Getting gap counts")
        gap_db = Fasta.get_fasta_gaps(input_fasta)
        Message.info("Writing gap counts")
        with open(output_file, 'w') as fout:
            for sid in sorted(gap_db, key=lambda x: int(re.findall(r'(\d+)', x)[0])
                              if len(re.findall(r'(\d+)', x)) > 0 else 1000):
                if sid != "Total":
                    fout.write("%s\t%s\n" % (sid, gap_db[sid]))
            fout.write("Total\t%s\n" % gap_db["Total"])
        Message.info("Finished")
    else:
        gap_db = Fasta.get_fasta_gaps(input_fasta)
        for sid in sorted(gap_db, key=lambda x: int(re.findall(r'(\d+)', x)[0])
                          if len(re.findall(r'(\d+)', x)) > 0 else 1000):
            if sid != "Total":
                print("%s\t%s" % (sid, gap_db[sid]))
        print("Total\t%s" % gap_db["Total"])
