#include "myrpc.h"
#include "echo.pb.h"

class MyEchoService : public echo::EchoService {
public:
  virtual void Echo(::google::protobuf::RpcController* /* controller */,
                       const ::echo::EchoRequest* request,
                       ::echo::EchoResponse* response,
                       ::google::protobuf::Closure* done) {
      std::cout << request->msg() << std::endl;
      response->set_msg(
              std::string("I have received '") + request->msg() + std::string("'"));
      done->Run();
  }
};//MyEchoService

int main() {
    MyServer my_server;
    MyEchoService echo_service;
    my_server.add(&echo_service);
    my_server.start("127.0.0.1", 6688);

    return 0;
}

/* vim: set ts=4 sw=4 sts=4 tw=100 */
