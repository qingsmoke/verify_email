## 📖简介

**本程序只做学习用途，请勿非法用途**

作用：Python在线验证邮箱真实性，支持批量验证，支持全部域名邮箱

改了一个批量验证功能，Tzeross师傅的脚本地址：https://github.com/Tzeross/verifyemail

注意：在本机上使用会暴露你的本机IP，望知晓。（我怕到时候有些师傅没注意到这方面）

## 🚍使用

安装库命令：
pip install dnspython colorama

使用命令：
python verify_email.py 1.txt

![image-20240316214136389](C:\Users\刺客\AppData\Roaming\Typora\typora-user-images\image-20240316214136389.png)

## ⏰个人想说的话

使用 SMTP RCPT TO：返回250状态码，证明邮箱地址存在；返回550状态码，证明邮箱地址不存在。

注意：有些邮箱服务设置为**Catch-all**，这意味该域名下的每个邮箱地址，都会被认为是存在的。（Catch-all方面知识请师傅们自行学习)