import requests
from bs4 import BeautifulSoup
import time
import re
import os
import random
from configure import *

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
			"referer":"https://www.iconfinder.com/",
			}

s = requests.session()

def icon_links(url):
	req = s.get(url, headers=headers)
	soup = BeautifulSoup(req.text, "lxml")
	links = soup.find_all("a",{"class":"iconlink"})
	links = ["https://www.iconfinder.com"+i["href"] for i in links]  # 链接
	return links

# 保存不同大小的图片
def save_img(title, link):

	header = headers.copy()
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

		with open(title+"/"+img_size_link[-1],'wb') as f:
			f.write(im)

if __name__ == '__main__':
	for url in urls:
		title = url.split("/")[-1]
		if not os.path.exists(title):
			links = icon_links(url)
			os.mkdir(title)
			for index, link in enumerate(links):
				save_img(title, link)
				time.sleep(1+random.random())
				print(title, "第%d张图片" %(index+1))