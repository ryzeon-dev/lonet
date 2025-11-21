cmake_minimum_required(VERSION 3.20)
project(cpp)

set(CMAKE_CXX_STANDARD 20)

add_library(net_if_binding SHARED binding.cpp)