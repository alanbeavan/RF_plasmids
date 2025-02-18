#to make this generic, read in directory as argument
#needs to be the actual experiment directory - so 12345/2025-01-01-01-01-01-01
#or the like
if [[ $# -ne 2 ]]; then
    echo "USAGE ./run_kit_and_kaboodle.sh exp_dir lvlX"
    exit 1
fi


dir=$1
lvl=$2

if ! [ -d "$dir" ]; then
  echo "$dir does not exist."
  exit 1
fi

cd $dir

ls='ls | grep -v "^_" | grep -v "\."';
runs=$(eval "$ls");

for run in $runs; do
    cd $run
    gunzip ${run}_raw.fastq.gz
    #sort path out
    python3 ~/OneDrive\ -\ The\ University\ of\ Nottingham/experimental_evolution_project/fastq_to_fasta.py ${run}_raw.fastq ${run}_raw.fasta
    blastn  -query ${run}_raw.fasta -db /Users/mbzab1/Library/CloudStorage/OneDrive-TheUniversityofNottingham/experimental_evolution_project/test_libraries/cds.fa -outfmt 6 -out blast_hits_cds.tab
    blastn  -evalue 10E-7 -word_size 7  -query ${run}_raw.fasta -db /Users/mbzab1/Library/CloudStorage/OneDrive-TheUniversityofNottingham/experimental_evolution_project/test_libraries/terminators.fa  -outfmt 6 -out blast_hits_terminators.tab
    blastn  -evalue 10E-7 -word_size 7  -query ${run}_raw.fasta -db /Users/mbzab1/Library/CloudStorage/OneDrive-TheUniversityofNottingham/experimental_evolution_project/test_libraries/promotors.fa  -outfmt 6 -out blast_hits_promotors.tab
    blastn  -evalue 10E-7 -word_size 7  -query ${run}_raw.fasta -db /Users/mbzab1/Library/CloudStorage/OneDrive-TheUniversityofNottingham/experimental_evolution_project/test_libraries/rbs.fa  -outfmt 6 -out blast_hits_rbs.tab
    blastn  -evalue 10E-7 -word_size 7  -query ${run}_raw.fasta -db /Users/mbzab1/Library/CloudStorage/OneDrive-TheUniversityofNottingham/experimental_evolution_project/test_libraries/flanking_seqs.fa  -outfmt 6 -out blast_hits_flankers.tab
    
#These 2 lines are probably unnecessary for most runs but I'll leave them here commented in case I need to access them elsewhere
    #blastn -query ${run}_raw.fasta -evalue 1e-10 -db ../../../../blast_dbs/BW25113.cds.fa -outfmt 6 -out BW25113_hits.tab
    #blastn -query ${run}_raw.fasta -evalue 1e-10 -db ../../../../blast_dbs/NEB-10-beta.cds.fa -outfmt 6 -out NEB-10-beta_hits.tab

    grep $lvl blast_hits_flankers.tab > temp ; mv temp blast_hits_flankers.tab
    python3 ~/OneDrive\ -\ The\ University\ of\ Nottingham/experimental_evolution_project/select_best_hit.py blast_hits_rbs.tab > temp ; mv temp blast_hits_rbs.tab
    python3 ~/OneDrive\ -\ The\ University\ of\ Nottingham/experimental_evolution_project/select_best_hit.py blast_hits_promotors.tab > temp ; mv temp blast_hits_promotors.tab
    python3 ~/OneDrive\ -\ The\ University\ of\ Nottingham/experimental_evolution_project/select_best_hit.py blast_hits_terminators.tab > temp ;  mv temp blast_hits_terminators.tab
    
    cd ../
done

#now process the results
python3 ~/OneDrive\ -\ The\ University\ of\ Nottingham/experimental_evolution_project/get_order_of_elements.py $dir
