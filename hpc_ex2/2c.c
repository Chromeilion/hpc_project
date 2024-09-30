#include <complex.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>


// How many times to iterate the threshold T
double NO_T_STEPS = 10;
double T_MAX = 1;
double T_BASE = 3;

// Storage for a single pixel coordinate
typedef struct {
    unsigned int x;
    unsigned int y;
    unsigned char data;
} pixel;

// A semifinished pixel. Useful for caching.
typedef struct {
    pixel *pxl; // Actual pixel object
    unsigned int iter_no; // The current iteration of the pixel
    bool completed; // Whether the pixel has been fully computed
    complex long double c_data; // The computed complex value of the pixel
    complex long double z_data; // Computed value for the current iteration
} unfinished_pixel;

void write_pgm_image( void *image, int maxval, int xsize, int ysize, const char *image_name)
/*
 * image        : a pointer to the memory region that contains the image
 * maxval       : either 255 or 65536
 * xsize, ysize : x and y dimensions of the image
 * image_name   : the name of the file to be written
 *
 */
{
    FILE* image_file;
    image_file = fopen(image_name, "w");

    // Writing header
    // The header's format is as follows, all in ASCII.
    // "whitespace" is either a blank or a TAB or a CF or a LF
    // - The Magic Number (see below the magic numbers)
    // - the image's width
    // - the height
    // - a white space
    // - the image's height
    // - a whitespace
    // - the maximum color value, which must be between 0 and 65535
    //
    // if he maximum color value is in the range [0-255], then
    // a pixel will be expressed by a single byte; if the maximum is
    // larger than 255, then 2 bytes will be needed for each pixel
    //

    int color_depth = 1 + ( maxval > 255 );

    fprintf(image_file, "P5\n# generated by\n# put here your name\n%d %d\n%d\n", xsize, ysize, maxval);

    // Writing file
    fwrite( image, 1, xsize*ysize*color_depth, image_file);

    fclose(image_file);
}

double t_func(const unsigned int x) {
    return pow(T_BASE, (x-NO_T_STEPS)) * T_MAX;
}

// The Mandelbrot set function
void increment_fc(complex long double *z, const complex long double *c) {
    *z = cpow(*z, 2) + *c;
}

// Check whether a point is in the Mandelbrot set using a number of iterations T.
unsigned short int in_m(complex long double *z,
                        const complex long double *c,
                        const unsigned short int T) {
    unsigned short int i = 0;
    while (cabsl(*z) < 2 && i < T) {
        increment_fc(z, c);
        ++i;
    }
    return i;
}

// Check whether a given pixel is in the set and return a bounded output.
void pxl_in_m(unfinished_pixel* pxl,
              const unsigned int *T) {
    complex long double *z_val = &pxl->z_data;
    const complex long double *c_val = &pxl->c_data;
    unsigned int iter_to_do = *T - pxl->iter_no;
    unsigned short int iter = in_m(z_val, c_val, iter_to_do);
    pxl->iter_no += iter;
}

// Run all Mandelbrot set calculations on the provided array.
unsigned int run_calculations(unfinished_pixel** incomplete,
                              const complex double *bottom_left,
                              const unsigned int arr_size,
                              const unsigned int *T,
                              const unsigned int *max_iters) {
    unsigned int c = 0;
#pragma omp parallel for default(none) shared(T, bottom_left, arr_size, incomplete, max_iters) reduction(+:c)
    for (int i = 0; i < arr_size; ++i) {
        unfinished_pixel* current_pixel = incomplete[i];
        pxl_in_m(current_pixel, T);
        if (current_pixel->iter_no < *T) {
            current_pixel->completed = true;
            c += 1;
        }
    }
    return c;
}

