#!/bin/bash
#SBATCH --partition=THIN
#SBATCH --job-name=run_osu_bcast_barrier
#SBATCH --ntasks-per-node=24
#SBATCH --ntasks=48
#SBATCH --exclusive
#SBATCH --mem=15gb
#SBATCH --time=01:00:00
#SBATCH --output=./logs/run_out%j.out
set -a; source .env set +a

module load "$MPI_MODULE"

# Add osu to the path for ease of use
PATH=$PATH:${OSU_COMPILED_PATH}/libexec/osu-micro-benchmarks/mpi/collective
python3 run_tests.py
