breakGFW - 提高墙内Mac用户翻墙体验
===


 Net上本没有墙，Reset的多了也便有了墙
---
我待天网如初恋，天网置我千万遍，在一次次被Reset后，我走上了翻墙之路，墙外这边风景虽好，但我等毕竟“心在曹营身在汉”，免不了在墙头东张西望。
米国有句话说的好，自由是有代价的。开始墙头生活后，烦恼亦随之而至：每次开机、休眠后需要重连VPN；连上之后，VPN还时不时掉线；访问国内网站南辕北辙，龟速难忍，即使添加了天网路由表，DNS解服务器会告诉你联通和电信的距离有多远。在Google了一番之后，我写了个小脚本，让翻墙生活看起来更美好。


工作原理
---
  - 建立VPN连接后，让VPN接管所有的网络流量
  - 添加天网路由表，访问国内网络不经过VPN
  - VPN的nameserver一般会默认为国外的IP地址，如Google DNS或openDNS，解析域名的数据包会经过VPN线路发送，对于大型站点，解析到的IP地址往往不是离访问者物理距离最近的IP，所以，需要把nameserver地址也增加进路由表，这样就能解析到最优的IP地址。大家可能会问，这样不会导致国外的域名解析不准确么？不过好在被GFW的域名，一般是不会在中国部署服务器的，哈哈。
  - 对于国外一些没有被GFW的站点、对访问者又比较频繁的网站，让这部分地址直接加入路由表，避免经过VPN发送


 警告
---
使用此工具后，访问国内网站会暴露自己真实的IP地址，请慎重使用此工具。


### 安装
    git clone https://github.com/puwaifu/breakGFW.git
    cd breakGFW
    sudo ./bfw install
注意：命令行工具需要使用breakGFW目录，在卸载之前，请不要删除该目录。


### 使用

首先，在网络设置中，添加一个VPN，服务名为 breakGFW，让所有数据经过VPN转发。服务名也可以是其他名字，不过这样的话在后续的命令行工具中，就需要指定服务名。

启动
    sudo bfw start [service name]
<service name> 为你添加的服务名，如果不传递服务名，默认为breakGFW

监控VPN状态，掉线重连
    sudo bfw auto [service name]

停止
    sudo bfw stop [service name]

重启
    sudo bfw restart [service name]

添加指定的IP或者网段到路由表
    sudo bfw add ip <ip or net>
如果不指定IP，则添加所有天网IP段和用户添加的IP到路由表中。新增加的IP地址会记录在本地文件中，下次无需再次添加。

从路由表删除IP
    sudo bfw delete ip [ip or net]
如果不指定IP，则从路由表删除所有天网IP段和用户添加的IP。指定IP后，只删除对应的IP，并且会从本地IP记录中删除IP

查看当前的直连IP
    bfw list ip

添加指定的网站到路由表
    sudo bfw add site <www.site.com>
解析到的多个IP地址，会添加到路由表，对于同一个域名的不同子域名，需要分别添加。域名会记录在本地文件中，下次无需再次添加。

从路由表删除网站
    sudo bfw delete site <www.site.com>
从路由表中删除域名解析到的IP，并从本地网站记录中删除网站。

强烈推荐添加自动启动并监控VPN状态，一劳永逸。还有附加的好处，使用 add、delete 指令时，无需输入烦人的sudo。
    sudo echo "bfw start" >> /etc/rc.local
    sudo echo "bfw auto" >> /etc/rc.local

版本支持
---
因笔者使用Mac，故没有编写Linux和Windows版本，后续有必要的话，可考虑移植到Linux和Windows

后记
---
不用的域名利用不用的nameserver来解析这个问题，本来在*nix下有完美的解决办法:在/etc/resolver目录下增加不同的域名指示文件，但是Mac并没有使用*nix内置的resolver，而使用的mDNSResponder又存在BUG，在添加多个域名指示文件后，即会出现无法解析dns的错误，故无法采取此种方法。另外，自动连接vpn使用的是networksetup -connectpppoeservice，可是同系列的networksetup -disconnectpppoeservice却无法工作，真实相当的奇怪。望不吝赐教。
