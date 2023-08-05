import logging
import os
import glob
import sys
import re
import gzip
import pandas as pd
import numpy as np
import subprocess
from collections import defaultdict
import celescope.tools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

tools_dir = os.path.dirname(celescope.tools.__file__)
logger1 = logging.getLogger(__name__)


def process_read(read2_file, pattern_dict, barcode_dict, linker_dict):
    # if valid, return (True)
    metrics = defaultdict(int)
    res_dict = genDict(dim=3)
    read2 = gzip.open(read2_file, "rt")
    while True:
        line1 = read2.readline()
        line2 = read2.readline()
        line3 = read2.readline()
        line4 = read2.readline()
        if not line4:
            break
        metrics['Total Reads'] += 1
        attr = str(line1).strip("@").split("_")
        barcode = str(attr[0])
        umi = str(attr[1])
        seq = line2.strip()
        if linker_dict:
            try:
                seq_linker = ''.join(seq_range(seq, pattern_dict['L']))
            except:
                metrics['Reads Unmapped too Short'] += 1
                continue
        if barcode_dict:
            try:
                seq_barcode = ''.join(seq_range(seq, pattern_dict['C']))
            except:
                metrics['Reads Unmapped too Short'] += 1
                continue
        
        # check linker
        valid_linker = False
        for linker_name in linker_dict:
            if hamming_correct(linker_dict[linker_name], seq_linker):
                valid_linker = True
                continue
        
        if not valid_linker:
            metrics['Reads Unmapped Invalid Linker'] += 1
            continue

        # check barcode
        valid_barcode = False
        for barcode_name in barcode_dict:
            if hamming_correct(barcode_dict[barcode_name], seq_barcode):
                res_dict[barcode][barcode_name][umi] += 1
                valid_barcode = True
                continue

        if not valid_barcode:
            metrics['Reads Unmapped Invalid Barcode'] += 1
            continue

        # mapped
        metrics['Reads Mapped'] += 1
        if metrics['Reads Mapped'] % 1000000 == 0:
            logger1.info(str(metrics['Reads Mapped']) + " reads done.")
        
    return res_dict, metrics


def seq_range(seq, pattern_dict):
    # get subseq with intervals in arr and concatenate
    length = len(seq)
    for x in pattern_dict:
        if length < x[1]:
            raise Exception(f'invalid seq range {x[0]}:{x[1]} in read')
    return ''.join([seq[x[0]:x[1]]for x in pattern_dict])


def read_one_col(file):
    df = pd.read_csv(file, header=None)
    col1 = list(df.iloc[:, 0])
    num = len(col1)
    return col1, num


def read_fasta(fasta_file, equal=False):
    # seq must have equal length
    dict = {}
    LENGTH = 0
    with open(fasta_file, "rt") as f:
        while True:
            line1 = f.readline()
            line2 = f.readline()
            if not line2:
                break
            name = line1.strip(">").strip()
            seq = line2.strip()
            seq_length = len(seq)
            if equal:
                if LENGTH == 0:
                    LENGTH = seq_length
                else:
                    if LENGTH != seq_length:
                        raise Exception(f"{fasta_file} have different seq length")
            dict[name] = seq
    if equal:
        return dict, LENGTH
    return dict


def hamming_correct(string1, string2):
    threshold = len(string1) / 10 + 1
    if hamming_distance(string1, string2) < threshold:
        return True
    return False


def hamming_distance(string1, string2):
    distance = 0
    length = len(string1)
    length2 = len(string2)
    if (length != length2):
        raise Exception("string1 and string2 do not have same length")
    for i in range(length):
        if string1[i] != string2[i]:
            distance += 1
    return distance


def gen_stat(df, stat_file):
    # 3cols: item count total_count
    df['percent'] = df["count"] / df['total_count']
    df['value'] = df.apply(
        lambda x: f"{x['count']}({round(x['percent'] * 100, 2)}%)",
        axis=1)
    df = df.loc[:, ["item", "value"]]
    df.to_csv(stat_file, sep=":", header=None, index=False)


def get_fq(library_id, library_path):
    try:
        pattern1_1 = library_path + '/' + library_id + '*' + '_1.fq.gz'
        pattern1_2 = f'{library_path}/*{library_id}*R1.fastq.gz'
        pattern2_1 = library_path + '/' + library_id + '*' + '_2.fq.gz'
        pattern2_2 = f'{library_path}/*{library_id}*R2.fastq.gz'
        fq1 = ",".join(glob.glob(pattern1_1) + glob.glob(pattern1_2))
        fq2 = ",".join(glob.glob(pattern2_1) + glob.glob(pattern2_2))
    except IndexError as e:
        sys.exit("Mapfile Error:" + str(e))
    return fq1, fq2


