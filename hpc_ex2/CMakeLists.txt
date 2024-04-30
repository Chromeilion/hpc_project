cmake_minimum_required(VERSION 3.26)
project(hw1)

set(CMAKE_C_STANDARD 23)
find_package(MPI REQUIRED)
include_directories(SYSTEM ${MPI_INCLUDE_PATH})
add_executable(2a 2a.c)
target_link_libraries(2a ${MPI_C_LIBRARIES})
