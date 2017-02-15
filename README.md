我们需要实现的功能就是在**惠惠购物助手**上面来获取优惠信息，然后把一条条的优惠信息存入mongo数据库，这就是我们本次的要达到的目的，我这里就是抛砖引玉，到时大家可以根据自己的喜好来抓取网络上面的内容。


###1. 实例化scrapy爬虫

 
&emsp;&emsp;我使用的是PyCharm来编写python的，我创建了一个叫"huihui"的工程，如果你安装了scrapy框架，那么可以直接在PyCharm的命令行控制台直接实例化scrapy工程。

```python
scrapy startproject huihui
```
    如果在PyCharm里面进行初始化这个还需要稍微调整一些目录，所以建议直接在命令行跳转到相应目录下进行初始化项目。最终我们会得到一个目录结构，这个目录结构在上篇我介绍的文章里面都有讲解，我在这里也做个笔记吧！
    
```python
    ├── scrapy.cfg
└── stack
    ├── __init__.py
    ├── items.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        └── __init__.py
```
&emsp;&emsp; 第一个scrapy.cfg是配置文件，我们基本是没有动这个文件，\__init__.py文件我们看看它自己的介绍就明白了，很明显这里是写一些关于爬虫的信息的。
```
# Please refer to the documentation for information on how to create and manage
# your spiders.
```

items.py文件就是我们的数据模型，按照MVC的编程思想就是mvc中得model。pipelines.py可以简单的理解是数据到数据库的“隧道”，有了这条隧道就可以让数据沿着这条隧道进入到数据库当中。settings.py我理解的就是一些全局的设置就在这里进行设置，就像它文件里面介绍的一样。
```
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
```
在spiders里面就真正放的是我们的“爬虫”了，在这里会对我们的爬虫进行编写。

###2. 编写爬虫

&emsp;&emsp;我们先需要在spiders文件夹里创建一个hui_spider.py的文件，在里面写我们的爬虫，然后导入相应的功能文件。
```
from scrapy import Spider
from scrapy.selector import Selector
```
然后我们huihui这个爬虫类继承自Spider类，并且初始化一些内容
```
class HuiSpider(Spider):
#实例化属性
    name = "huihui" #这是爬虫的名字
    allowed_domains = ["http://www.huihui.cn"] #这是爬虫活动活动的范围
    start_urls = [
        "http://www.huihui.cn/all?page=1",
    ] #爬虫起始的位置
```

接下来我们需要定义一个方法，这个方法是控制爬虫到底该如何去爬数据。
```
#爬虫方法
    def parse(self, response):
        #促销
        sales = Selector(response).xpath('//li[@class="hui-list-item1"]')
        print sales.extract() #输出调试
```

