#!/bin/bash

# *** specific slurm job directives ***
#SBATCH --account=cdsc_project1
#SBATCH --job-name=job1
#SBATCH --output="slurm-%j.txt"

# *** general slurm job directives ***
#SBATCH --mail-type=NONE
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=4000m 
#SBATCH --time=24:00:00
#SBATCH --partition=standard

# *** application ***
hostname
pwd