// Run all calculations while iteratively increasing the threshold value.
bool run_calculations_iter(pixel *arr,
                           const complex double *bottom_left,
                           const complex double *top_right,
                           const int n_x,
                           const int n_y,
                           const int arr_size,
                           const unsigned int *T) {
    const double x_range = creal(*top_right) - creal(*bottom_left);
    const double x_increment = x_range / n_x;
    const double y_range = cimag(*top_right) - cimag(*bottom_left);
    const double y_increment = y_range / n_y;

    // Create the initial job array
    unfinished_pixel* unfinished_pixels =
            (unfinished_pixel*)calloc(arr_size, sizeof(unfinished_pixel));
    unfinished_pixel** job_array =
            (unfinished_pixel**)calloc(arr_size, sizeof(unfinished_pixel*));
    for (unsigned int i = 0; i < arr_size; ++i) {
        complex double c_d = *bottom_left + arr[i].x * x_increment +
                arr[i].y * y_increment * I;
        unfinished_pixels[i] = (unfinished_pixel) {
                .completed = false, .pxl = &arr[i], .iter_no = 0, .c_data = c_d,
                .z_data = 0
        };
        job_array[i] = &unfinished_pixels[i];
    }
    unsigned int current_iter;
    unsigned int prev_job_size = arr_size;
    unsigned int completed;
    // Would love to multithread this but with the current implementation
    // it would go horribly.
    for (unsigned int j = 1; j <= NO_T_STEPS; ++j) {
        current_iter = (unsigned int)round(*T * t_func(j));
        completed = run_calculations(job_array,
                                     bottom_left,
                                     prev_job_size,
                                     &current_iter,
                                     T);
        unsigned int counter = 0;
        for (unsigned int i = 0; i < prev_job_size; ++i) {
            if (!job_array[i]->completed) {
                job_array[counter] = job_array[i];
                counter += 1;
                if (counter >= prev_job_size - completed) { break; }
            }
        }
        prev_job_size -= completed;
    }
    free(job_array);
#pragma omp for
    for (unsigned int i = 0; i < arr_size; ++i) {
        unfinished_pixels[i].pxl->data =
                (unsigned char)round((double)unfinished_pixels[i].iter_no *
                ((double)255 / (double)*T));
    }
    free(unfinished_pixels);
    return 0;
}

// Initialize an array of pixels.
void init_pixels(pixel *pixels,
                 const unsigned int n_y,
                 const unsigned int n_x) {
    for (unsigned int row = 0; row < n_y; ++row) {
        for (unsigned int column = 0; column < n_x; ++column) {
            pixel *current_item = &pixels[row * n_x + column];
            current_item->x = column;
            current_item->y = row;
        }
    }
}

// Save the array to an image.
int save_to_image(pixel *pixels, unsigned const int arr_len,
                  const int n_x, const int n_y) {
    unsigned char *img = (unsigned char*)calloc(arr_len, sizeof(unsigned char));
    for (unsigned int i = 0; i < arr_len; ++i) {
        unsigned char data = pixels[i].data;
        if (data == 255) { data = 0; }
        img[i] = data;
    }
    write_pgm_image(img, 255, n_x, n_y, "m_set.pgm");
    free(img);
    return 0;
}

// Print an array of pixels
int print_array(pixel *pixels, unsigned const int arr_len) {
    for (unsigned int i = 0; i < arr_len; ++i) {
        printf("%u ", pixels[i].data);
    }
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 7) {
        printf("Please specify all required arguments!!!");
        return 1;
    }
    // I'd like to use an int type for n_x and n_y to make conversion to double
    // easier in the future. Since there's no string to int function, we first
    // get a long and then convert it to an int.
    const long n_x_ = strtol(argv[1], NULL, 10);
    const long n_y_ = strtol(argv[2], NULL, 10);
    if (n_x_ > INT_MAX || n_y_ > INT_MAX || n_x_ < INT_MIN || n_y_ < INT_MIN) {
        printf("The provided image sizes (n_x, n_y) are too large or too "
               "small!!!");
        return 1;
    }
    const int n_x = (const int)n_x_;
    const int n_y = (const int)n_y_;

    long double x_l;
    sscanf(argv[3], "%Lf", &x_l);
    long double y_l;
    sscanf(argv[4], "%Lf", &y_l);
    long double x_r;
    sscanf(argv[5], "%Lf", &x_r);
    long double y_r;
    sscanf(argv[6], "%Lf", &y_r);
    long i_max_ = strtol(argv[7], NULL, 10);
    if (i_max_ > USHRT_MAX || i_max_ < 0) {
        printf("The provided iteration no (I) is too large or less than "
               "zero!!!");
        return 1;
    }
    const unsigned int i_max = i_max_;

    complex double bottom_left = x_l + y_l*I;
    complex double top_right = x_r + y_r*I;

    int arr_len = n_x * n_y;
    pixel *pxls = (pixel*)calloc(arr_len, sizeof(pixel));
    init_pixels(pxls, n_x, n_y);
    run_calculations_iter(pxls, &bottom_left, &top_right, n_x, n_y,
                          arr_len, &i_max);
    save_to_image(pxls, arr_len, n_x, n_y);
    print_array(pxls, arr_len);
    free(pxls);
    return 0;
}
