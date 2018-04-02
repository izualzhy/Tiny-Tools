/***************************************************************************
 * 
 * Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
 * $Id$ 
 * 
 **************************************************************************/
 
 /**
 * @file bd_test/protobuf_test/src/test_myrpc_client.cpp
 * @author zhangying21(zhangying21@baidu.com)
 * @date 2018/03/25 21:40:14
 * @version $Revision$ 
 * @brief 
 *  
 **/

#include <iostream>
#include "echo.pb.h"
#include "myrpc.h"

int main() {
    MyChannel channel;
    channel.init("127.0.0.1", 6688);

    echo::EchoRequest request;
    echo::EchoResponse response;
    request.set_msg("hello, myrpc.");

    echo::EchoService_Stub stub(&channel);
    MyController cntl;
    stub.Echo(&cntl, &request, &response, NULL);
    std::cout << "resp:" << response.msg() << std::endl;

    return 0;
}

/* vim: set ts=4 sw=4 sts=4 tw=100 */
