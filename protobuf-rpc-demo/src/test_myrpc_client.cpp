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
