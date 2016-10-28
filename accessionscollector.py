#!/usr/bin/env python3


"""
Author: Elina Wever
Date: 22-09-2016
Purpose: Collecting and storing all available accession id´s for every micro-organism in a single list
Version: 0.0.1
"""
import os
import glob


class CollectAccessionIds:
    """This class reads different .ids plus .txt files and extracts plus returns a list of all accession id's """

    def __init__(self):
        """"Constructor for CollectAccessionIds class"""
        self.accession_list = []      # Create list to store all accessions
        self.path_separator = os.sep  # Get system specific path separator
        self.pathway = "//172.16.6.53{0}StageStorage{0}voorbeelddata{0}ncbi_genomes{0}".format(self.path_separator)
        self.file_list = []           # Create list to store file names
        self.accession_list = []

    def collect_ids(self):
        """ This method reads multiple files and extracts all accession id's
            Input: .ids/.txt files
            Output: A list of all accession id's
        """
        to_be_filtered_list = []
        file_types = ("*.ids", "*.txt")  # Define to be read extensions
        txt_files_list = []
        ids_files_list = []

        for files in file_types:
            self.file_list.extend(glob.glob(self.pathway + files))  # Create list with files with different extensions

        for names in self.file_list:

            with open(names,
                      encoding="utf-8") as complete_files:  # Type utf-8 is needed to prevent an error during opening
                filename = str(complete_files.name)  # Get complete file names
                if filename.endswith(".txt"):
                    for lines in complete_files:
                        if lines.__contains__("Complete Genome"):
                            accessions_version = lines.split("\t")[9]  # Extract accessions from file
                            remove_sign = accessions_version.replace("-", "")  # Remove - sign to avoid Bad Request error
                            accessions = remove_sign.split(".", 1)[0]  # Remove version number
                            accessions = accessions.split(",")  # Adapt accessions

                            to_be_filtered_list.append(accessions)  # Add all accessions to list
                            txt_files_list = [i for sublist in to_be_filtered_list for i in sublist]  # Flatten list

                else:
                    for lines in complete_files:
                        if lines.__contains__("eukaryota"):  # Skip header
                            continue
                        else:
                            accessions = lines.split("\t")[4]  # Extract accession id's
                            accessions = accessions.replace("-", "")  # Remove - sign to avoid Bad Request error
                            ids_files_list.append(accessions)  # Save accessions in a list

        self.accession_list = txt_files_list + ids_files_list  # Merge output from different files
        return self.accession_list
