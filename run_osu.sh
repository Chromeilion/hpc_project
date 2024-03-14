#!/bin/bash
#SBATCH --partition=THIN
#SBATCH --job-name=run_osu_bcast_barrier
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --mem=15gb
#SBATCH --time=00:15:00
#SBATCH --output=./logs/run_out%j.out
set -a; source .env set +a

module load "${MPI_MODULE}"

# Set path for ease of use
PATH=$PATH:${COMPILED_PATH}/libexec/osu-micro-benchmarks/mpi/collective

srun -n "$SLURM_NTASKS" osu_bcast > bcast.txt
srun -n "$SLURM_NTASKS" osu_barrier > barrier.txt
