# It might be useful in the future. Not for now.
# import sys

# import click

# from iseq.gff import read as read_gff


# @click.command()
# @click.argument("gff_file", type=click.File("r"))
# def gff_dedup(gff_file):
#     """
#     Deduplicate a GFF_FILE file.

#     The deduplicated GFF_FILE will be written to the standard output.
#     """

#     gff = read_gff(gff_file)
#     gff.deduplicate()

#     gff.write_file(sys.stdout)
