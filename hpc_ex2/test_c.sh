#!/bin/bash
#SBATCH --partition=THIN
#SBATCH --job-name=c_testing
#SBATCH --ntasks-per-node=15
#SBATCH --ntasks=30
#SBATCH --exclusive
#SBATCH --mem=15gb
#SBATCH --time=00:15:00
#SBATCH --output=./logs/run_out%j.out
set -a; source .env set +a

module load "$MPI_MODULE"

# Add osu to the path for ease of use
PATH=$PATH:${OSU_COMPILED_PATH}/libexec/osu-micro-benchmarks/mpi/collective
python3 run_tests_circ.py
