# DataCollector

This README describes the usage and purpose of different written modules.

This package contains different .py files with different functions. These are:
 * ncbi_datacollector
 * keggdatacollector
 * accessionscollector
 
 ## NCBI Data Collector
 
 The ncbi_datacollector module retrieves all complete genomes of every single micro-organism. It's input is a set of accesion id's which 
 are generated by the accessionscollector.py .
 
 * How do I set up ?
   The only installation needed to succesfully run this program is Biopython(1.68) and Python(3.5).
   
 ## KEGG Data Collector
 
 The keggdatacollector module retrieves all available pathway files of each organism based on a single entry code. An example of an 
 entry code is "pan". These entry codes are extracted from a file downloaded of the following link: http://rest.kegg.jp/list/organism
 
 * How do I set up ? 
   Installation of Python(3.5) only is enough to run this program
   
 ## Accessions Collector
 
 The accessionscollector collects all accession id's of different NCBI files and puts them in a single list. This list is used by the
 ncbi_datacollector module to retrieve genbankfiles from NCBI.
 
 