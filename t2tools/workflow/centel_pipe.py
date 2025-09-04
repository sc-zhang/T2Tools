from t2tools.centel.identifier import CentroIdentifier, TeloIdentifier
from t2tools.workflow.visual_trf_pipe import plotter
from t2tools.utils.runner import CenTelTRFRunner
from t2tools.utils.io import Fasta
from t2tools.utils.trf2bed import trf2bed
from t2tools.utils.message import Message
from os import path, makedirs, listdir, chdir
from pathos.multiprocessing import Pool


def run_trf(trf_dir, fasta_file, trf_options):
    chdir(trf_dir)
    r = CenTelTRFRunner()
    if not trf_options:
        r.set_command(fasta_file)
    else:
        r.set_command_with_custom_trf_options(fasta_file, trf_options)
    r.print_command()
    r.run()
    return r.get_result(), r.get_err()


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
    trf_options = args.trf_options if args.trf_options else ""
    if args.telo_type == "plant":
        telo_pattern = "TTTAGGG" * 10
        rev_telo_pattern = "CCCTAAA" * 10
    else:
        telo_pattern = "TTAGGG" * 10
        rev_telo_pattern = "CCCTAA" * 10
    threads = args.threads
    pipeline(
        input_fasta,
        out_dir,
        window_size,
        step_size,
        is_split,
        lower,
        upper,
        telo_pattern,
        rev_telo_pattern,
        minium_copy_number,
        minium_score,
        trf_options,
        threads,
    )


def pipeline(
    input_fasta,
    out_dir,
    window_size,
    step_size,
    is_split,
    lower,
    upper,
    telo_pattern,
    rev_telo_pattern,
    minium_copy_number,
    minium_score,
    trf_options,
    threads,
):
    if not path.exists(out_dir):
        makedirs(out_dir)

    Message.info("Loading fasta")
    if is_split:
        fa_dir = path.join(out_dir, "separated")
        if not path.exists(fa_dir):
            makedirs(fa_dir)

            if not path.isfile(input_fasta):
                Message.info(
                    "Fatal error: split function can only apply on single fasta file"
                )
                exit(-1)
            if not window_size or not step_size:
                Message.info(
                    "Fatal error: window_size and step_size is required while split is on"
                )
                exit(-1)

            # Split fasta with slide windows
            window_size = float(window_size)
            step_size = float(step_size)
            fa_loader = Fasta()
            fa_loader.load_fasta(input_fasta)
            fa_loader.split_with_win(fa_dir, window_size, step_size, threads)
        fa_loader = Fasta()
        fa_loader.load_fasta_dir(fa_dir)
    else:
        # For single fasta file, link it to outdir/separated/ directory
        if path.isfile(input_fasta):
            fa_dir = path.join(out_dir, "separated")
            if not path.exists(fa_dir):
                makedirs(fa_dir)
            fa_loader = Fasta()
            fa_loader.load_fasta(input_fasta)
            fa_loader.split_fasta(fa_dir, threads)
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
        res = []
        for fasta_file in listdir(fa_dir):
            if not fasta_file.endswith(".fa") and not fasta_file.endswith(".fasta"):
                continue
            fasta_file = path.join(fa_dir, fasta_file)
            r = pool.apply_async(
                run_trf,
                (
                    trf_dir,
                    fasta_file,
                    trf_options,
                ),
            )
            res.append(r)
        pool.close()
        pool.join()

        flog = open(path.join(out_dir, "trf.log"), "w")
        ferr = open(path.join(out_dir, "trf.err"), "w")
        for r in res:
            log_info, err_info = r.get()
            flog.write("%s\n" % log_info)
            ferr.write("%s\n" % err_info)
    else:
        Message.info("%s found, skip." % trf_dir)

    Message.info("Visualizing trf results")
    trf_loader = trf2bed(trf_dir, out_dir)
    plotter(trf_loader, out_dir, lower, upper, is_split)

    Message.info("Identifying centromeres and telomeres")
    centro = CentroIdentifier(
        trf_loader.get_bed_list(),
        is_split,
        lower,
        upper,
        minium_copy_number,
        minium_score,
    )
    centro.identify()
    with open(path.join(out_dir, "centro.list"), "w") as fout:
        fout.write("#sid\tstart_pos\tend_pos\tlength\tcopy_num\tscore\tpattern\tseq\n")
        for _ in sorted(centro.get_centro_list()):
            fout.write("%s\n" % ("\t".join(map(str, _))))

    telo = TeloIdentifier(
        trf_loader.get_bed_list(),
        fa_loader.get_length(),
        telo_pattern,
        rev_telo_pattern,
        is_split,
    )
    telo.identify()
    with open(path.join(out_dir, "telo.list"), "w") as fout:
        fout.write("#sid\tstart_pos\tend_pos\ttelo_size\ttelo_pattern\tpos\tcopy_num\n")
        for _ in sorted(telo.get_telo_list()):
            fout.write("%s\n" % ("\t".join(map(str, _))))

    Message.info("Finished")
