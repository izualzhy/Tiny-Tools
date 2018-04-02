PROJECT(protobuf-rpc-demp)
cmake_minimum_required(VERSION 3.2)
add_compile_options(-std=c++11)

INCLUDE_DIRECTORIES(
    ./src
    ../../../../bc_out/third-64/protobuf/output/include
    ../../../../bc_out/third-64/boost/output/include)
LINK_DIRECTORIES(../../../../bc_out/third-64/protobuf/output/lib)
LINK_DIRECTORIES(../../../../bc_out/third-64/boost/output/lib)
LINK_DIRECTORIES(./build)

SET(LIBMYRPC_SRC ./src/rpc_meta.pb.cc)
ADD_LIBRARY(myrpc STATIC ${LIBMYRPC_SRC})
ADD_EXECUTABLE(server ./src/echo.pb.cc ./src/test_myrpc.cpp)
TARGET_LINK_LIBRARIES(server libprotobuf.a libboost_signals.a libboost_system.a libmyrpc.a)
ADD_EXECUTABLE(client ./src/echo.pb.cc ./src/test_myrpc_client.cpp)
TARGET_LINK_LIBRARIES(client libprotobuf.a libboost_signals.a libboost_system.a libmyrpc.a)
