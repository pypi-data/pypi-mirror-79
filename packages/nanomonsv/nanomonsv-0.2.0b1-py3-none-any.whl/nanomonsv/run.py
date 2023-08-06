#! /usr/bin/env python

import os, subprocess, shutil
from .parse import *
from .filt import *
from .identify import *
from .long_read_validate import *
from .insert_classify import *
from .utils import *

from .logger import get_logger
logger = get_logger(__name__)

def parse_main(args):

    # check if the executables exist
    is_tool("tabix")
    is_tool("bgzip")

    # check input file existences
    is_exists_bam(args.bam_file)

    # BAM format check
    bam_format_check(args.bam_file)

    # make directory for the output prefix
    output_dir = os.path.dirname(args.output_prefix)
    if output_dir != '' and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ####################
    parse_alignment_info(args.bam_file, args.output_prefix + ".tmp.deletion_info.txt", 
                                        args.output_prefix + ".tmp.insertion_info.txt", 
                                        args.output_prefix + ".tmp.rearrangement_info.txt")

    ####################
    # deletion processing
    hout = open(args.output_prefix + ".tmp.deletion.sorted.bed", 'w')
    subprocess.check_call(["sort", "-k1,1", "-k2,2n", "-k3,3n", args.output_prefix + ".tmp.deletion_info.txt"], stdout = hout)
    hout.close()

    hout = open(args.output_prefix + ".deletion.sorted.bed.gz", 'w')
    subprocess.check_call(["bgzip", "-f", "-c", args.output_prefix + ".tmp.deletion.sorted.bed"], stdout = hout)
    hout.close()

    subprocess.check_call(["tabix", "-p", "bed", args.output_prefix + ".deletion.sorted.bed.gz"])
    ####################

    ####################
    # insertion processing
    hout = open(args.output_prefix + ".tmp.insertion.sorted.bed", 'w')
    subprocess.check_call(["sort", "-k1,1", "-k2,2n", "-k3,3n", args.output_prefix + ".tmp.insertion_info.txt"], stdout = hout)
    hout.close()
    
    hout = open(args.output_prefix + ".insertion.sorted.bed.gz", 'w') 
    subprocess.check_call(["bgzip", "-f", "-c", args.output_prefix + ".tmp.insertion.sorted.bed"], stdout = hout)
    hout.close()
     
    subprocess.check_call(["tabix", "-p", "bed", args.output_prefix + ".insertion.sorted.bed.gz"])
    ####################

    ####################
    # rearrangement processing
    hout = open(args.output_prefix + ".tmp.rearrangement_info.name_sorted.txt", 'w')
    subprocess.check_call(["sort", "-k1,1", "-k2,2n", args.output_prefix + ".tmp.rearrangement_info.txt"], stdout = hout)
    hout.close()

    extract_bedpe_junction(args.output_prefix + ".tmp.rearrangement_info.name_sorted.txt", 
                           args.output_prefix + ".tmp.rearrangement.bedpe") # ,
                           # args.split_alignment_check_margin, args.minimum_breakpoint_ambiguity)

    hout = open(args.output_prefix + ".tmp.rearrangement.sorted.bedpe", 'w')
    subprocess.check_call(["sort", "-k1,1", "-k2,2n", "-k3,3n", "-k4,4", "-k5,5n", "-k6,6n", 
                           args.output_prefix + ".tmp.rearrangement.bedpe"], stdout = hout)
    hout.close()
  
    hout = open(args.output_prefix + ".rearrangement.sorted.bedpe.gz", 'w')
    subprocess.check_call(["bgzip", "-f", "-c", args.output_prefix + ".tmp.rearrangement.sorted.bedpe"], stdout = hout)
    hout.close()

    subprocess.check_call(["tabix", "-p", "bed", args.output_prefix + ".rearrangement.sorted.bedpe.gz"])
    ####################

    if not args.debug:
        subprocess.check_call(["rm", "-rf", args.output_prefix + ".tmp.deletion_info.txt"])
        subprocess.check_call(["rm", "-rf", args.output_prefix + ".tmp.deletion.sorted.bed"])
        subprocess.check_call(["rm", "-rf", args.output_prefix + ".tmp.insertion_info.txt"])
        subprocess.check_call(["rm", "-rf", args.output_prefix + ".tmp.insertion.sorted.bed"])
        subprocess.check_call(["rm", "-rf", args.output_prefix + ".tmp.rearrangement_info.txt"])
        subprocess.check_call(["rm", "-rf", args.output_prefix + ".tmp.rearrangement_info.name_sorted.txt"])
        subprocess.check_call(["rm", "-rf", args.output_prefix + ".tmp.rearrangement.bedpe"])
        subprocess.check_call(["rm", "-rf", args.output_prefix + ".tmp.rearrangement.sorted.bedpe"])


