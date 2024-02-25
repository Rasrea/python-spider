import requests
import re

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 '
}
base_url = 'https://ssr1.scrape.center'  # 原始网址


# 爬取相关内容，包括封面，名称，类别，上映时间，评分，剧情简介
def scrape_text(url):
    # 请求html
    html = requests.get(url, headers=headers).text

    # 封面
    cover_pattern = re.compile(r'class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    cover_url = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern,
                                                                             html) else None
    # 名称
    name_pattern = re.compile(r'<h2.*?>(.*?)</h2>', re.S)
    name_text = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern,
                                                                            html) else None
    # 类别，列表类型
    type_pattern = re.compile(r'category el-button.*?<span>(.*?)</span>', re.S)
    type_text = re.findall(type_pattern, html) if re.search(type_pattern,
                                                            html) else None
    # 上映时间
    time_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}).*?上映', re.S)
    time_text = re.search(time_pattern, html).group(1).strip() if re.search(time_pattern,
                                                                            html) else None
    # 评分
    score_pattern = re.compile(r'class="score.*?>(.*?)</p>', re.S)
    score_text = re.search(score_pattern, html).group(1).strip() if re.search(score_pattern,
                                                                              html) else None
    # 剧情简介
    ele_pattern = re.compile(r'<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    ele_text = re.search(ele_pattern, html).group(1).strip() if re.search(ele_pattern,
                                                                          html) else None

    # 以字典的格式返回
    print( {
        'cover': cover_url,
        'name': name_text,
        'type': type_text,
        'time': time_text,
        'score': score_text,
        'element': ele_text
    })


# 爬取电影详细链接
def scrape_url(url):
    html = requests.get(url).text
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')  # 详细网址后缀
    t_url = re.findall(pattern, html)
    for item in t_url:
        detail_url = f'{base_url}{item}'  # 组合成详细网址

        scrape_text(detail_url)  # 爬取相关内容


# 主函数
def main():
    for page in range(1, 11 + 1):
        index_url = f'{base_url}/page/{page}'  # 获取所有列表网站
        scrape_url(index_url)  # 获取电影的详细网站


if __name__ == '__main__':
    main()
