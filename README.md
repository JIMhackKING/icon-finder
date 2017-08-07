# iconfinder—爬取精美图标

[http://www.iconfinder.com](http://www.iconfinder.com "iconfinder")上有很多精美的图标，但是一张一张的保存很麻烦，当然网站上也可以下载一系列的图标，不过在他自带的下载方式下载的话只能一次下载一种尺寸的图标。<font color="#9933ff">iconfinder</font>这个脚本可以自动爬取指定系列、尺寸的图标，并分类保存在相应的文件夹中。

###configure.py

	# 要爬取的图标集
	urls = [
			"https://www.iconfinder.com/iconsets/3d-printing-6",
			"https://www.iconfinder.com/iconsets/ecology-33",
    		...
			]

	sizes = [48,64,128,256,512]  # 可选的图片尺寸

<font color="red">urls</font>指定了你要爬取的网页（图标集），对应的网页是这样的：

![screenshot](https://github.com/JIMhackKING/icon-finder/blob/master/screenshot.png)

<font color="red">sizes</font>指定了你想要爬取的图片尺寸（有其他可选的16，20，24，32）

###iconfinder.py

这个文件是爬虫的主程序

<font color="#CC6633">需要用到的库有</font>：

- requests
- bs4

首先定义常量，用于后面的网络请求

	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
			"referer":"https://www.iconfinder.com/",
			}

	s = requests.session() # Session对象

然后就是定义一个函数，在上图中一个图标集里面有许多个图标，这个函数的目的就是获取这个网页里面所有图标的链接

	def icon_links(url):
		req = s.get(url, headers=headers)
		soup = BeautifulSoup(req.text, "lxml")
		links = soup.find_all("a",{"class":"iconlink"})
		links = ["https://www.iconfinder.com"+i["href"] for i in links]  # 链接
		return links

返回的<font color="red">links</font>就是这个网页里面的链接

另一个函数<font color="red">save_img</font>作用是爬取不同尺寸的图标并保存在本地，该函数接受两个参数，<font color="red">title</font>是这些图标集的标题，用来以<font color="red">title</font>为名创建一个文件夹，我是以<font color="red">URL</font>作为标题的，第二个参数<font color="red">link</font>是图标集中的其中一个图标的链接。

	def save_img(title, link):
	
		header = headers.copy()  # 复制变量headers并改变referer
		header["referer"] = link
		req = s.get(link, headers=header, timeout=10)
		soup = BeautifulSoup(req.text, "lxml")
		img_link = soup.find("img", {"id":"detail-icon-img"})["src"]  # 图片链接
		# 根据不同尺寸改变URL
		for size in sizes:
			img_size_link = img_link.split("/")
			prev_size = re.match(".+?\-(\d+)\.\w+", img_size_link[-1]).group(1)
			img_size_link[-1] = img_size_link[-1].replace(prev_size, str(size))
			link = '/'.join(img_size_link)
	
			im = s.get(link, headers=header, timeout=10).content
	
			# 保存图片
			with open(title+"/"+img_size_link[-1],'wb') as f:
				f.write(im)

主要的函数完成了，最后一步就是运行，遍历<font color="red">urls</font>，然后传值进<font color="red">icon\_links</font>函数，之后再把返回值传进<font color="red">save\_image</font>函数就可以了