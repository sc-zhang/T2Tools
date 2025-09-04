from t2tools.centel.visualizer import Visualizer
from t2tools.utils.trf2bed import trf2bed
from t2tools.utils.message import Message
from os import path, makedirs


def main(args):
    input_dir = args.input
    out_dir = args.output
    out_dir = path.abspath(out_dir)
    lower = args.lower
    upper = args.upper

    pipeline(input_dir, out_dir, lower, upper)


def pipeline(input_dir, out_dir, lower, upper):
    if not path.exists(out_dir):
        makedirs(out_dir)
    Message.info("Visualizing trf results")
    trf_loader = trf2bed(input_dir, out_dir)
    Message.info("Plotting")
    plotter(trf_loader, out_dir, lower, upper, False)
    Message.info("Finished")


def plotter(trf_loader, out_dir, lower, upper, is_split):
    visualizer = Visualizer(trf_loader.get_bed_list(), is_split, lower, upper)
    out_pdf = path.join(out_dir, "whole.pdf")
    status = visualizer.visualize(out_pdf, "whole")
    if not status:
        Message.error("Could not draw whole figure")
    out_pdf = path.join(out_dir, "separated.pdf")
    status = visualizer.visualize(out_pdf, "single")
    if not status:
        Message.error(
            "Could not draw separated figure, may caused by more than 100 sequences"
        )

    max_monomers_info = visualizer.get_max_monomers_info()
    with open(path.join(out_dir, "centro_max_monomers.list"), "w") as fout:
        fout.write("#sid\tmonomer_length\tmonomer_count\n")
        for sid in sorted(max_monomers_info):
            if sid != "Whole":
                fout.write(
                    "%s\t%d\t%d\n"
                    % (sid, max_monomers_info[sid][0], max_monomers_info[sid][1])
                )
        fout.write(
            "Whole\t%d\t%d\n"
            % (max_monomers_info["Whole"][0], max_monomers_info["Whole"][1])
        )

    return trf_loader
