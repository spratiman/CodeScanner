"""Scan the program file and return information about commented lines."""

import os

from argparse import ArgumentParser


class Type:
    """Get language specific information for the type of file."""

    def __init__(self, extension):
        """
        Initialize the Type class.

        Args:
            extension: the type of the programming language.

        Returns:
            None

        """
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
        Check each line of the file and compute the count.

        Returns:
            None

        """
        lines = file.readlines()
        self.lines = len(lines)
        # Initialize a map of line numbers to its type, where
        # "u" = unchecked line
        # "s" = line with a single comment or inline comment
        # "m" = line with a multi comment or inline multi comment
        line_type = {k+1: "u" for k in range(self.lines)}

        for i in range(self.lines):
            line = lines[i]
            next_line = ""
            previous_line = ""
            # Assign the next and previous_line line
            if i < self.lines - 1:
                next_line = lines[i + 1]
            if i > 0:
                previous_line = lines[i - 1]

            if self.is_single(line.strip(), comment_identifier):
                # Map line type to "s"
                if line_type[i + 1] == "u":
                    line_type[i + 1] = "s"

            if self.is_multiple(self, line.strip(), comment_identifier,
                                next_line.strip(), previous_line.strip()):
                # Map line type to "m"
                if line_type[i + 1] == "u":
                    line_type[i + 1] = "m"
                elif comment_identifier.extension == ".py" and line_type[i + 1] == "s":
                    line_type[i + 1] = "m"

        self.update_counts(self, line_type, lines)

    @staticmethod
    def is_single(line, comment_identifier):
        """
        Check if the line contains a single line comment.

        Args:
            line: line to be checked.
            comment_identifier: Type object with language specific comment
                                 information

        Returns:
            bool: Flag for the check

        """
        if line != "" and line.startswith(comment_identifier.single_comment):
            # the whole line is a single comment
            return True
        elif line != "" and not line.startswith(comment_identifier.single_comment) and comment_identifier.single_comment in line:
            # the line has an in-line single comment
            return True
        return False

    @staticmethod
    def is_multiple(self, line, comment_identifier, next_line, previous_line):
        """
        Check if the line contains a multi line comment.

        Args:
            line: line to be checked.
            comment_identifier:  Type object with language specific comment
                                 information
            next_line: the line after the current line to be checked.
            previous_line: the line before the current line to be checked.

        Returns:
            bool: Flag for the check

        """
        if line != "" and comment_identifier.extension == ".py" and line.startswith(comment_identifier.multi_comment[0]) and next_line.startswith(comment_identifier.multi_comment[0]) and not previous_line.startswith(comment_identifier.multi_comment[0]):
            # beginning of a python code block
            self.block_comments += 1
            return True
        elif line != "" and comment_identifier.extension == ".py" and line.startswith(comment_identifier.multi_comment[0]) and (next_line.startswith(comment_identifier.multi_comment[0]) or previous_line.startswith(comment_identifier.multi_comment[0])):
            # middle or end of a python code block
            return True
        elif line != "" and comment_identifier.extension != ".py" and comment_identifier.multi_comment[0] in line:
            # beginning of a java and js code block
            self.block_comments += 1
            return True
        elif line != "" and comment_identifier.extension != ".py" and line.startswith("*"):
            # middle or end of a java or js code block
            return True
        elif line != "" and comment_identifier.extension != ".py" and comment_identifier.multi_comment[-1] in line:
            # in-line code block in java or js
            self.block_comments += 1
            return True

    @staticmethod
    def update_counts(self, line_type, lines):
        """
        Updates the Scan object counts for the final output.

        Args:
            line_type = dict to store the type of line for each line of the file
            lines = array of lines read from the file

        Returns:
            None

        """
        for key, val in line_type.items():
            if val == "s":
                # line is a single comment
                self.single_line_comments += 1
                if "TODO:" in lines[key-1]:
                    # line is a todo single comment
                    self.todo += 1
            elif val == "m":
                # line is a block comment
                self.multi_line_comments += 1
                if "TODO:" in lines[key-1]:
                    # line is a multi block comment todo
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
    # Extract the file extension from the path
    extension = os.path.splitext(file)[-1].lower()
    if (file.startswith(".") and not (file.startswith("./")
                                      or file.startswith(".\\"))) or (extension
                                                                      == ""):
        # File is not an acceptable program file
        raise TypeError("Invalid program file")
    else:
        comment_identifier = Type(extension)
        with open(file) as f:
            scan = Scan(f, comment_identifier)
            print("Total # of lines: {} \nTotal # of comment lines: {} \nTotal # of single line comments: {}\nTotal # of comment lines within block comments: {}\nTotal # of block line comments: {}\nTotal # of TODO's: {}".format(scan.lines,
                                                                                                                                                                                                                                     scan.single_line_comments +
                                                                                                                                                                                                                                     scan.multi_line_comments,
                                                                                                                                                                                                                                     scan.single_line_comments,
                                                                                                                                                                                                                                     scan.multi_line_comments,
                                                                                                                                                                                                                                     scan.block_comments,
                                                                                                                                                                                                                                     scan.todo))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", help='Program file to check', required=True)
    args = parser.parse_args()
    main(args.f)
