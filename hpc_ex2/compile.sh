#!/bin/bash
#SBATCH --partition=THIN
#SBATCH --job-name=compile_scripts
#SBATCH --cpus-per-task=12
#SBATCH --mem=15gb
#SBATCH --time=00:15:00
#SBATCH --output=./logs/compilation%j.out
set -a; source .env set +a

module load "$MPI_MODULE"
module load cmake/3.28.1

cmake .
make
