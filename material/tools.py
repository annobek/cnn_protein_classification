"""
Some essential and useful functions for the algorithm behind prot-fin
"""

from typing import List, Dict, Tuple, Set, Generator, TextIO, _GenericAlias, _UnionGenericAlias, Callable, Any, Type
from tqdm import tqdm
import re

ProteinID = str


class Fasta:
    """
    A class used for convenient iteration over a FASTA file's contents.

    ...

    Attributes
    ----------
    file_name : str
        The name of the FASTA formatted file
    protein_count : int
        The number of sequences stored in the FASTA file
    """
    def __init__(self, file_name: str, check=True):
        """
        Parameters
        ----------
        file_name : str
            The name of the FASTA formatted file
        """
        with open(file_name) as f:
            self.file_name = file_name
            if check:
                self.protein_count = count_appearances_in_file("^>", f)

                # validate ... TODO or validate during iteration like (re.match("^[A-Z]+$", seq) is not None)

            else:
                self.protein_count = None

    def __len__(self):
        if self.protein_count is None:
            raise TypeError("Can't predict protein count of unchecked Fasta")
        return self.protein_count

    def __iter__(self) -> Generator[Tuple[ProteinID, str, str], None, None]:
        return self[:]

    def __getitem__(self, key) -> Generator[Tuple[ProteinID, str, str], None, None]:
        assert type(key) is slice
        if self.protein_count is None:
            start, _, step = key.indices(0)
            stop = key.stop

            def open_range(start, step=1):
                while True:
                    yield start
                    start += step

            pbar = tqdm(open_range(start, step))
        else:
            start, stop, step = key.indices(self.protein_count)
            pbar = tqdm(range(start, stop, step))
        assert step > 0, "negative steps currently not supported"

        with open(self.file_name) as f:
            # create a progress bar and iterate over the FASTA file
            current_prot = 0
            for i in pbar:

                # find line of sequence description
                while current_prot <= i and (prot_desc := f.readline()):
                    current_prot += prot_desc[0] == ">"
                if not prot_desc:
                    break  # because EOF

                # read sequence
                seq = ""
                while (seq_segment := f.readline()) and seq_segment[0] != ">":
                    pointer = f.tell()
                    seq += seq_segment
                seq = seq.replace("\n", "")

                # go to last line -> readline returns header of next protein
                f.seek(pointer)

                # extract information from describing line
                header = prot_desc.split(" ", 1)
                if len(header) == 2:
                    prot_id, description = header
                else:
                    prot_id, description = header[0][:-1], "\n"

                # yield the extracted values, remove '>' from identifier and
                # '\n' from description
                yield Protein((prot_id[1:], description[:-1], seq))

        if stop is not None:
            assert current_prot == max(start, stop - (stop - start - 1) % step)


class Protein(tuple):
    def header(self) -> str:
        return f">{self[0].upper()}"

    def __str__(self):
        return self.header() + "\n%s\n" % self[-1].replace("*", "")


def count_appearances_in_file(pattern, file: TextIO):
    count = 0
    file.seek(0)
    while (buffer := file.read(1024 ** 2)):
        count += len(re.findall(pattern, buffer, re.MULTILINE))
    file.seek(0)

    return count
