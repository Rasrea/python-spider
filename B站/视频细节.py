import pandas as pd
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm


def scrape_labels(soup):
    all_data = soup.find_all('div', attrs={'class': 'tag not-btn-tag'})
    labels = [re.findall(r'target="_blank">(.*?)</a>', str(item)) for item in all_data]
    labels = [item[0] for item in labels if len(item) != 0]  # 去除空值
    labels = '/'.join(labels)  # 拼接
    return labels


def scrape_barrages(soup):
    barrages = soup.find('div', attrs={'class': 'dm-text'})
    if barrages is None:
        barrages = soup.find('span', attrs={'class': 'dm-count'})
        if barrages is None:
            return None
        return barrages.text.split()[-1].replace('弹幕', '')
    return barrages.text


def scrape_cur_time(soup):
    cur_time = soup.find('div', attrs={'class': 'pubdate-ip-text'})
    if cur_time is None:
        cur_time = soup.find('span', attrs={'class': 'pubdate-count'})
        if cur_time is None:
            return None
        return cur_time.text
    return cur_time.text


def scrape_summary(soup):
    summary = soup.find('span', attrs={'class': 'desc-info-text'})
    if summary is None:
        summary = soup.find('div', attrs={'class': 'video-desc open'})
        if summary is None:
            return None
    return summary.text.replace('\n', ' ')


def scrape_timelength(html):
    timelength = re.search(r'window\.__playinfo__=.*?"timelength":(\d+)', html, re.S)
    if timelength is None:
        return None
    return int(timelength.group(1)[:-3]) + 1


def scrape_up_url(soup):
    all_data = soup.find('div', attrs={'class': 'up-detail-top'})  # 搜索个人
    pattern = re.compile(r'<a.*?href="(.*?)".*?target="_blank">', re.S)
    up_url_ = re.search(pattern, str(all_data))
    if up_url_ is None:
        all_data = soup.find('div', attrs={'class': 'membersinfo-upcard'})  # 搜索团队
        up_url_ = re.search(pattern, str(all_data))
        if up_url_ is None:
            all_data = soup.find('div', attrs={'class': 'video-staffs-cover'})  # 搜索特殊
            up_url_ = re.search(pattern, str(all_data))
            if up_url_ is None:
                return None
    up_url = up_url_.group(1).strip()
    return 'https:' + up_url


async def fetch_url(session, url, headers):
    try:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            # 爬取网页详细信息
            return {
                '时长(秒)': scrape_timelength(html),
                '标签': scrape_labels(soup),
                '弹幕数': scrape_barrages(soup),
                '详细时间': scrape_cur_time(soup),
                'up网址': scrape_up_url(soup),
                '摘要': scrape_summary(soup)
            }
    except Exception as exc:
        print(f'{url} generated an exception: {exc}')
        return None


async def main(out_path, url_lst):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    # 保存信息
    dict_all_data = {'时长(秒)': [], '标签': [], '弹幕数': [], '详细时间': [], 'up网址': [], '摘要': []}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, headers) for url in url_lst]
        results = await tqdm.gather(*tasks, total=len(tasks))

    # 按顺序合并结果
    for result in results:
        if result:
            for key in dict_all_data:
                dict_all_data[key].append(result[key])

    # 保存为csv
    df = pd.DataFrame(dict_all_data)
    df.to_csv(out_path, index=False, encoding='utf-8-sig')
    print('运行完成！')


if __name__ == "__main__":
    output_path = r'd:\desktop\detail_data.csv'
    df = pd.read_csv(r"D:\DESKTOP\newbili.csv")
    url_lst = df['网站'].tolist()
    # print(url_lst)
    asyncio.run(main(output_path, url_lst))
