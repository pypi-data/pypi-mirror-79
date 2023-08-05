import unittest
import os
from celescope.hla.mapping_hla import split_bam
from celescope.tools.utils import read_barcode_file


class testHLA(unittest.TestCase):
    def setUp(self):
        os.chdir('/SGRNJ01/RD_dir/pipeline_test/zhouyiqi/HLA/sjm_0903')
        self.sample = 'pT_HLA_0812'
        self.out_bam = './/pT_HLA_0812/03.mapping_hla/bam/pT_HLA_0812.bam'
        self.match_dir = '/SGRNJ02/RandD4/RD2019016/20200804/PBMC_pTLib/'
        self.barcodes, _ncell = read_barcode_file(self.match_dir)

    def test_split_bam(self):
        outdir = f'{self.sample}/03.mapping_hla/'
        split_bam(self.out_bam, outdir, self.barcodes)


if __name__ == '__main__':
    unittest.main()