def get_main(args):

    # check if the executables exist
    is_tool("mafft")
    if args.use_ssw_lib: libssw_check()

    # check existences
    is_exists_bam(args.tumor_bam)
    is_exists(args.reference_fasta)
    if args.control_bam is not None: is_exists_bam(args.control_bam)
   
    # check parsed files existences
    is_exists_parsed_files(args.tumor_prefix)
    if args.control_prefix is not None: is_exists_parsed_files(args.control_prefix)
 
    # BAM format check
    bam_format_check(args.tumor_bam)
    fasta_format_check(args.reference_fasta)
    if args.control_bam is not None: bam_format_check(args.control_bam)

    control_rearrangement_bedpe = None
    control_deletion_bed = None
    control_insertion_bed = None
    if args.control_prefix is not None: 
        control_rearrangement_bedpe = args.control_prefix + ".rearrangement.sorted.bedpe.gz"
        control_deletion_bed = args.control_prefix + ".deletion.sorted.bed.gz"
        control_insertion_bed = args.control_prefix + ".insertion.sorted.bed.gz"
    
    ####################
    cluster_rearrangement(args.tumor_prefix + ".rearrangement.sorted.bedpe.gz", args.tumor_prefix + ".rearrangement.sorted.clustered.bedpe",
                     args.cluster_margin_size)

    filt_clustered_rearrangement1(args.tumor_prefix + ".rearrangement.sorted.clustered.bedpe", args.tumor_prefix + ".rearrangement.sorted.clustered.filt1.bedpe",
                             args.min_tumor_variant_read_num, args.median_mapQ_thres, args.max_overhang_size_thres)

    filt_clustered_rearrangement2(args.tumor_prefix + ".rearrangement.sorted.clustered.filt1.bedpe", args.tumor_prefix + ".rearrangement.sorted.clustered.filt2.bedpe", 
                                  control_rearrangement_bedpe)


    cluster_insertion_deletion(args.tumor_prefix + ".deletion.sorted.bed.gz", args.tumor_prefix + ".deletion.sorted.clustered.bedpe")

    filt_clustered_insertion_deletion1(args.tumor_prefix + ".deletion.sorted.clustered.bedpe", args.tumor_prefix + ".deletion.sorted.clustered.filt1.bedpe",
                                       args.min_tumor_variant_read_num, args.median_mapQ_thres, args.max_overhang_size_thres)

    filt_clustered_insertion_deletion2(args.tumor_prefix + ".deletion.sorted.clustered.filt1.bedpe", args.tumor_prefix + ".deletion.sorted.clustered.filt2.bedpe",
                                       control_deletion_bed)

    cluster_insertion_deletion(args.tumor_prefix + ".insertion.sorted.bed.gz", args.tumor_prefix + ".insertion.sorted.clustered.bedpe")

    filt_clustered_insertion_deletion1(args.tumor_prefix + ".insertion.sorted.clustered.bedpe", args.tumor_prefix + ".insertion.sorted.clustered.filt1.bedpe",
                                       args.min_tumor_variant_read_num, args.median_mapQ_thres, args.max_overhang_size_thres)

    filt_clustered_insertion_deletion2(args.tumor_prefix + ".insertion.sorted.clustered.filt1.bedpe", args.tumor_prefix + ".insertion.sorted.clustered.filt2.bedpe",
                                       control_insertion_bed)

    identify(args.tumor_prefix + ".rearrangement.sorted.clustered.filt2.bedpe", 
             args.tumor_prefix + ".insertion.sorted.clustered.filt2.bedpe",
             args.tumor_prefix + ".deletion.sorted.clustered.filt2.bedpe",
             args.tumor_prefix + ".refined_bp.txt", args.tumor_bam, args.reference_fasta, args.debug)

    long_read_validate_main(args.tumor_prefix + ".refined_bp.txt",
                  args.tumor_bam,
                  args.tumor_prefix + ".refined_bp.validated.txt",
                  args.tumor_prefix + ".validated.tumor_sread.txt",
                  args.reference_fasta, 
                  args.control_bam, args.var_read_min_mapq, args.use_ssw_lib, args.debug)

    is_control = True if args.control_bam is not None else False

    filt_final(args.tumor_prefix + ".refined_bp.validated.txt",
               args.tumor_prefix + ".validated.tumor_sread.txt",
               args.tumor_prefix + ".nanomonsv.result.txt",
               args.tumor_prefix + ".nanomonsv.supporting_read.txt",
               args.min_tumor_variant_read_num, args.min_tumor_VAF, args.max_control_variant_read_num, args.max_control_VAF, False, is_control)

    if not args.debug:
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".rearrangement.sorted.clustered.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".rearrangement.sorted.clustered.filt1.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".rearrangement.sorted.clustered.filt2.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".deletion.sorted.clustered.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".deletion.sorted.clustered.filt1.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".deletion.sorted.clustered.filt2.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".insertion.sorted.clustered.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".insertion.sorted.clustered.filt1.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".insertion.sorted.clustered.filt2.bedpe"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".refined_bp.txt"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".refined_bp.validated.txt"])
        subprocess.check_call(["rm", "-rf", args.tumor_prefix + ".validated.tumor_sread.txt"])


