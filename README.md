breakGFW - 提高Mac用户翻墙体验
===


 Net上本没有墙，Reset的多了也便有了墙
---
>我待天网如初恋，天网置我千万遍，在一次次被Reset后，我走上了翻墙之路。墙外这边风景虽好，但我等毕竟“心在曹营身在汉”，免不了在墙头东张西望。
>米国有句话说的好，自由是有代价的。开始墙头生活后，烦恼亦随之而至：每次开机、休眠后需要重连VPN；连上之后，VPN还时不时掉线；访问国内网站南辕北辙，龟速难忍，即使添加了天网路由表，DNS解服务器亦会告诉你联通和电信的距离有多远。在Google了一番之后，我写了个小脚本，让翻墙生活看起来更美好。


工作原理
---
  - 建立VPN连接后，让VPN接管所有的网络流量；
  - 添加天网路由表，访问国内网络不经过VPN；
  - 针对不同的域名利用不同的nameserver解析，这样国内域名就可以解析到最优IP；
  - 对于国外一些没有被GFW的、而对访问者来说又比较频繁的网站，访问这部分网站不经过VPN转发；


警告
---
使用此工具后，访问国内网站会暴露自己真实的IP地址，请慎重使用此工具。


### 安装
    #此工具利用了Python的Twisted库来建立本地的DNS Resolver，请确保本机安装了Python
    #如果没有安装Twister，请按如下步骤安装Twisted
    curl -o Twisted-12.1.0.tar.bz2 http://twistedmatrix.com/Releases/Twisted/12.1/Twisted-12.1.0.tar.bz2
    tar jxvf Twisted-12.1.0.tar.bz2
    cd Twisted-12.1.0
    sudo python setup.py install
    
    #安装breakGFW
    git clone https://github.com/puwaifu/breakGFW.git
    sudo breakGFW/bfw install
注意：命令行工具需要使用breakGFW目录，在卸载之前，请不要删除该目录。


### 使用

>翻墙默认域名解析解析服务器为8.8.8.8和8.8.4.4，如果需要修改，请自行编辑 breakGFW/free_resolv.conf文件。

>国内域名解析服务器会动态获取以太网域名服务解析器，在start指令中，会在vpn启动前复制/etc/resolv.conf中的记录，为以防万一，请自行新建国内域名解析服务器配置文件 breakGFW/china_resolv.conf，并将你所知道的你本地的域名解析服务器IP地址增加进去。

>在启动breakGFW前，请先在网络设置中，添加一个VPN，服务名为 breakGFW，在高级里配置设置首选DNS服务器地址为 127.0.0.1，并且选择经由VPN发送所有网络数据。服务以也可以是其他名字，不过这样在后续的命令行工具中，就需要指定服务名。建议用默认服务名。

    #启动breakGFW
    <service name> 为你添加的服务名，如果不传递服务名，默认为breakGFW
    sudo bfw start [service name]

    #监控VPN状态，掉线重连
    sudo bfw auto [service name]

    #停止
    sudo bfw stop [service name]

    #重启
    sudo bfw restart [service name]
    
    #添加域名
    #如果你确信某个域名的解析被污染或者解析的IP不正确，你可以通过该命令增加到系统中，让可靠的域名服务器来解析
    sudo bfw add domain <domain.com>

    #删除域名
    sudo bfw delete <domain.com>

    #查看域名列表
    bfw list domain

    #添加网站
    #有部分网站的DNS解析虽然被污染了，但是IP因为经常变化，没有被墙，在这种情况下，你可以添加该网站到系统中
    #breakGFW会解析域名对应的IP地址并增加到直连IP设置内，不需要经过VPN中转
    #增加、删除的网站不会修改该域名的解析方式
    sudo bfw add site <www.site.com>

    #删除网站
    sudo bfw delete site <www.site.com>

    #查看网站列表
    bfw list site

    #添加IP
    #和 add site 类似，对于一些私有IP，不会被墙，比如自己的个人网站IP，此时可以直接添加进系统避免VPN中转
    sudo add ip <ipv4 address>

    #删除IP
    sudo bfw delete ip <ipv4 address>

    #查看IP列表
    bfw list ip

    #添加路由
    #添加IP或者网络到路由表，避免经过VPN中转
    #参数为空时会添加天网IP段，自定义的IP地址到路由表
    sudo bfw add route [ipv4 address or net]

    #删除路由
    #参数为空时会从路由表中删除天网IP段，自定义的IP地址
    sudo bfw delete route [ipv4 address or net]

### 强烈推荐

    #为了良好的体验，强烈推荐添加自动启动并监控VPN状态，一劳永逸。
    echo "bfw start" | sudo tee -a /etc/rc.local
    echo "bfw auto" | sudo tee -a /etc/rc.local


版本支持
---
>因笔者使用Mac，故没有编写Linux和Windows版本，后续有必要的话，可考虑移植到Linux和Windows。

文件说明
---
  - bfw breakGFW主文件
  - resolver.py dns解析器文件
  - update_gfw_domain.sh 更新被墙域名，域名地址文件来源于autoproxy数据，建议定期更新
  - china_ipv4.lst 天网IP段，网络收集，据说来源于dnspod
  - gfw_domain.lst 被墙域名列表，由 update_gfw_domain.sh 生成
  - free_resolv.conf 国外域名解析服务器地址，每行一个IP地址
  - free_resolv.conf breakGFW在运行过程中探测到的国内dns解析服务器地址
  - china_resolv.conf 国内域名解析服务器地址，如若怀疑dns解析有问题或者受不了国内的404强奸解析，请手动设置DNS服务器为国外IP地址，每行一个IP地址。

后记
---
>不用的域名利用不用的nameserver来解析这个问题，本来在\*nix下有完美的解决办法:在/etc/resolver目录下增加不同的域名指示文件，但是Mac并没有使用\*nix内置的resolver，而使用的mDNSResponder又存在BUG，在添加多个域名指示文件后，即会出现无法解析dns的错误，故采取了自行编写域名解析器的方法。
>另外，自动连接vpn使用的是networksetup -connectpppoeservice，可是同系列的networksetup -disconnectpppoeservice却无法工作，真实相当的奇怪。望不吝赐教。

反馈
---
 - Bug：<https://github.com/puwaifu/breakGFW/issues>
 - Twitter: <http://twitter.com/puwaifu>
