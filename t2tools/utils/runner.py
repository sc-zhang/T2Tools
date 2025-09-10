from subprocess import Popen, PIPE
from t2tools.utils.message import Message


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
        self._res = ""
        self._err = ""

    def set_command(self, cmd):
        """This function is for setting command to run

        Args:
            cmd:

        Returns:
            None
        """
        self._cmd = '"%s"' % cmd

    def print_command(self):
        """This function is for printing current command

        Returns:
            None
        """
        Message.info(self._cmd)

    def run(self):
        """This function is for running command with os.popen, and store result to list _res

        Returns:
            None
        """
        p = Popen(self._cmd, stdout=PIPE, stderr=PIPE, shell=True, encoding="utf-8")
        self._res, self._err = p.communicate()

    def get_result(self):
        return self._res

    def get_err(self):
        return self._err


class CenTelTRFRunner(Runner):
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
            "File": '"%s"' % fasta_file,
            "Match": 1,
            "Mismatch": 1,
            "Delta": 2,
            "PM": 80,
            "PI": 5,
            "Minscore": 200,
            "MaxPeriod": 2000,
            "options": "-d -h",
        }
        param_order = [
            "File",
            "Match",
            "Mismatch",
            "Delta",
            "PM",
            "PI",
            "Minscore",
            "MaxPeriod",
            "options",
        ]
        cmd_list = [str(TRF_PARAM[_]) for _ in param_order]
        self._cmd = "trf %s" % (" ".join(cmd_list))

    def set_command_with_custom_trf_options(self, fasta_file, trf_options):
        """This function is to generate command with trf for centromeres and telomeres
            with custom options

        Args:
            fasta_file: input fasta file
            trf_options: custom trf options

        Returns:
            None
        """
        self._cmd = 'trf "%s" %s -d -h' % (fasta_file, trf_options)
