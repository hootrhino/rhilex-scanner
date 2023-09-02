package main

import (
	"fmt"
	"net"
	"os"
	"time"
)

// StartServer 启动UDP服务器，监听指定端口，处理客户端请求
func StartServer(port int) {
	// 解析UDP地址
	udpAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("0.0.0.0:%d", port))
	if err != nil {
		fmt.Println("Error resolving UDP address:", err)
		os.Exit(1)
	}

	// 创建UDP连接
	conn, err := net.ListenUDP("udp", udpAddr)
	if err != nil {
		fmt.Println("Error creating UDP connection:", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Printf("UDP server listening on port %d...\n", port)

	for {
		// 接收数据
		buffer := make([]byte, 1024)
		n, addr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Error reading from UDP connection:", err)
			continue
		}

		// 打印接收到的数据
		fmt.Printf("Received data from %s: %s\n", addr, string(buffer[:n]))

		// 回复"OK"
		response := []byte("OK")
		_, err = conn.WriteToUDP(response, addr)
		if err != nil {
			fmt.Println("Error sending response:", err)
		}
	}
}
func Request() {
	// 目标广播地址和端口，这里使用的是通用的IPv4广播地址
	broadcastAddr := "127.0.0.1:1994" // 请替换为实际的广播地址和端口

	// 准备要发送的数据
	message := "NODE_INFO"

	// 解析广播地址
	udpAddr, err := net.ResolveUDPAddr("udp", broadcastAddr)
	if err != nil {
		fmt.Println("Error resolving broadcast address:", err)
		os.Exit(1)
	}

	// 创建UDP连接
	conn, err := net.DialUDP("udp", nil, udpAddr)
	if err != nil {
		fmt.Println("Error creating UDP connection:", err)
		os.Exit(1)
	}
	defer conn.Close()

	// 将消息转换为字节数组并发送
	_, err = conn.Write([]byte(message))
	if err != nil {
		fmt.Println("Error sending message:", err)
		os.Exit(1)
	}

	// 接收回复数据
	buffer := make([]byte, 10)
	n, _, err := conn.ReadFromUDP(buffer)
	if err != nil {
		fmt.Println("Error reading from UDP connection:", err)
		os.Exit(1)
	}

	// 打印回复数据
	fmt.Printf("Received response: %s\n", string(buffer[:n]))

	// 如果有回复则输出"OK"
	fmt.Println("OK")
}

func main() {
	go StartServer(1994)
	Request()
	time.Sleep(5 * time.Second)
}
