# flyCat
## ——简单易用的IP代理池爬虫框架——
---
此程序从今年5月开始动手写，一直断断续续，没事儿的时候敲两下代码，终于在两个月以后出了一个并不完善的半成品。
#### 此程序独特的地方:
> 1. 用BeautifulSoup解析HTML，也可自定义，可根据不同的代理网站编写不同的解析方式.
 > 2. 只需要在spider.py文件中添加一个需要爬取的网站的方法，就能完成代理IP的爬取工作，每个方法相互独立，互不影响
 > 3. 占时没想到...
#### 目前还有待完善的地方：
> 1. 爬取后的代理IP没有进行有效性验证就直接保存。
> 2. 目前暂时只能保存为CSV文件，后续会加入MySQL，NoSQL等。
> 3. 日志文件以及出错以后的响应。
## 如何使用？
#### 当确定了需要爬取的代理网站以后，只需在spider.py文件里面添加一个爬取方法即可。
**例如我们爬取西刺：**
```python
    def xici():
    'http://www.xicidaili.com/nn/<1,20>'
    load = _plug.load('xici')
    allip = set()
    for html in load:  
        soup=_BeautifulSoup(html,'lxml')
        a=soup.find_all('td',class_='country')
        for b in a:
            l=[]
            for d in b.next_siblings:
                if d.string != '\n':
                    l.append(str(d.string))
            if l != []:
                result=_plug.ipMatch(l)
                if result:
                    allip.add(result)
    return allip
```
- 我们首选需要确定爬取的URL，这里面只需要将URL写到一行注释里面即可:
<1,20> 尖括号内表示起始页与总的翻页量，从第一页开始，往后+20页
```python
'http://www.xicidaili.com/nn/<1,20>'
```
- 然后我们需要调用spider_plug加载页面下载以后的缓存，这是必须的,_plug.load()内的参数与方法同名。
```python
load = _plug.load('xici')
```
- 最后返回的必须是一个set()
```python
allip = set()
```
- 用BeautifulSoup或者自定义方法解析出协议、IP以及端口号以后，统一调用_plug.ipMatch()进行IP地址验证及拼合。
```python
result=_plug.ipMatch(l)
```
### 编写spider方法特别需要注意：
> 1. spider.py文件中所有载入的模块，必须增加别名，别名必须加上"_"下划线，以便spider解析器进行过滤。
> 2. spider.py文件中的所有网页解析方法的名称，不能加上"_"下划线，以免被过滤掉。
> 3. 添加新的方法以后，可以用debug方法进行测试，例如新的方法为66ip，那么在paw实例化以后，不用start(),直接debug('66ip')
# 感谢各位大佬的阅读，文档与程序我还会逐步完善，Thanks！

- 2018-07-23 上传程序至GitHub....Version : 0.1.0 Beta
- 2018-07-25 spider新增66ip.cn、89ip.cn
- 2018-07-26 修复因连接超时抛出异常，程序终止问题。
             更新版本号 Version : 0.1.1 Beta
