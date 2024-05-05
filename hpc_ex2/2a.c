#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>


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
    int buf = my_msg;
    int i;
    for (i = 0; i < world_size; ++i) {
        MPI_Send(&buf, 1, MPI_INT, before, world_rank, MPI_COMM_WORLD);
        MPI_Recv(&buf, 1, MPI_INT, after, after, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        res[(after+i) % world_size] = buf;
    }
    if (world_rank == 1) {
        FILE *fp;
        fp = fopen("all_stuffs.txt", "w");
        write_arr(res, world_size, fp);
    }
    free(res);
    MPI_Finalize();
    return 0;
}

