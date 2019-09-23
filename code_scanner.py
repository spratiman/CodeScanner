"""Scan the program file and return information about commented lines."""

import os

from argparse import ArgumentParser


class Type:
    """Get language specific information for the type of file."""

    def __init__(self, extension):
        self.extension = extension
        self.single_comment = self.get_single_comment(extension)
        self.multi_comment = self.get_multi_comment(extension)

    @staticmethod
    def get_single_comment(extension):
        """
        Return language specific single line comment identifier for file type.

        Returns:
            str: single line comment identifier

        """
        identifier = {
            '.java': '//',
            '.js': '//',
            '.py': '#'
        }

        return identifier[extension]

    @staticmethod
    def get_multi_comment(extension):
        """
        Return language specific multi line comment identifier for file type.

        Returns:
            tuple: start and end string of multi line comment identifier

        """
        identifier = {
            '.java': ('/*', '*/'),
            '.js': ('/*', '*/'),
            '.py': ('#')
        }

        return identifier[extension]


class Scan:
    """Object to process various information regarding the code lines."""

    def __init__(self, f, comment_identifier):
        """
        Initialize the Scan class.

        Args:
            f: File to be scanned.

        Returns:
            None

        """
        self.lines = 0
        self.todo = 0
        self.single_line_comments = 0
        self.multi_line_comments = 0
        self.block_comments = 0
        self.process_file(self, f, comment_identifier)

    @staticmethod
    def process_file(self, file, comment_identifier):
        """
        Check each line of the file.

        Returns:
            None

        """
        lines = file.readlines()
        self.lines = len(lines)
        line_type = {k+1: "u" for k in range(self.lines)}

        for i in range(self.lines):
            line = lines[i]
            next_line = ""
            if i < self.lines - 1:
                next_line = lines[i + 1]

            if self.is_single(line.strip(), comment_identifier):
                # print(line.strip())
                if line_type[i+1] == "u":
                    line_type[i+1] = "s"
            elif self.is_multiple(line.strip(), comment_identifier):
                print(line.strip())


        self.update_counts(self, line_type, lines)

    @staticmethod
    def is_single(line, comment_identifier):
        if line != "" and line.startswith(comment_identifier.single_comment):
            return True
        elif line != "" and not line.startswith(comment_identifier.single_comment) and comment_identifier.single_comment in line:
            return True
        return False

    @staticmethod
    def is_multiple(line, comment_identifier):
        if line != "" and line.startswith(comment_identifier.single_comment):
            return True
        elif line != "" and not line.startswith(comment_identifier.single_comment) and comment_identifier.single_comment in line:
            return True
        return False

    @staticmethod
    def update_counts(self, line_type, lines):
        for key, val in line_type.items():
            if val == "s":
                self.single_line_comments += 1
                if "TODO:" in lines[key-1]:
                    self.todo += 1


def main(file):
    """
    Execute the scanner on the file and display report about commented lines.

    Args:
        file: This is the input file to be scanned.

    Returns:
        None

    Raises:
        FileNotFoundError
        TypeError

    """
    extension = os.path.splitext(file)[-1].lower()
    if (file.startswith(".") and not (file.startswith("./")
                                      or file.startswith(".\\"))) or (extension
                                                                      == ""):
        raise TypeError("Invalid program file")
    else:
        comment_identifier = Type(extension)
        with open(file) as f:
            scan = Scan(f, comment_identifier)
            print("Total # of lines: {} \nTotal # of single line comments: {}\nTotal # of TODO's: {}".format(scan.lines, scan.single_line_comments, scan.todo))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", help='Program file to check', required=True)
    args = parser.parse_args()
    main(args.f)
