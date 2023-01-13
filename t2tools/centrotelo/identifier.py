class CentroTeloIdentifier:
    """
    This class is base class for identifying centromeres and telomeres

    Attributes:
        _bed_list:  a 2-dimensions list like below:
                [[seq_name1, 1, 1000, 1000, 50, 1000, ATCG, ATCG...ATCG],
                 ...
                ]
    """

    def __init__(self, bed_list):
        """
        Init attributes

        Args:
            bed_list: simplified bed loaded by io.TRFData
        """
        self._bed_list = bed_list


class CentroIdentifier(CentroTeloIdentifier):
    """
    This class is a subclass of CentroTeloIdentifier for identifying centromeres
    Attributes:
        __centro_list: a list of centromeres
    """

    def __init__(self, bed_list):
        """
        Init attributes
        bed_list: simplified bed loaded by io.TRFData
        """
        super().__init__(bed_list)
        self.__centro_list = []

    def identify(self):
        """This function is for identifying centromeres from trf result which loaded by io.TRFData

        Returns:

        """
        length_db = {}
        for _, _, _, length, _, _, pattern, _ in self._bed_list:
            pattern_length = len(pattern)
            if pattern_length < 50 or pattern_length > 200:
                continue

            if pattern_length not in length_db:
                length_db[pattern_length] = 0
            length_db[pattern_length] += length

        max_length = 0
        max_pattern = 0
        for pattern_length in length_db:
            if length_db[pattern_length] > max_length:
                max_length = length_db[pattern_length]
                max_pattern = pattern_length

        for _ in self._bed_list:
            # each line of _bed_list is like below:
            # sid, start_pos, end_pos, length, copy_num, score, pattern, seq
            pattern_length = len(_[-2])
            copy_num = _[4]
            score = _[5]
            if copy_num < 10 or score < 1000:
                continue

            if max_pattern - 1 <= pattern_length <= max_pattern + 1:
                self.__centro_list.append(_)

    def get_centro_list(self):
        """This function return the centromere information identified

        Returns:
            A list of centromere information
        """
        return self.__centro_list


class TeloIdentifier(CentroTeloIdentifier):
    """
    This class is a subclass of CentroTeloIdentifier for identifying telomeres
    Attributes:
        __telo_list: a list of telomeres
    """

    def __init__(self, bed_list, seq_length, is_split):
        """
        Init attributes
        Args:
            bed_list: simplified bed loaded by io.TRFData
            seq_length: a dictionary of all sequences length
            is_split: if the sequence of fasta is split, position need convert with offset
        """
        super().__init__(bed_list)
        self.__telo_list = []
        self.__seq_length = seq_length
        self.__is_split = is_split

    def identify(self):
        """This function is for identifying telomeres from trf result which loaded by io.TRFData

        Returns:

        """
        telo_pattern = "TTTAGGG" * 10
        rev_telo_pattern = "CCCTAAA" * 10
        if self.__is_split:
            length_db = {}
            for id in self.__seq_length:
                sid = id.split('_')[0]
                if sid not in length_db:
                    length_db[sid] = 0
                length_db[sid] += self.__seq_length[id]
            self.__seq_length = length_db

        for _ in self._bed_list:
            # each line of _bed_list is like below:
            # sid, start_pos, end_pos, telo_size, telo_pattern, pos, copy_num
            sid = _[0]
            start_pos = _[1]
            end_pos = _[2]
            if self.__is_split:
                sid, offset, _ = sid.split('_')
                offset = int(offset)-1
                start_pos += offset
                end_pos += offset

            if start_pos < self.__seq_length[sid] / 2.:
                pos_marker = "start"
            elif end_pos > self.__seq_length[sid] / 2.:
                pos_marker = "end"
            else:
                continue
            if telo_pattern in _[-1] or rev_telo_pattern in _[-1]:
                self.__telo_list.append([sid, start_pos, end_pos, _[3], _[-2], pos_marker, _[4]])

    def get_telo_list(self):
        """This function return the centromere information identified

        Returns:
            A list of telomere information
        """
        return self.__telo_list
