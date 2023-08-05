import os
import gzip
from Bio import SeqIO
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import celescope
import pysam
from celescope.tools.utils import format_number, log, read_barcode_file


def sub_typing(index, fq_outdir):
    fq = f'{fq_outdir}/cell{index}/cell{index}.fq'
    outdir = f'{fq_outdir}/cell{index}/'
    cmd = (
        f'OptiTypePipeline.py '
        f'--input {fq} '
        f'--rna '
        f'--outdir {outdir} '
        f'>/dev/null 2>&1 '
    )
    os.system(cmd)


@log
def razer(fq, outdir, sample, thread):

    # get ref
    root_path = os.path.dirname(celescope.__file__)
    ref = f'{root_path}/data/HLA/hla_reference_rna.fasta'

    # mkdir
    out_bam_dir = f'{outdir}/bam/'
    if not os.path.exists(out_bam_dir):
        os.mkdir(out_bam_dir)

    # out_bam    
    out_bam = f'{outdir}/bam/{sample}.bam'

    # run
    cmd = (
        f'razers3 -i 97 -m 99999 --distance-range 0 -pa '
        f'-tc {thread} '
        f'-o {out_bam} '
        f'{ref} '
        f'{fq} '
    )
    razer.logger.info(cmd)
    os.system(cmd)
    return out_bam


@log
def split_bam(out_bam, outdir, barcodes):

    # init
    count_dict = defaultdict(dict)
    bam_dict = defaultdict(list)
    index_dict = defaultdict(dict)
    bam_outdir = f'{outdir}/cells/'

    # read bam and split
    samfile = pysam.AlignmentFile(out_bam, "rb")
    header = samfile.header
    for read in samfile:
        attr = read.query_name.split('_')
        barcode = attr[0]
        umi = attr[1]
        if barcode in barcodes:
            bam_dict[barcode].append(read)
            if umi in count_dict[barcode]:
                count_dict[barcode][umi] += 1
            else:
                count_dict[barcode][umi] = 1
    
    # write new bam
    index = 0
    for barcode in barcodes:
        # init
        index += 1
        index_dict[index]['barcode'] = barcode
        index_dict[index]['valid'] = False

        # out
        if barcode in bam_dict:
            cell_dir = f'{bam_outdir}/cell{index}'
            cell_bam_file = f'{cell_dir}/cell{index}.bam'
            if not os.path.exists(cell_dir):
                os.makedirs(cell_dir) 
            index_dict[index]['valid'] = True
            cell_bam = pysam.AlignmentFile(
                f'{cell_bam_file}', "wb", header=header)
            for read in bam_dict[barcode]:
                cell_bam.write(read)
            cell_bam.close()


@log
def hla_typing(fq_outdir, index_dict, thread):
    all_res = []
    valid_index_dict = {}
    for index in index_dict:
        if index_dict[index]['valid']:
            valid_index_dict[index] = index_dict[index]['barcode']

    args2 = [fq_outdir for index in valid_index_dict]
    with ProcessPoolExecutor(thread) as pool:
        for res in pool.map(sub_typing, valid_index_dict.keys(), args2):
            all_res.append(res)


@log
def mapping_hla(args):

    sample = args.sample
    outdir = args.outdir
    fq = args.fq
    thread = int(args.thread)
    match_dir = args.match_dir

    # process args
    barcodes, nCell = read_barcode_file(match_dir)

    # check dir
    if not os.path.exists(outdir):
        os.system('mkdir -p %s' % (outdir))

    # razer
    out_bam = razer(fq, outdir, sample, thread)

    # split bam

    '''
    # split fq
    fq_outdir = f'{outdir}/cells/'
    index_dict, read_dict = split_fq(fq, fq_outdir, barcodes)

    # typing
    hla_typing(fq_outdir, index_dict, thread)
    '''


def get_opts_mapping_hla(parser, sub_program):
    if sub_program:
        parser.add_argument('--outdir', help='output dir', required=True)
        parser.add_argument('--sample', help='sample name', required=True)
        parser.add_argument("--fq", required=True)
        parser.add_argument('--assay', help='assay', required=True)
    parser.add_argument("--match_dir", help="match scRNA-Seq dir", required=True)
    parser.add_argument("--thread", help='number of thread', default=1)