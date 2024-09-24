#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>


// Append an array to a given file.
void write_arr(int arr[], int no_rows, FILE *fp) {
    for (unsigned row = 0; row < no_rows; row++) {
        fprintf(fp, "%i, ", arr[row]);
        fprintf(fp, "\n");
    }
}

int main() {
    MPI_Init(NULL, NULL);

    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    int my_msg = world_rank;

    int* res = calloc(world_size, sizeof(int));
    res[world_rank] = my_msg;

    int before = world_rank - 1;
    if (before == -1) {before = world_size-1;}
    int after = (world_rank + 1) % world_size;
    int i;
    clock_t start, end;
    double cpu_time_used;
    if (world_rank == 1) {
        start = clock();
    }
    for (i = 0; i < world_size-1; ++i) {
        MPI_Sendrecv(
                &res[(after+i-1+world_size)%world_size],
                1,
                MPI_INT,
                before,
                world_rank,
                &res[(after+i)%world_size],
                1,
                MPI_INT,
                after,
                after,
                MPI_COMM_WORLD,
                MPI_STATUS_IGNORE);
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    if (world_rank == 1) {
        FILE *fp;
        fp = fopen("all_stuffs.txt", "w");
        write_arr(res, world_size, fp);

        FILE *fp2;
        fp2 = fopen("time_taken.txt", "w");
        fprintf(fp2, "%f\n", cpu_time_used);
        fclose(fp2);
    }
    free(res);
    MPI_Finalize();
    return 0;
}

