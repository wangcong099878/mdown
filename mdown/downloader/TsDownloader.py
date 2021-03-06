import requests
from downloader.Downloader import Downloader


class TsDownloader(Downloader):
    """
    下载ts文件的下载器
    """

    def __init__(self, url: str, path: str, num: int, parentDownloader: Downloader, timeout: int = 5,
                 noSuffix: bool = True):
        self.url = url
        self.path = path
        self.num = num
        self.parentDownloader = parentDownloader
        self.timeout = timeout
        self.noSuffix = noSuffix
        self.filename = str(num)
        if not self.noSuffix:
            self.filename += '.ts'
        pass

    def download(self):
        i = 0
        # 如果请求失败就重新请求，直至请求成功
        while True:
            try:
                resp = requests.get(url=self.url, timeout=self.timeout)
                with open(self.path + '/' + self.filename, "wb") as f:
                    for data in resp.iter_content(1024):
                        self.parentDownloader.lock.acquire()
                        self.parentDownloader.dataPerInterval += len(data)
                        self.parentDownloader.lock.release()
                        f.write(data)
                    pass
                self.parentDownloader.lock.acquire()
                self.parentDownloader.completeNum += 1
                self.parentDownloader.lock.release()
                break
                pass
            except requests.exceptions.RequestException:
                i += 1
                pass
            pass
        pass
        pass

    pass
