from os import popen


class Runner:
    """
    This class is for running command and getting results

    Attributes:
        _cmd:   command for running
        _res:   a list for storing result lines
    """
    def __init__(self):
        """
        Init attributes
        """
        self._cmd = ""
        self._res = []

    def set_command(self, cmd):
        """This function is for setting command to run

        Args:
            cmd:

        Returns:
            None
        """
        self._cmd = "\"%s\"" % cmd

    def print_command(self):
        """This function is for printing current command

        Returns:
            None
        """
        print(self._cmd)

    def run(self):
        """This function is for running command with os.popen, and store result to list _res

        Returns:
            None
        """
        with popen(self._cmd, 'r') as fin:
            for line in fin:
                self._res.append(line)

    def get_result(self):
        """This function return a string of result

        Returns:
            A result string
        """
        return ''.join(self._res)


class CentroTeloTRFRunner(Runner):
    """
    This class is a subclass of Runner, it can create command for identifying centromeres and telomeres
    """
    def set_command(self, fasta_file):
        """This function is to generate command with trf for centromeres and telomeres

        Args:
            fasta_file: input fasta file

        Returns:
            None
        """
        TRF_PARAM = {
            "File": "\"%s\"" % fasta_file,
            "Match": 1,
            "Mismatch": 1,
            "Delta": 2,
            "PM": 80,
            "PI": 5,
            "Minscore": 200,
            "MaxPeriod": 2000,
            "options": "-d -h"
        }
        param_order = ["File", "Match", "Mismatch", "Delta", "PM", "PI", "Minscore", "MaxPeriod", "options"]
        cmd_list = [str(TRF_PARAM[_]) for _ in param_order]
        self._cmd = "trf %s" % (' '.join(cmd_list))