def parse_map_col4(mapfile, default_val):
    fq_dict = defaultdict(list)
    col4_dict = defaultdict(list)
    with open(mapfile) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            tmp = line.split()
            library_id = tmp[0]
            library_path = tmp[1]
            sample_name = tmp[2]
            if len(tmp) == 4:
                col4 = tmp[3]
            else:
                col4 = default_val
            fq1, fq2 = get_fq(library_id, library_path)

            if sample_name in fq_dict:
                fq_dict[sample_name][0].append(fq1)
                fq_dict[sample_name][1].append(fq2)
            else:
                fq_dict[sample_name] = [[fq1], [fq2]]
            col4_dict[sample_name] = col4

    for sample_name in fq_dict:
        fq_dict[sample_name][0] = ",".join(fq_dict[sample_name][0])
        fq_dict[sample_name][1] = ",".join(fq_dict[sample_name][1])

    return fq_dict, col4_dict


def generate_sjm(cmd, name, conda, m=1, x=1):
    res_cmd = f'''
job_begin
    name {name}
    sched_options -w n -cwd -V -l vf={m}g,p={x}
    cmd source activate {conda}; {cmd}
job_end
'''

    return res_cmd


def merge_report(fq_dict, steps, last_step, sjm_cmd,
                 sjm_order, logdir, conda, outdir, rm_files):
    step = "merge_report"
    steps_str = ",".join(steps)
    samples = ','.join(fq_dict.keys())
    app = tools_dir + '/merge_table.py'
    cmd = (
        f'python {app} --samples {samples} '
        f'--steps {steps_str} --outdir {outdir}'
    )
    if rm_files:
        cmd += ' --rm_files'
    sjm_cmd += generate_sjm(cmd, 'merge_report', conda)
    for sample in fq_dict:
        sjm_order += f'order {step} after {last_step}_{sample}\n'
    with open(logdir + '/sjm.job', 'w') as fh:
        fh.write(sjm_cmd + '\n')
        fh.write(sjm_order)


def format_number(number: int) -> str:
    return format(number, ",")


def glob_genomeDir(genomeDir, logger1):
    refFlat = glob.glob(genomeDir + "/*.refFlat")
    if (len(refFlat) > 1):
        sys.exit("ERROR: Multiple refFlat file in " + genomeDir)
    elif (len(refFlat) == 0):
        sys.exit("ERROR: refFlat file not found in " + genomeDir)
    else:
        refFlat = refFlat[0]
        logger1.info("refFlat file found: " + refFlat)

    gtf = glob.glob(genomeDir + "/*.gtf")
    if (len(gtf) == 0):
        sys.exit("ERROR: gtf file not found in " + genomeDir)
    elif (len(gtf) > 1):
        gtf = glob.glob(genomeDir + "/*.chr.gtf")
        if (len(gtf) > 1):
            sys.exit("ERROR: Multiple gtf file in " + genomeDir)
        else:
            gtf = gtf[0]
            logger1.info("chr gtf file found: " + gtf)
    else:
        gtf = gtf[0]
        logger1.info("gtf file found: " + gtf)

    return refFlat, gtf


def barcode_filter_with_magnitude(
        df, plot='magnitude.pdf', col='UMI', percent=0.1, expected_cell_num=3000):
    # col can be readcount or UMI
    # determine validated barcodes
    df = df.sort_values(col, ascending=False)
    idx = int(expected_cell_num * 0.01) - 1
    idx = max(0, idx)

    # calculate read counts threshold
    threshold = int(df.iloc[idx, df.columns == col] * 0.1)
    threshold = max(1, threshold)
    validated_barcodes = df[df[col] > threshold].index

    fig = plt.figure()
    plt.plot(df[col])
    plt.hlines(threshold, 0, len(validated_barcodes), linestyle='dashed')
    plt.vlines(len(validated_barcodes), 0, threshold, linestyle='dashed')
    plt.title('expected cell num: %s\n%s threshold: %s\ncell num: %s' %
              (expected_cell_num, col, threshold, len(validated_barcodes)))
    plt.loglog()
    plt.savefig(plot)

    return (validated_barcodes, threshold, len(validated_barcodes))


