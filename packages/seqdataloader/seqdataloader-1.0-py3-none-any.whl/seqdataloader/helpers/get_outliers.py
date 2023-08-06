import pandas as pd
import pyBigWig
import numpy as np
import argparse

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--bed_regions_to_upsample")
    parser.add_argument("--label_bigwig") 
    parser.add_argument("--max_quantile",type=int,help="value between 1 and 100")
    parser.add_argument("--outf")
    return parser.parse_args()

def main():
    args=parse_args()
    get_outliers(args)
def get_outliers(args):
    peaks=pd.read_csv(args.bed_regions_to_upsample,header=None,sep='\t')
    bigwig=pyBigWig.open(args.label_bigwig)
    total=peaks.shape[0]
    chroms=[]
    region_start=[]
    region_end=[]
    counts=[] 
    for index,row in peaks.iterrows():
        if index%1000==0:
            print(str(index)+'/'+str(total)) 
        chrom=row[0]
        start=row[1]
        end=row[2]
        cur_counts=np.sum(np.nan_to_num(bigwig.values(chrom,start,end,numpy=True)))
        chroms.append(chrom)
        region_start.append(start)
        region_end.append(end)
        counts.append(cur_counts)
        
    counts=pd.DataFrame([chroms,region_start,region_end,counts]).transpose()
    #find counts above quantile
    count_vals=counts[3]
    quantiles=np.quantile(count_vals, np.arange(0.01,1.01,0.01))
    max_val=quantiles[args.max_quantile-1]
    outliers=counts[counts[3]>max_val]
    outliers.to_csv(args.outf,header=False,index=False,sep='\t')


if __name__=="__main__":
    main()
    
