Dependency versions:
    system: Ubuntu 24.04.1 LTS
    python3: 3.12.3
    python3-pandas: 2.1.4
    python3-tqdm: 4.66.2
    wget: 1.21.4

Notes to filter_mapman.py:
 - Purpose: filter the bincodes to keep only the one largest bin per root bin (root bin is the first number in bincode)
 - Usage:
    python3 filter_mapman.py mapman.tsv > mapman_filtered.tsv
    # now filter proteins according to new mapman table as well
    python3 filter_prots.py mapman_filtered.tsv protein.fa > protein_filtered.fa

Reproduce:
 1. in a new directory, download the proteomes (grep -Po ": \Khttps://.*" README.txt | xargs wget) and extract them if compressed (downloaded on 17.12.2024).
    note that the gitlab link may require access to the repository, so you need to request for it.
 2. afterwards all proteomes are in current directory as faa, fasta, fa files
 3. prepare them for mercator by running:
     ls -1 *_*.fa* | xargs python3 prepare_for_mercator.py
 4. a second version for each proteome exists in *_fixed.fa
 5. go to https://www.plabipd.de/mercator_main.html and submit a job for each *_fixed.fa file:
   1. sequence type: protein
   2. don't include prot-scriber
   3. don't inclue swissprot
   4. *_fixed.fa file
   5. don't use demo file
   6. give a job name (it won't submit if invalid, but snake_case works well)
   7. enter email adress to get the results per email
   8. submit and wait until the job appears below the "Job ... has been submitted" message
   9. wait until jobs are done. If no email provided, the results should be availabe at:
       http://www.plabipd.de/projects/Mercator4_output/JOBID
      where JOBID is the Job ID mentioned in the appeared job below the message (for me the IDs always had the pattern GFA-*)
 6. extract the mercator results, so you have all *.results.txt in current directory, also mapmanreferencebins.results.txt for protein.fa
 7. merge the results:
     mv mapmanreferencebins.results.txt joined_mapman.tsv
     for f in *.txt; do tail -n +2 $f >> joined_mapman.tsv; done
 8. reduce the results:
     python3 reduce_mapman.py joined_mapman.tsv > mapman.tsv
 9. create joined protein.fa:
     mv protein.fa protein_orig.fa
     # now join them and keep only proteins occuring in mapman table
     python3 filter_prots.py mapman.tsv protein_orig.fa *_fixed.fa > protein.fa
10. compress to mapman.tar.bz2
     tar -cjf mapman.tar.bz2 README.txt protein.fa mapman.tsv *.py



Used proteomes:
protein.fa, mapmanreferencebins.results.txt: https://gitlab.rlp.net/a.hallab/aibi-ws-2024-25/-/blob/3ad976a2721a571eaf26e2e07bc2c4d75073237f/material/Mapman_reference_DB_202310.tar.bz2
Rice (Oryza sativa): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/034/140/825/GCF_034140825.1_ASM3414082v1/GCF_034140825.1_ASM3414082v1_protein.faa.gz
Potato (Solanum tuberosum): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/226/075/GCF_000226075.1_SolTub_3.0/GCF_000226075.1_SolTub_3.0_protein.faa.gz
Tomato (Solanum lycopersicum): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/036/512/215/GCF_036512215.1_SLM_r2.1/GCF_036512215.1_SLM_r2.1_protein.faa.gz
Medicago truncatula: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/003/473/485/GCF_003473485.1_MtrunA17r5.0-ANR/GCF_003473485.1_MtrunA17r5.0-ANR_protein.faa.gz
Soybean (Glycine max): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/004/515/GCF_000004515.6_Glycine_max_v4.0/GCF_000004515.6_Glycine_max_v4.0_protein.faa.gz
Grapevine (Vitis vinifera): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/030/704/535/GCF_030704535.1_ASM3070453v1/GCF_030704535.1_ASM3070453v1_protein.faa.gz
Arabidopsis thaliana: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_protein.faa.gz
Faba bean (Vicia faba): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/948/472/305/GCA_948472305.1_Hedin2_genome_v1/GCA_948472305.1_Hedin2_genome_v1_protein.faa.gz
Chlamydomonas reinhardtii: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/002/595/GCF_000002595.2_Chlamydomonas_reinhardtii_v5.5/GCF_000002595.2_Chlamydomonas_reinhardtii_v5.5_protein.faa.gz
Maize (Zea mays): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/902/167/145/GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0/GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_protein.faa.gz
Barley (Hordeum vulgare): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/904/849/725/GCF_904849725.1_MorexV3_pseudomolecules_assembly/GCF_904849725.1_MorexV3_pseudomolecules_assembly_protein.faa.gz
Wheat (Triticum aestivum): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/018/294/505/GCF_018294505.1_IWGSC_CS_RefSeq_v2.1/GCF_018294505.1_IWGSC_CS_RefSeq_v2.1_protein.faa.gz
Sorghum (Sorghum bicolor): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/003/195/GCF_000003195.3_Sorghum_bicolor_NCBIv3/GCF_000003195.3_Sorghum_bicolor_NCBIv3_protein.faa.gz
Banana (Musa acuminata): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/036/884/655/GCF_036884655.1_Cavendish_Baxijiao_AAA/GCF_036884655.1_Cavendish_Baxijiao_AAA_protein.faa.gz
Poplar (Populus trichocarpa): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/002/775/GCF_000002775.5_P.trichocarpa_v4.1/GCF_000002775.5_P.trichocarpa_v4.1_protein.faa.gz
Brachypodium distachyon: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/505/GCF_000005505.3_Brachypodium_distachyon_v3.0/GCF_000005505.3_Brachypodium_distachyon_v3.0_protein.faa.gz
Cucumber (Cucumis sativus): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/004/075/GCF_000004075.3_Cucumber_9930_V3/GCF_000004075.3_Cucumber_9930_V3_protein.faa.gz
Cotton (Gossypium hirsutum): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/007/990/345/GCF_007990345.1_Gossypium_hirsutum_v2.1/GCF_007990345.1_Gossypium_hirsutum_v2.1_protein.faa.gz
Canola/Rapeseed (Brassica napus): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/020/379/485/GCF_020379485.1_Da-Ae/GCF_020379485.1_Da-Ae_protein.faa.gz
Eucalyptus (Eucalyptus grandis): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/016/545/825/GCF_016545825.1_ASM1654582v1/GCF_016545825.1_ASM1654582v1_protein.faa.gz
Peach (Prunus persica): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/346/465/GCF_000346465.2_Prunus_persica_NCBIv2/GCF_000346465.2_Prunus_persica_NCBIv2_protein.faa.gz
Coffee (Coffea arabica): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/003/713/225/GCF_003713225.1_Cara_1.0/GCF_003713225.1_Cara_1.0_protein.faa.gz
Cassava (Manihot esculenta): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/001/659/605/GCF_001659605.2_M.esculenta_v8/GCF_001659605.2_M.esculenta_v8_protein.faa.gz
Date Palm (Phoenix dactylifera): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/389/715/GCF_009389715.1_palm_55x_up_171113_PBpolish2nd_filt_p/GCF_009389715.1_palm_55x_up_171113_PBpolish2nd_filt_p_protein.faa.gz
Foxtail Millet (Setaria italica): https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/263/155/GCF_000263155.2_Setaria_italica_v2.0/GCF_000263155.2_Setaria_italica_v2.0_protein.faa.gz
Physcomitrella patens: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/002/425/GCF_000002425.4_Phypa_V3/GCF_000002425.4_Phypa_V3_protein.faa.gz
Marchantia polymorpha: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/037/833/965/GCA_037833965.1_MpTak2_v7.1/GCA_037833965.1_MpTak2_v7.1_protein.faa.gz
Cryptomeria japonica: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/030/272/615/GCF_030272615.1_Sugi_1.0/GCF_030272615.1_Sugi_1.0_protein.faa.gz
Azolla filiculoides: https://fernbase.org/ftp/Azolla_filiculoides/Azolla_asm_v1.1/Azolla_filiculoides.protein.highconfidence_v1.1.fasta
Adiantum capillus-veneris: https://fernbase.org/ftp/Adiantum_capillus-veneris/Adc_genome_protein.fa