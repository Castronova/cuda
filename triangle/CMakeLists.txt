cmake_minimum_required(VERSION 3.2)
project(triangle)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")



add_definitions(-DTRILIBRARY -O3 -DSELF_CHECK -I/usr/local/lib -L/usr/local/include -lx11 )
set(SOURCE_FILES
    showme.c
    triangle.c
    triangle.h
    tricall.c)
#
add_executable(triangle ${SOURCE_FILES})

## force cmake to call makefile
#add_custom_target(triangle COMMAND make -C ${triangle_SOURCE_DIR}
#                         CLION_EXE_DIR=${PROJECT_BINARY_DIR})