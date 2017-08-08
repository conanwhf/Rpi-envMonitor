# Rpi-envMonitor
A small family environment monitor system, base on Python3.
树莓派搭建的一个家用小型的环境检测系统。系统分为两种状态：监控和日常，监控状态所有数据1秒更新一次，日常状态则每10分钟更新一次传感器数据并上报。

- [x] 从传感器获取环境状态，包括温度，湿度，照度，空气质量等
- [x] 获取系统运行状态，包括CPU温度和Loading，内存使用，外网IP，网络连接，运行时间等
- [ ] 数据保存至本地数据库
- [ ] 屏幕显示数据
- [ ] 空气质量恶化时报警
- [ ] 上报状态至yeelink