def barcode_filter_with_kde(df, plot='kde.pdf', col='UMI'):
    # col can be readcount or UMI
    # filter low values
    df = df.sort_values(col, ascending=False)
    arr = np.log10([i for i in df[col] if i / float(df[col][0]) > 0.001])

    # kde
    x_grid = np.linspace(min(arr), max(arr), 10000)
    density = gaussian_kde(arr, bw_method=0.1)
    y = density(x_grid)

    local_mins = argrelextrema(y, np.less)
    log_threshold = x_grid[local_mins[-1][0]]
    threshold = np.power(10, log_threshold)
    validated_barcodes = df[df[col] > threshold].index

    # plot
    fig, (ax1, ax2) = plt.subplots(2, figsize=(6.4, 10))
    ax1.plot(x_grid, y)
    #ax1.axhline(y[local_mins[-1][0]], -0.5, log_threshold, linestyle='dashed')
    ax1.vlines(log_threshold, 0, y[local_mins[-1][0]], linestyle='dashed')
    ax1.set_ylim(0, 0.3)

    ax2.plot(df[col])
    ax2.hlines(threshold, 0, len(validated_barcodes), linestyle='dashed')
    ax2.vlines(len(validated_barcodes), 0, threshold, linestyle='dashed')
    ax2.set_title('%s threshold: %s\ncell num: %s' %
                  (col, int(threshold), len(validated_barcodes)))
    ax2.loglog()
    plt.savefig(plot)

    return (validated_barcodes, threshold, len(validated_barcodes))


def get_slope(x, y, window=200, step=10):
    assert len(x) == len(y)
    start = 0
    last = len(x)
    res = [[], []]
    while True:
        end = start + window
        if end > last:
            break
        z = np.polyfit(x[start:end], y[start:end], 1)
        res[0].append(x[start])
        res[1].append(z[0])
        start += step
    return res


def barcode_filter_with_derivative(
        df, plot='derivative.pdf', col='UMI', window=500, step=5):
    # col can be readcount or UMI
    # filter low values
    df = df.sort_values(col, ascending=False)
    y = np.log10([i for i in df[col] if i / float(df[col][0]) > 0.001])
    x = np.log10(np.arange(len(y)) + 1)

    # derivative
    res = get_slope(x, y, window=window, step=step)
    res2 = get_slope(res[0], res[1], window=window, step=step)
    g0 = [res2[0][i] for i, j in enumerate(res2[1]) if j > 0]
    cell_num = int(np.power(10, g0[0]))
    threshold = df[col][cell_num]
    validated_barcodes = df.index[0:cell_num]

    # plot
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(6.4, 15))
    ax1.plot(res[0], res[1])

    ax2.plot(res2[0], res2[1])
    ax2.set_ylim(-1, 1)

    ax3.plot(df[col])
    ax3.hlines(threshold, 0, len(validated_barcodes), linestyle='dashed')
    ax3.vlines(len(validated_barcodes), 0, threshold, linestyle='dashed')
    ax3.set_title('%s threshold: %s\ncell num: %s' %
                  (col, int(threshold), len(validated_barcodes)))
    ax3.loglog()
    plt.savefig(plot)

    return (validated_barcodes, threshold, len(validated_barcodes))


def genDict(dim=3):
    if dim == 1:
        return defaultdict(int)
    else:
        return defaultdict(lambda: genDict(dim - 1))


def downsample(bam, barcodes, percent):
    """
    calculate median_geneNum and saturation based on a given percent of reads

    Args:
        bam - bam file
        barcodes(set) - validated barcodes
        percent(float) - percent of reads in bam file.

    Returns:
        percent(float) - input percent
        median_geneNum(int) - median gene number
        saturation(float) - sequencing saturation

    Description:
        Sequencing Saturation = 1 - n_deduped_reads / n_reads.
        n_deduped_reads = Number of unique (valid cell-barcode, valid UMI, gene) combinations among confidently mapped reads.
        n_reads = Total number of confidently mapped, valid cell-barcode, valid UMI reads.
    """
    logging.info('working' + str(percent))
    cmd = ['samtools', 'view', '-s', str(percent), bam]
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    # nesting defaultdicts in an arbitrary depth
    readDict = genDict()

    n_reads = 0
    while True:
        line = p1.stdout.readline()
        if not line.strip():
            break
        tmp = line.strip().split()
        if tmp[-1].startswith('XT:Z:'):
            geneID = tmp[-1].replace('XT:Z:', '')
            cell_barcode, umi = tmp[0].split('_')[0:2]
            # filter invalid barcode
            if cell_barcode in barcodes:
                n_reads += 1
                readDict[cell_barcode][umi][geneID] += 1
    p1.stdout.close()

    geneNum_list = []
    n_deduped_reads = 0
    for cell_barcode in readDict:
        genes = set()
        for umi in readDict[cell_barcode]:
            for geneID in readDict[cell_barcode][umi]:
                genes.add(geneID)
                if readDict[cell_barcode][umi][geneID] == 1:
                    n_deduped_reads += 1
        geneNum_list.append(len(genes))

    median_geneNum = np.median(geneNum_list) if geneNum_list else 0
    saturation = (1 - float(n_deduped_reads) / n_reads) * 100

    return "%.2f\t%.2f\t%.2f\n" % (
        percent, median_geneNum, saturation), saturation


if __name__ == '__main__':

    df = pd.read_table('SRR6954578_counts.txt', header=0)
    barcode_filter_with_magnitude(df)
    barcode_filter_with_kde(df)
    barcode_filter_with_derivative(df)
