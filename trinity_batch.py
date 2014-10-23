#!/usr/bin/env python

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"
__version__ = "0.10 BOOTES" 
'''

Trinity Batch Script
Trinity --seqType fq --left fastq_1.fastq --right fastq_2.fastq --JM 96G --CPU 32 --full_cleanup -o output.Trinity.fasta;

'''

import argparse
import os
import sys
import subprocess


# Get a listing of all files in the input directory that match the file extension and return a unique set
# The set created does not include the _1.extension or _2.extension
def make_fileset(recurse, file_extension, input_dir):
	filelist = []
	if recurse:
		for dirname, dirnames, filenames in os.walk(input_dir):
			for filename in filenames:
				if filename.endswith(file_extension):
					# Append path+filename with no extension
					filelist.append(dirname+(os.path.splitext(filename)[0]).rsplit('_',1)[0]) # multiple underscores
	else:
		for filename in os.listdir(input_dir):
			if filename.endswith(file_extension):
				# Append filename with no extension
				filelist.append(input_dir+(os.path.splitext(filename)[0]).rsplit('_',1)[0])
	# Create a set to remove duplicates
	fileset = set(filelist)
	return fileset


def main():

	#Create the argument parser
	parser = argparse.ArgumentParser()
	
	# -i --input
	parser.add_argument("-i", "--input", dest="input_dir", help="The input directory to analyze", required=True)
	# -e --extension
	parser.add_argument("-e", "--ext", dest="extension_string", help="The file extension to match. File extensions must start with '.' to be valid!", required=True)
	# -o --output
	parser.add_argument("-o", "--output", dest="output_path", help="path to output folder", required=True)
	# -t --threads
	parser.add_argument("-t", "--threads", dest="processors", default='32', help="The number of processors to use. Default is 90 percent of available. i.e. This machine's DEFAULT = 32 " )
	# -r --recurse
	parser.add_argument("-r", "--recurse", action="store_true", dest="recurse", help="recurse through all directories")
	# -m --memory
	parser.add_argument("-m","--memory", dest="ram", default="96G", help="The amount of RAMs to use. Default: 96G")

	# Parse arguments
	args = parser.parse_args()

	# Set argument values
	input_dir = os.path.abspath(args.input_dir)+'/' # REQUIRED
	file_extension = args.extension_string # REQUIRED
	output_path = os.path.abspath(args.output_path)+'/' # REQUIRED
	processors = args.processors
	recurse = args.recurse
	ram = args.ram

	fileset = make_fileset(recurse, file_extension, input_dir)

	# Build command list
	command_list = []
	for filename in fileset:
		# Build filenames for read one and two
		read_1 = filename+'_1'+file_extension
		read_2 = filename+'_2'+file_extension
		command_string = "/media/nfs_opt/trinity/trinityrnaseq_r20140717/Trinity --seqType fq --left {} --right {} --JM {} --CPU {} --full_cleanup -o {}/{}.Trinity.fasta;".format(read_1, read_2, ram, processors, output_path.rstrip('/'), os.path.basename(filename))
		# Add command to the command list 
		command_list.append(command_string)

	# Queue the files
	for command in command_list:
		try:
			print "Running: {}".format(command_string)
			proc = subprocess.Popen(command, shell=True)
			proc.wait()
		except OSError:
			print "Something broke on command: {}".format(command_string)
			pass
			
if __name__ == '__main__':
	main()
 
