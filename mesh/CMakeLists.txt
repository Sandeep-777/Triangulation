cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
project(greedy_projection)
find_package(PCL 1.2 REQUIRED)
include_directories(${PCL_INCLUDE_DIRS} /usr/local/include/pcl-1.7 )
link_directories(${PCL_LIBRARY_DIRS} usr/local/lib)
add_definitions(${PCL_DEFINITIONS})
add_executable(greedy_projection greedy_projection.cpp)
target_link_libraries(greedy_projection ${PCL_LIBRARIES})
