# ZeroMQ 介绍

* ZeroMQ（也称为ØMQ）是一个高性能的异步消息库，用于构建分布式和并发应用。它提供了多种通信模式，如请求-回复、发布-订阅、推-拉等，使得进程间通信，多机通信等变得简单。

* ​套接字类型​​：ZeroMQ提供了多种套接字类型，每种类型对应一种通信模式：
  * ​请求-回复（REQ-REP）​​：用于同步的请求-回复模式，类似HTTP。
  * ​发布-订阅（PUB-SUB）​​：用于一对多的消息分发，发布者发送消息，订阅者接收感兴趣的消息。
  * ​​推-拉（PUSH-PULL）​​：用于管道模式，消息从推端流向拉端，适合负载均衡。
  * ​配对（PAIR）​​：用于一对一的通信，两个套接字直接连接。
  * ​路由-委托（ROUTER-DEALER）​​：用于高级的请求-回复模式，可以构建复杂的代理结构。

## 传输协议

> ZeroMQ 支持多种传输协议，每种协议针对不同的使用场景，不同平台（windows,linux,vxworks,..）支持也有差异，protocol定义如下：

```c++
/// src/address.hpp
namespace protocol_name
{
static const char inproc[] = "inproc";
static const char tcp[] = "tcp";
static const char udp[] = "udp";
#ifdef ZMQ_HAVE_OPENPGM
static const char pgm[] = "pgm";
static const char epgm[] = "epgm";
#endif
#ifdef ZMQ_HAVE_NORM
static const char norm[] = "norm";
#endif
#ifdef ZMQ_HAVE_WS
static const char ws[] = "ws";
#endif
#ifdef ZMQ_HAVE_WSS
static const char wss[] = "wss";
#endif
#if defined ZMQ_HAVE_IPC
static const char ipc[] = "ipc";
#endif
#if defined ZMQ_HAVE_TIPC
static const char tipc[] = "tipc";
#endif
#if defined ZMQ_HAVE_VMCI
static const char vmci[] = "vmci";
#endif
}
```

* 简单介绍下linux上常用的protocol:
  * 其中 udp 更适合可靠性要求不高、实时性要求高的广播模式。
  * inproc 作用不大，线程间通过BlockingQueue等队列传数据对象共享指针更好，对于复杂结构体数据会省去序列化/反序列化操作，性能更好。

| 协议 | 前缀 | 适用场景 | 性能特点 |
|------|------|----------|----------|
| **tcp** | `tcp://` | 跨网络通信 | 高吞吐量，可靠 |
| **ipc** | `ipc://` | 进程间通信 | 低延迟，高性能 |
| **udp** | `udp://` | 多播/广播 | 实时性，可扩展 |
| **inproc** | `inproc://` | 线程间通信 | 最快 |

> 套接字类型与协议常用组合:

| 套接字类型 | 适用协议 | 典型应用场景 |
|------------|----------|--------------|
| **PUB/SUB** | TCP,UDP, PGM, EPGM, IPC | 发布/订阅模式，一对多消息分发 |
| **XPUB/XSUB** | TCP, IPC | 代理模式，消息过滤和转发 |
| **PUSH/PULL** | TCP, IPC | 管道模式，负载均衡 |
| **REQ/REP** | TCP, IPC | 请求/响应模式 |
| **ROUTER/DEALER** | TCP, IPC | 高级路由模式,负载均衡器 |
| **PAIR** | TCP, IPC | 点对点通信 |

## 整体类图框架

![zeromq_class](./assets/puml/zeromq_class.puml)

* 以 tcp,ipc 相关文件分析，其他也是类似的；
* protocol_name : 协议类型字符串定义；
* address : 解析地址 将 `tcp://127.0.0.1:80` 等 解析成需要的数据；



## 使用示例

![server](./assets/puml/simple_server_sequence.mermaid)