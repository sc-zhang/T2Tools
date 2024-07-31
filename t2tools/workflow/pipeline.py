from t2tools.centrotelo.identifier import CentroIdentifier, TeloIdentifier
from t2tools.centrotelo.visualizer import Visualizer
from t2tools.utils.runner import CentroTeloTRFRunner
from t2tools.utils.io import Fasta, TRFData
from t2tools.utils.message import Message
from os import path, makedirs, system, listdir, chdir
from pathos.multiprocessing import Pool


def run_trf(trf_dir, fasta_file):
    chdir(trf_dir)
    r = CentroTeloTRFRunner()
    r.set_command(fasta_file)
    r.print_command()
    r.run()


def main(args):
    input_fasta = args.fasta
    out_dir = args.output
    out_dir = path.abspath(out_dir)
    window_size = args.window_size
    step_size = args.step_size
    is_split = args.split
    lower = args.lower
    upper = args.upper
    minium_copy_number = args.copy
    minium_score = args.score
    threads = args.threads
    pipeline(input_fasta, out_dir, window_size, step_size, is_split,
             lower, upper, minium_copy_number, minium_score, threads)


def pipeline(input_fasta, out_dir, window_size, step_size, is_split,
             lower, upper, minium_copy_number, minium_score, threads):
    if not path.exists(out_dir):
        makedirs(out_dir)

    Message.info("Loading fasta")
    if is_split:
        fa_dir = path.join(out_dir, 'separated')
        if not path.exists(fa_dir):
            makedirs(fa_dir)

            if not path.isfile(input_fasta):
                Message.info("Fatal error: split function can only apply on single fasta file")
                exit(-1)
            if not window_size or not step_size:
                Message.info("Fatal error: window_size and step_size is required while split is on")
                exit(-1)

            # Split fasta with slide windows
            window_size = float(window_size)
            step_size = float(step_size)
            fa_loader = Fasta()
            fa_loader.load_fasta(input_fasta)
            fa_loader.split_fasta(fa_dir, window_size, step_size, threads)
        fa_loader = Fasta()
        fa_loader.load_fasta_dir(fa_dir)
    else:
        # For single fasta file, link it to outdir/separated/ directory
        if path.isfile(input_fasta):
            fa_dir = path.join(out_dir, 'separated')
            if not path.exists(fa_dir):
                makedirs(fa_dir)

            system("ln -s %s %s/input.fa" % (path.abspath(input_fasta), fa_dir))
        else:
            fa_dir = path.abspath(input_fasta)

        fa_loader = Fasta()
        fa_loader.load_fasta_dir(fa_dir)

    Message.info("Running trf")
    # Running trf multiprocessing
    trf_dir = path.join(out_dir, "trf_dat")
    if not path.exists(trf_dir):
        makedirs(trf_dir)

        pool = Pool(processes=threads)
        for fasta_file in listdir(fa_dir):
            if not fasta_file.endswith(".fa") and not fasta_file.endswith(".fasta"):
                continue
            fasta_file = path.join(fa_dir, fasta_file)
            pool.apply_async(run_trf, (trf_dir, fasta_file,))
        pool.close()
        pool.join()
    else:
        Message.info("%s found, skip." % trf_dir)

    Message.info("Loading trf results")
    trf_loader = TRFData()
    for trf_file in listdir(trf_dir):
        if trf_file.endswith('.dat'):
            trf_loader.add_dat(path.join(trf_dir, trf_file))

    with open(path.join(out_dir, "trf_total.bed"), 'w') as fout:
        for _ in trf_loader.get_bed_list():
            fout.write("%s\n" % ('\t'.join(map(str, _))))

    Message.info("Visualizing trf results")
    visualizer = Visualizer(trf_loader.get_bed_list(), is_split, lower, upper)
    out_pdf = path.join(out_dir, "whole.pdf")
    visualizer.visualize(out_pdf, "whole")
    out_pdf = path.join(out_dir, "seperated.pdf")
    visualizer.visualize(out_pdf, "single")

    Message.info("Identifying centromeres and telomeres")
    centro = CentroIdentifier(trf_loader.get_bed_list(), is_split, lower, upper, minium_copy_number, minium_score)
    centro.identify()
    with open(path.join(out_dir, "centro.list"), 'w') as fout:
        fout.write("#sid\tstart_pos\tend_pos\tlength\tcopy_num\tscore\tpattern\tseq\n")
        for _ in sorted(centro.get_centro_list()):
            fout.write("%s\n" % ('\t'.join(map(str, _))))

    telo = TeloIdentifier(trf_loader.get_bed_list(), fa_loader.get_length(), is_split)
    telo.identify()
    with open(path.join(out_dir, "telo.list"), 'w') as fout:
        fout.write("#sid\tstart_pos\tend_pos\ttelo_size\ttelo_pattern\tpos\tcopy_num\n")
        for _ in sorted(telo.get_telo_list()):
            fout.write("%s\n" % ('\t'.join(map(str, _))))

    Message.info("Finished")
