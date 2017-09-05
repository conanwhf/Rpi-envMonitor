# Rpi-envMonitor
A small family environment monitor system, base on Python3.
树莓派搭建的一个家用小型的环境检测系统，从传感器获取环境状态，包括温度，湿度，照度，空气质量等。系统分为两种状态：监控和日常，监控状态所有数据1秒更新一次，日常状态则每10分钟更新一次传感器数据并上报。

- [x] 使用DHT111获取温度和湿度
- [x] 使用传感器获取PM2.5和PM10数据
- [x] 使用PCF8591获取照度
- [x] 获取系统运行状态，包括CPU温度和Loading，内存和磁盘使用，外网IP，网络连接，运行时间等
- [x] 通过GPIO自动控制背光和传感器电源，以减少硬件过度使用的损耗
- [ ] 数据保存至本地数据库
- [x] 屏幕显示数据
- [x] 空气质量恶化时红灯报警
- [x] 上报状态至yeelink


对于DHT22，需要装官方库**Adafruit_Python_DHT**，且使用pip安装失败。安装步骤如下：
	
	git clone https://github.com/adafruit/Adafruit_Python_DHT.git
	cd Adafruit_Python_DHT
	sudo python3 setup.py install