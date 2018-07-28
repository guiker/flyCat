# flyCat Beta版
## ——简单易用的IP代理池爬虫框架——
---
此程序从今年5月开始动手写，一直断断续续，没事儿的时候敲两下代码，终于在两个月以后出了一个并不完善的半成品。
## 所需要的模板
- 1、BeautifulSoup - 如果修改spider.py的解析规则，此模板非必须。
- 2、SQLite3 - 用于存储数据，后期将会加入更多存储方式
- 3、 urllib
## 如何使用？
> #### 1、常规抓取
**我们以爬取西刺为例**
我们需要打开flyCat目录下的spider.py文件，在当中添加一个需要爬取的方法
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
                result=_plug.ip_match(l)
                if result:
                    allip.add(result)
    return allip
```
- 我们首选需要确定爬取的URL，这里面只需要将URL写到一行注释里面即可,
<1,20> 尖括号内表示起始页与总的翻页量，从第1页开始，往后+20页。
```python
'http://www.xicidaili.com/nn/<1,20>'
```
- 然后我们需要调用spider_plug加载页面下载以后的缓存，这是必须的,_plug.load()内的参数与方法同名。
```python
load = _plug.load('xici')
```
- 我们需要实例化一个set()，用于最后的return
```python
allip = set()
```
- 我们打开西刺的HTML代码，找到代理IP所在的位置
```html
 <tr class="">
    <td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>
    <td>121.31.192.157</td>
    <td>8123</td>
    <td>广西桂林</td>
    <td class="country">高匿</td>
    <td>HTTP</td>
      <td>880天</td>
    <td>5分钟前</td>
  </tr>
```
- 我们需要将<td>标签内的内容解析到一个list，格式为：
```python
l = ['121.31.192.157','8123','广西桂林','高匿','HTTP','880天','5分钟前']
```
- 我们不用管多余的数据，将结果赋值给_plug.ip_match()方法:
```python
result=_plug.ip_match(l)
```
- 最终得到的结果是一个tuple：
```python
result = ('http':'121.31.192.157:8123')
```
- 最后我们将result添加到allip，有的<td>标签的内容可能会不匹配代理IP的要求，此时_plug.ip_match会返回False，我们需要先判断result不为False，在添加到allip。
```python
if result:
    allip.add(result)
```
- 最后直接将结果return
```python
return allip
```
- 我们打开示例程序go.py，实例化paw类
```python
import flyCat
paw = new flyCatpaw()
```
- 我们可以先调用debug()方法，对抓取进行测试：
```python
debug('xici')
```
*这里需要注意，debug()方法不会将抓取到的数据保存到本地，只讲结果打印到屏幕，为了快速调试，建议在调试的时候不要采用翻页功能：
```python
'http://www.xicidaili.com/nn/<1,20>'
# 将此行注释更改为如下，只用抓取一页进行测试，数据抓取成功以后再根据需求添加翻页。
'http://www.xicidaili.com/nn/1'
```
- 抓取测试完成以后，直接运行start()开始工作
```python
paw.start()
```
> #### 2、是用IP代理访问代理网站进行抓取
- 可以在Paw()实例化的时候，将需要使用的代理IP传入
> #### 3、代理IP有效性测试
- 可以直接独立运行ping()
 ```python
    import flyCat.proxy_test as test
    test.ping()
 ```
### 此程序独特的地方:
> 1. 用BeautifulSoup解析HTML，也可自定义，可根据不同的代理网站编写不同的解析方式.
 > 2. 只需要在spider.py文件中添加一个需要爬取的网站的方法，就能完成代理IP的爬取工作，每个方法相互独立，互不影响。
 > 3. 每一个代理IP存储到数据库以后，都分配了5分的状态，每一次验证不通过则减1分，知道分数为0后进行删除。
 > 4. 暂时还没想到...
#### 目前还有待完善的地方：
> 1. shell自动化代码
> 2. 目前保存数据为SQLite，代码还有待优化
> 3. 日志文件以及出错以后的响应。
### 编写spider方法特别需要注意：
> 1. spider.py文件中所有载入的模块，必须增加别名，别名必须加上"_"下划线，以便spider解析器进行过滤。
> 2. spider.py文件中的所有网页解析方法的名称，不能加上"_"下划线，以免被过滤掉。
> 3. 添加新的方法以后，可以用debug方法进行测试，例如新的方法为66ip，那么在paw实例化以后，不用start(),直接debug('66ip')
# 感谢各位大佬的阅读，文档与程序我还会逐步完善，Thanks！

- 2018-07-23 上传程序至GitHub....Version : 0.1.0 Beta
- 2018-07-25 spider新增66ip.cn、89ip.cn
- 2018-07-26 修复因连接超时抛出异常，程序终止问题。部分完善README文档。Version : 0.1.1 Beta
- 2018-07-28 更改数据存储方式，从csv更改为SQLite，增加代理IP有效性验证功能。Version : 0.1.2 Beta
