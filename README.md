2021/5/13  
0.0.0  
创建项目仓库，并写下第一行代码  

2021/5/20 18:03  
0.0.1  
0.0.1版正式上线了！！虽然什么功能都没实现，README也懒得写  

2021/5/26 21:36  
0.0.2  
实现了Console父类，把MetroConsole类改成了Console的子类，增强了MetroConsole的可读性和可拓展性，现在可以很轻松的实现两种权限的用户了。  

2021/5/27 11:08  
0.0.3  
修复了某些错误输入会导致程序异常终止的bug  

2021/5/27 15:28  
0.0.4  
新增了Admin权限下的创建文件/新增站点和线路/把站点添加到线路/保存文件的功能  
在过程中发现了一些可以改进的地方：  
1. 这些新增的操作在操作完成后应该提示操作成功
2. 把站点添加到线路这一操作失败时的提示太笼统
3. 如果没有修改，直接退出时不应该询问是否保存
4. 可以增加另存为功能
5. 增加数据文件的MD5校验，防止直接修改数据文件


将来的改进方向
1. 随着算法的进一步复杂（优化空间复杂度，考虑并行计算），可以考虑把图类的管理层和业务层也分成两个类
2. 加入日志和版本管理系统
3. 把图的计算结果也作为文件存下来
4. 加密？MD5？
5. 客户端和服务端
6. 加上前端开发，做成完整的项目
7. 装进容器内？
8. 可以把接口留好，但是不要过度设计！

flyod算法（带记录文件路径）
https://blog.csdn.net/weixin_39956356/article/details/80620667?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control

