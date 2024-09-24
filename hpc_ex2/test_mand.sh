#!/bin/bash
#SBATCH --partition=THIN
#SBATCH --job-name=m_testing
#SBATCH --ntasks-per-node=1
#sbatch --cpus-per-task=24
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --mem=15gb
#SBATCH --time=02:30:00
#SBATCH --output=./logs/run_out%j.out
set -a; source .env set +a

module load "$MPI_MODULE"

# Add osu to the path for ease of use
PATH=$PATH:${OSU_COMPILED_PATH}/libexec/osu-micro-benchmarks/mpi/collective
python3 run_tests_mand.py