def validate_main(args):
    
    # executable check
    if args.use_ssw_lib: libssw_check()

    ####################
    long_read_validate_main(args.sv_list_file,
                            args.tumor_bam,
                            args.output + ".validated.txt",
                            args.output + ".validated.tumor_sread.txt",
                            args.reference_fasta,
                            args.control_bam, 
                            args.var_read_min_mapq,
                            args.use_ssw_lib, args.debug)

    is_control = True if args.control_bam is not None else False

    filt_final(args.output + ".validated.txt",
               args.output + ".validated.tumor_sread.txt",
               args.output, 
               args.output + ".supporting_read.txt",
               0, 0, float("inf"), float("inf"), True, is_control)

    if not args.debug:
        subprocess.check_call(["rm", "-rf", args.output + ".validated.txt"])
        subprocess.check_call(["rm", "-rf", args.output + ".validated.tumor_sread.txt"])


def insert_classify_main(args):

    import tempfile
    import annot_utils.exon

    # check if the executables exist
    is_tool("minimap2")
    is_tool("bedtools")
    is_tool("bwa")
    is_tool("RepeatMasker")

    make_fasta_file(args.sv_list_file, args.output_file + ".tmp.fasta", args.output_file + ".tmp.seq_id.txt")
    
    ##########
    # processed pseudo gene
    annot_utils.exon.make_exon_info(args.output_file + ".tmp.exon.bed.gz", "gencode", args.genome_id, args.grc, True)

    with open(args.output_file + ".tmp.minimap2.sam", 'w') as hout:
        subprocess.check_call(["minimap2", "-ax", "splice", args.reference_fasta, args.output_file + ".tmp.fasta"], stdout = hout)

    sam2bed_split(args.output_file + ".tmp.minimap2.sam", args.output_file + ".tmp.minimap2.filt.bed")
    
    with open(args.output_file + ".tmp.minimap2.filt.exon.bed", 'w') as hout:
        subprocess.check_call(["bedtools", "intersect", "-a", args.output_file + ".tmp.minimap2.filt.bed", 
                               "-b", args.output_file + ".tmp.exon.bed.gz", "-wo"], stdout = hout)
 
    pp_proc_filt_exon(args.output_file + ".tmp.minimap2.filt.exon.bed", 
                      args.output_file + ".tmp.seq_id.txt", 
                      args.output_file + ".tmp.ppseudo.txt")
    ##########

    ##########
    # repeat masker
    output_dir = os.path.dirname(args.output_file)
    tmpdir_rmsk = tempfile.mkdtemp()
    # tmpdir_rmsk = "tmp"
    subprocess.check_call(["RepeatMasker", "-species", "human", args.output_file + ".tmp.fasta", "-dir", tmpdir_rmsk])

    summarize_rmsk(tmpdir_rmsk + '/' + os.path.basename(args.output_file + ".tmp.fasta") + ".out", args.output_file + ".tmp.rmsk.txt")

    check_tsd_polyAT(args.output_file + ".tmp.fasta", args.output_file + ".tmp.seq_id.txt", 
                     args.reference_fasta, args.output_file + ".tmp.tsd.polyAT.txt")

    shutil.rmtree(tmpdir_rmsk)
    ##########
    
    ##########
    # alignment to reference genome
    with open(args.output_file + ".tmp.bwa.sam", 'w') as hout:
        print(' '.join(["bwa", "mem", "-h", "200", args.reference_fasta, args.output_file + ".tmp.fasta"]))
        subprocess.check_call(["bwa", "mem", "-h", "200", args.reference_fasta, args.output_file + ".tmp.fasta"], stdout = hout)

    summarize_bwa_alignment2(args.output_file + ".tmp.bwa.sam", args.output_file + ".tmp.seq_id.txt", args.output_file + ".tmp.alignment.txt")

    organize_info(args.output_file + ".tmp.rmsk.txt", args.output_file + ".tmp.alignment.txt", 
                 args.output_file + ".tmp.tsd.polyAT.txt", args.output_file + ".tmp.seq_id.txt", 
                 args.output_file + ".tmp.org.txt", args.genome_id)

    annotate_sv_file(args.sv_list_file, args.output_file + ".tmp.org.txt", args.output_file + ".tmp.ppseudo.txt",
                     args.output_file + ".tmp.seq_id.txt", args.output_file)

    if not args.debug:
        os.remove(args.output_file + ".tmp.fasta")
        os.remove(args.output_file + ".tmp.seq_id.txt")
        os.remove(args.output_file + ".tmp.bwa.sam")
        os.remove(args.output_file + ".tmp.exon.bed.gz")
        os.remove(args.output_file + ".tmp.exon.bed.gz.tbi")
        os.remove(args.output_file + ".tmp.minimap2.filt.bed")
        os.remove(args.output_file + ".tmp.minimap2.filt.exon.bed")
        os.remove(args.output_file + ".tmp.ppseudo.txt")
        os.remove(args.output_file + ".tmp.rmsk.txt")
        os.remove(args.output_file + ".tmp.tsd.polyAT.txt")
        os.remove(args.output_file + ".tmp.minimap2.sam")
        os.remove(args.output_file + ".tmp.alignment.txt")
        os.remove(args.output_file + ".tmp.org.txt")


