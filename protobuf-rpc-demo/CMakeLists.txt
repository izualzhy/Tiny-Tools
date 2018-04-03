PROJECT(protobuf-rpc-demp)
cmake_minimum_required(VERSION 3.2)
add_compile_options(-std=c++11)

include_directories(
    ./src
    ../../../../bc_out/third-64/protobuf/output/include
    ../../../../bc_out/third-64/boost/output/include)
link_directories(
    ../../../../bc_out/third-64/protobuf/output/lib
    ../../../../bc_out/third-64/boost/output/lib
    ./build)

set(LIBMYRPC_SRC ./src/rpc_meta.pb.cc)
add_library(myrpc ${LIBMYRPC_SRC})
add_executable(server ./src/echo.pb.cc ./src/test_myrpc.cpp)
target_link_libraries(server libprotobuf.a libboost_signals.a libboost_system.a myrpc)
add_executable(client ./src/echo.pb.cc ./src/test_myrpc_client.cpp)
target_link_libraries(client libprotobuf.a libboost_signals.a libboost_system.a myrpc)
