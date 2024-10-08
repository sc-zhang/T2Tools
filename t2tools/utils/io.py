from os import path, makedirs, listdir
from pathos.multiprocessing import Pool


class Fasta:
    """
    This is a class for fasta file operating
    Attributes:
        __fasta_file:   A string of input fasta file name
        __fasta_db:     A dictionary for all sequences in fasta file, key means sequence id, value means sequence
    """

    def __init__(self):
        """
        Init attributes
        """
        self.__fasta_file = ""
        self.__fasta_db = {}

    @staticmethod
    def get_fasta_gaps(fasta_file):
        total_cnt = 0
        gap_db = {}
        with open(fasta_file, 'r') as fin:
            sid = ''
            gap_cnt = 0
            for line in fin:
                if line[0] == '>':
                    if sid != '':
                        gap_db[sid] = gap_cnt
                        total_cnt += gap_cnt
                    sid = line.strip()[1:]
                    gap_cnt = 0
                    last_base = ''
                else:
                    for i in range(len(line.strip())):
                        if line[i].lower() == 'n' and last_base != 'n':
                            gap_cnt += 1
                        last_base = line[i].lower()
            gap_db[sid] = gap_cnt
            gap_db["Total"] = total_cnt
        return gap_db

    def load_fasta(self, fasta_file):
        """This is fasta load function

        It will read fasta file and store all sequences in self.__fasta_db and length of all sequences in
        self.__fasta_len

        Args:
            fasta_file: fasta file for loading

        Returns:

        """
        with open(fasta_file, 'r') as fin:
            sid = ""
            seq = []
            for line in fin:
                if line[0] == '>':
                    if len(seq) != 0:
                        self.__fasta_db[sid] = ''.join(seq)
                    sid = line.strip().split()[0][1:]
                    seq = []
                else:
                    seq.append(line.strip())
            if len(seq) != 0:
                self.__fasta_db[sid] = ''.join(seq)

    def load_fasta_dir(self, fasta_dir):
        """This function will load all fasta file in fasta_dir

        Args:
            fasta_dir: a directory contain all fasta files to be load

        Returns:

        """
        for fn in listdir(fasta_dir):
            if fn.endswith('.fa') or fn.endswith('.fasta'):
                self.load_fasta(path.join(fasta_dir, fn))

    def get_length(self):
        """This function return the dictionary of length of sequences

        Returns:
            A dictionary of length of sequences
        """
        # calculate fasta length
        return {sid: len(self.__fasta_db[sid]) for sid in self.__fasta_db}

    @staticmethod
    def __split_seq(out_dir, sid, seq, window_size, step_size):
        """This is a function for split a sequence with window_size and step_size

        For downstream analysing, we need split sequence into pieces.

        Args:
            out_dir:        directory for store separated sequences
            sid:            sequence id
            seq:            sequence string
            window_size:    size of window
            step_size:      size of step

        Returns:

        """
        start_pos = 0
        end_pos = window_size
        seq_length = len(seq)
        while start_pos < seq_length:
            out_fasta_file = "%s:::%d:::%d.fasta" % (sid, start_pos + 1, end_pos)
            with open(path.join(out_dir, out_fasta_file), 'w') as fout:
                fout.write(">%s:::%d:::%d\n%s\n" % (sid, start_pos + 1, end_pos, seq[start_pos: end_pos]))
            start_pos += step_size
            end_pos = min(start_pos + window_size, seq_length)

    def split_with_win(self, out_dir, window_size, step_size, threads):
        """This function is for splitting fasta by calling __split_seq with multi threads

        Args:
            threads:        thread count for splitting fasta
            out_dir:        directory for store separated sequences
            window_size:    size of window
            step_size:      size of step

        Returns:

        """
        window_size = int(window_size)
        step_size = int(step_size)
        if not path.exists(out_dir):
            makedirs(out_dir)

        pool = Pool(processes=threads)
        for sid in self.__fasta_db:
            pool.apply_async(self.__split_seq, (out_dir, sid, self.__fasta_db[sid], window_size, step_size,))
        pool.close()
        pool.join()

    @staticmethod
    def __write_seq(out_dir, sid, seq):
        out_fasta_file = path.join(out_dir, "%s.fasta" % sid)
        with open(out_fasta_file, "w") as fout:
            fout.write(">%s\n%s\n" % (sid, seq))

    def split_fasta(self, out_dir, threads):
        """This function is for extracting sequences from fasta

                Args:
                    threads:        thread count for splitting fasta
                    out_dir:        directory for store separated sequences

                Returns:

                """

        if not path.exists(out_dir):
            makedirs(out_dir)

        pool = Pool(processes=threads)
        for sid in self.__fasta_db:
            pool.apply_async(self.__write_seq, (out_dir, sid, self.__fasta_db[sid],))
        pool.close()
        pool.join()


class TRFData:
    """
    This class is for parsing result generated by trf
    Attributes:
        __bed_list: A 2-dimensions list like below:
                    [[seq_name1, 1, 1000, 1000, 50, 1000, ATCG, ATCG...ATCG],
                     ...
                    ]
    """

    def __init__(self):
        """
        Init attributes
        """
        self.__bed_list = []

    @staticmethod
    def __load_file(dat_file):
        """This function is for loading dat file and return a generator

        Args:
            dat_file: trf dat file for parsing

        Returns:
            A generator for read line of dat file
        """
        with open(dat_file, 'r') as fin:
            for line in fin:
                yield line

    def add_dat(self, dat_file):
        """This function is for simplifying dat file and writing it to bed file

        For down stream analyzing, we only need 5 attributes: sequence_name start_pos end_pos length sequence.

        Args:
            dat_file: trf dat file for parsing
        Returns:
            A 2-dimensions list like below:
            [[seq_name1, 1, 1000, 1000, 50, 1000, ATCG, ATCG...ATCG],
             ...
            ]
        """
        sid = ""
        for line in self.__load_file(dat_file):
            if len(line.strip()) == 0:
                continue
            data = line.strip().split()
            if (not data[0].startswith("Sequence")) and len(data) < 10:
                continue
            if data[0].startswith("Sequence"):
                sid = data[1]
            else:
                start_pos = int(data[0])
                end_pos = int(data[1])
                length = abs(start_pos - end_pos) + 1
                pattern = data[-2]
                copy_num = float(data[3])
                score = float(data[7])
                seq = data[-1]
                self.__bed_list.append([sid, start_pos, end_pos, length, copy_num, score, pattern, seq])

    def get_bed_list(self):
        """This function is for getting __bed_list for down stream analyzing

        Returns:
            __bed_list
        """

        return self.__bed_list