方法里面response是进行网络请求返回的response对象，我们请求的是一个网页，返回是一堆网页的源代码，我们可以在xpath里面进行筛选我们想要的数据。我们先看看网页大概是什么样子，并且使用谷歌浏览器查看源代码。
<P>
![](https://leanote.com/api/file/getImage?fileId=56acc83cab64416c540000f9)
<p>
可以从图上看出我们想要的内容就是li标签的内容，里标签里面有我们想要的内容。这里我们使用的是xpath的方法，可以通过查阅资料来了解xpath的语法的使用规则。
```
'//li[@class="hui-list-item1"]'
```
意思就是把这里面所有class为hui-list-item1的里li标签全部拿出来。

我们可以跑一跑看看效果，可以在命令行里面跑，我是直接在PyCharm的里面的命令行跑的。
```
scrapy crawl huihui(这里就写爬虫的名字，我这里是huihui，你们要写你们爬虫的名字)
```

查看输出的效果
![](https://leanote.com/api/file/getImage?fileId=56acc83cab64416c540000fa)
<p>
当你能看到这么多的html标签的时候就说明你成功了。那么我们已经完成一小步了，我们这一部分就结束了。接下来就是筛选数据，转成模型。
<p>

###3. 编写模型

&emsp;&emsp;打开我们的items.py文件，然后编写我们的数据模型，有过mvc编程经验这话，这里理解起来就超简单，几乎不用理解,模型里面的字段都是参考**惠惠购物助手**上面的内容进行获取的，我们把每一个这样的（如下图）消息列出来成为一个模型。
![](https://leanote.com/api/file/getImage?fileId=56acc83cab64416c540000fb)

代码如下：
```
import scrapy

from scrapy.item import Item,Field

class HuihuiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #标题
    title = Field()
    #图片
    imageURL = Field()
    #描叙
    detail = Field()
    #URL
    itemURL = Field()
    #来源
    itemfrom = Field()
    #热点
    hot = Field()
    pass

```

###4. 数据转模型

&emsp;&emsp;现在我们的模型也创建好了，我们接下来做的就是把我们读取的网页li标签里面的内容提取出来，我们还是会用到xpath语法，使用xpath语法提取相应的的字段传给model对象。在hui_spider.py文件中导入模型
```
#数据模型
from Huihui.items import HuihuiItem
```
然后在我们刚刚写parse方法里面提取我们要的标签内容，这里还是使用xpath方法来进行筛选，代码如下所示：
```
#爬虫方法
    def parse(self, response):
        #促销
        sales = Selector(response).xpath('//li[@class="hui-list-item1"]')
        titles = sales.xpath('//h3/a/text()').extract()
        imageURLs = sales.xpath('//div[@class="hlist-list-pic"]/a/img/@data-src').extract()
        details = sales.xpath('//div[@class="hui-content-text"]/p/text()').extract()
        itemURLs = sales.xpath('//h3/a/@href').extract()
        itemfroms = sales.xpath('//div[@class="list-shop"]/a/text()').extract()
        hots = sales.xpath('//h3/a/em/text()').extract()
```

我们在这里把我们想要的数据已经提取出来，接下来做的就是把实例化数据模型，然后把这些值给这个模型的对应属性。
```
#爬虫方法
    def parse(self, response):
        #促销
        sales = Selector(response).xpath('//li[@class="hui-list-item1"]')
        titles = sales.xpath('//h3/a/text()').extract()
        imageURLs = sales.xpath('//div[@class="hlist-list-pic"]/a/img/@data-src').extract()
        details = sales.xpath('//div[@class="hui-content-text"]/p/text()').extract()
        itemURLs = sales.xpath('//h3/a/@href').extract()
        itemfroms = sales.xpath('//div[@class="list-shop"]/a/text()').extract()
        hots = sales.xpath('//h3/a/em/text()').extract()

        for index in range(len(sales)):
            print "创建数据模型"
            item = HuihuiItem()

            item["title"] = titles[index]
            item["imageURL"] = imageURLs[index]
            item["detail"] = details[index]
            item["itemURL"] = itemURLs[index]
            item["itemfrom"] = itemfroms[index]
            item["hot"] = hots[index]

            yield item

        print '数据转模型完成'

```
在这个方法中，方法把一个个的被赋值模型作为参赛给返回出去，接下来就是拿到返出去的模型，然后把他们送进数据库。

###5. 存入数据库

&emsp;&emsp;在前面说了，我们需要建立起一条与数据库的通信的隧道，然后把我们的数据模型送进数据库，所以我们先要做的就是建立隧道。打开隧道控制文件pipelines.py,导入相应的功能文件
```
#导入系统设计，也就是刚刚我们设计的全局变量
from scrapy.conf import settings
#导入异常处理机制
from scrapy.exceptions import DropItem
#log功能
from scrapy import log
```
然后新建一个类，这个类就是我们的隧道，代码如下:
注意：在代码中大写字母字段是定义在settings里面的一些公共变量，定义这些公共变量以便代码的规范与复用，先贴出setting.py里面的代码：
```
#模型通道，定义在模型,里面的值是pipelines的位置
ITEM_PIPELINES = ['Huihui.pipelines.MongoDBPipeline',]
#服务器地址
MONGODB_SERVER = "localhost"
#服务器端口
MONGODB_PORT = 27017
#数据库名
MONGODB_DB = "Huihui"
#mongdb的（表）
MONGODB_COLLECTION = "sales"
```

pipelines.py文件里面的代码

```
class MongoDBPipeline(object):
    #初始化方法
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        #链接数据库
        db = connection[settings['MONGODB_DB']]
        if not db:
            print '数据库连接失败'
        #(表)
        self.collection = db[settings['MONGODB_COLLECTION']]
        if not self.collection:
            print 'collection获取失败'

    #链接数据库的通道
    def process_item(self, item, spider):

        valid = True
        for data in item:
            if not data:
                raise DropItem("数据库通道未接收到数据")
        #把数据录入数据库
        self.collection.insert(dict(item))
        log.msg("successful add!!!",level=log.DEBUG,spider=spider)

        return item

```

###6. 检查数据是否进入数据库

&emsp;&emsp;运行我们的爬虫
```
scrapy crawl huihui
```
如果顺利没有报错的话，那就打开我们的mongo数据库查看一下里面的数据，你可以直接使用命令行，也可以使用可视化工具，我这里使用的是就是Rebomongo，查看里面的数据如下图所示。
![](https://leanote.com/api/file/getImage?fileId=56acc83cab64416c540000fc)
<p>
可以看出来我们的数据已经成功的录入到数据库了。

## 结尾
&emsp;&emsp;至此，我们已经完成了自主获取数据的功能，这一步类似一般电商后台管理系统的功能，把一些顾客或者是商品的内容录入到系统当中。我们这里顶多是玩玩啦~好啦，这一部分就到此结束，祝你玩的愉快^_^
<p>
