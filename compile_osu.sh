#!/bin/bash
#SBATCH --partition=THIN
#SBATCH --job-name=osu_compilation_
#SBATCH --cpus-per-task=12
#SBATCH --mem=15gb
#SBATCH --time=00:15:00
#SBATCH --output=./logs/compilation%j.out
set -a; source .env set +a

module load "${MPI_MODULE}"

mkdir osu
wget -qO- https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.3.tar.gz | tar xvz -C ./osu
cd ./osu/*/ || exit
./configure CC=mpicc CXX=mpicxx --prefix="${COMPILED_PATH}" 
make 
make install
