import json
import os
import random
import time
import ctypes
import urllib.parse
from datetime import datetime
from typing import List, Dict, Generator
import httpx
from random import uniform
from playwright.async_api import async_playwright
import asyncio
from urllib.parse import urlencode, quote

# 从help.py复制的lookup表
lookup = [
    "Z", "m", "s", "e", "r", "b", "B", "o", "H", "Q", "t", "N", "P", "+", "w", "O",
    "c", "z", "a", "/", "L", "p", "n", "g", "G", "8", "y", "J", "q", "4", "2", "K",
    "W", "Y", "j", "0", "D", "S", "I", "k", "3", "V", "x", "T", "f", "i", "l", "d",
    "U", "A", "F", "M", "9", "7", "h", "E", "C", "v", "u", "R", "X", "5", "1", "6"
]

def tripletToBase64(e):
    """三元组转base64"""
    return (
        lookup[63 & (e >> 18)] +
        lookup[63 & (e >> 12)] +
        lookup[(e >> 6) & 63] +
        lookup[e & 63]
    )

def encodeChunk(e, t, r):
    """编码数据块"""
    m = []
    for b in range(t, r, 3):
        n = (16711680 & (e[b] << 16)) + \
            ((e[b + 1] << 8) & 65280) + (e[b + 2] & 255)
        m.append(tripletToBase64(n))
    return ''.join(m)

def b64Encode(e):
    """自定义base64编码"""
    P = len(e)
    W = P % 3
    U = []
    z = 16383
    H = 0
    Z = P - W
    
    while H < Z:
        U.append(encodeChunk(e, H, Z if H + z > Z else H + z))
        H += z
        
    if W == 1:
        F = e[P - 1]
        U.append(lookup[F >> 2] + lookup[(F << 4) & 63] + "==")
    elif W == 2:
        F = (e[P - 2] << 8) + e[P - 1]
        U.append(lookup[F >> 10] + lookup[63 & (F >> 4)] + lookup[(F << 2) & 63] + "=")
        
    return "".join(U)

def encodeUtf8(e):
    """UTF-8编码"""
    b = []
    m = urllib.parse.quote(e, safe='~()*!.\'')
    w = 0
    while w < len(m):
        T = m[w]
        if T == "%":
            E = m[w + 1] + m[w + 2]
            S = int(E, 16)
            b.append(S)
            w += 2
        else:
            b.append(ord(T[0]))
        w += 1
    return b

def get_b3_trace_id():
    """生成b3 trace id"""
    re = "abcdef0123456789"
    je = 16
    e = ""
    for t in range(16):
        e += re[random.randint(0, je - 1)]
    return e

def mrc(e):
    """签名算法的一部分"""
    # 从help.py复制完整的ie数组
    ie = [
        0, 1996959894, 3993919788, 2567524794, 124634137, 1886057615, 3915621685,
        2657392035, 249268274, 2044508324, 3772115230, 2547177864, 162941995,
        2125561021, 3887607047, 2428444049, 498536548, 1789927666, 4089016648,
        2227061214, 450548861, 1843258603, 4107580753, 2211677639, 325883990,
        1684777152, 4251122042, 2321926636, 335633487, 1661365465, 4195302755,
        2366115317, 997073096, 1281953886, 3579855332, 2724688242, 1006888145,
        1258607687, 3524101629, 2768942443, 901097722, 1119000684, 3686517206,
        2898065728, 853044451, 1172266101, 3705015759, 2882616665, 651767980,
        1373503546, 3369554304, 3218104598, 565507253, 1454621731, 3485111705,
        3099436303, 671266974, 1594198024, 3322730930, 2970347812, 795835527,
        1483230225, 3244367275, 3060149565, 1994146192, 31158534, 2563907772,
        4023717930, 1907459465, 112637215, 2680153253, 3904427059, 2013776290,
        251722036, 2517215374, 3775830040, 2137656763, 141376813, 2439277719,
        3865271297, 1802195444, 476864866, 2238001368, 4066508878, 1812370925,
        453092731, 2181625025, 4111451223, 1706088902, 314042704, 2344532202,
        4240017532, 1658658271, 366619977, 2362670323, 4224994405, 1303535960,
        984961486, 2747007092, 3569037538, 1256170817, 1037604311, 2765210733,
        3554079995, 1131014506, 879679996, 2909243462, 3663771856, 1141124467,
        855842277, 2852801631, 3708648649, 1342533948, 654459306, 3188396048,
        3373015174, 1466479909, 544179635, 3110523913, 3462522015, 1591671054,
        702138776, 2966460450, 3352799412, 1504918807, 783551873, 3082640443,
        3233442989, 3988292384, 2596254646, 62317068, 1957810842, 3939845945,
        2647816111, 81470997, 1943803523, 3814918930, 2489596804, 225274430,
        2053790376, 3826175755, 2466906013, 167816743, 2097651377, 4027552580,
        2265490386, 503444072, 1762050814, 4150417245, 2154129355, 426522225,
        1852507879, 4275313526, 2312317920, 282753626, 1742555852, 4189708143,
        2394877945, 397917763, 1622183637, 3604390888, 2714866558, 953729732,
        1340076626, 3518719985, 2797360999, 1068828381, 1219638859, 3624741850,
        2936675148, 906185462, 1090812512, 3747672003, 2825379669, 829329135,
        1181335161, 3412177804, 3160834842, 628085408, 1382605366, 3423369109,
        3138078467, 570562233, 1426400815, 3317316542, 2998733608, 733239954,
        1555261956, 3268935591, 3050360625, 752459403, 1541320221, 2607071920,
        3965973030, 1969922972, 40735498, 2617837225, 3943577151, 1913087877,
        83908371, 2512341634, 3803740692, 2075208622, 213261112, 2463272603,
        3855990285, 2094854071, 198958881, 2262029012, 4057260610, 1759359992,
        534414190, 2176718541, 4139329115, 1873836001, 414664567, 2282248934,
        4279200368, 1711684554, 285281116, 2405801727, 4167216745, 1634467795,
        376229701, 2685067896, 3608007406, 1308918612, 956543938, 2808555105,
        3495958263, 1231636301, 1047427035, 2932959818, 3654703836, 1088359270,
        936918000, 2847714899, 3736837829, 1202900863, 817233897, 3183342108,
        3401237130, 1404277552, 615818150, 3134207493, 3453421203, 1423857449,
        601450431, 3009837614, 3294710456, 1567103746, 711928724, 3020668471,
        3272380065, 1510334235, 755167117
    ]
    
    o = -1
    
    def right_without_sign(num: int, bit: int=0) -> int:
        val = ctypes.c_uint32(num).value >> bit
        MAX32INT = 4294967295
        return (val + (MAX32INT + 1)) % (2 * (MAX32INT + 1)) - MAX32INT - 1
    
    for n in range(len(e)):
        o = ie[(o & 255) ^ ord(e[n])] ^ right_without_sign(o, 8)
    return o ^ -1 ^ 3988292384

def sign(a1="", b1="", x_s="", x_t=""):
    """生成签名"""
    common = {
        "s0": 3,
        "s1": "",
        "x0": "1",
        "x1": "3.7.8-2",
        "x2": "Mac OS",
        "x3": "xhs-pc-web",
        "x4": "4.27.2",
        "x5": a1,
        "x6": x_t,
        "x7": x_s,
        "x8": b1,
        "x9": mrc(x_t + x_s + b1),
        "x10": 154,
    }
    encode_str = encodeUtf8(json.dumps(common, separators=(',', ':')))
    x_s_common = b64Encode(encode_str)
    x_b3_traceid = get_b3_trace_id()
    return {
        "x-s": x_s,
        "x-t": x_t,
        "x-s-common": x_s_common,
        "x-b3-traceid": x_b3_traceid
    }

class RedTalk:
    def __init__(self, cookie=None, proxy=None):
        """初始化RedTalk类"""
        self.headers = {
            'authority': 'www.xiaohongshu.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'origin': 'https://www.xiaohongshu.com',
            'referer': 'https://www.xiaohongshu.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'x-s': '',
            'x-t': '',
            'x-s-common': ''
        }
        
        # 基础cookie
        self.cookies = {
            'xsecappid': 'xhs-pc-web',
            'webBuild': '3.7.8',
            'websectiga': 'b31c3c5272f15b0cca8887e187b4c1a53f872c4267bc2e8f96988a2e451926f6',
            'web_session': '040069b0b3079d5826df071c84354b2c81c605'
        }
        
        # 合并传入的cookie
        if cookie:
            self.cookies.update(cookie)
        
        self.max_notes = 25  # 每个关键词最多收集20个笔记
        self.max_comments_per_note = 50  # 每个笔记最多收集50个高赞评论
        self.hot_comment_min_likes = 88  # 评论最少点赞数
        self.min_reply_count = 30  # 评论最少回复数
        self.data_dir = "hot_comments"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.proxy = proxy
        self.client = httpx.AsyncClient(
            cookies=self.cookies,
            headers=self.headers,
            timeout=30.0,
            follow_redirects=True,
            proxy=self.proxy if self.proxy else None
        )
        self.request_interval = (1, 2)  # 请求间隔范围(秒)
        self.max_retries = 3  # 最大重试次数
        self.retry_interval = 1  # 重试间隔(秒)

    async def _sign_request(self, method: str, url: str, data=None):
        """签名请求"""
        # 这里添加签名逻辑
        # 从red_craw的help.py中获取签名算法
        pass

    async def _sleep_random(self):
        """随机休眠一段时间"""
        await asyncio.sleep(random.uniform(*self.request_interval))

    async def request(self, method: str, url: str, **kwargs) -> dict:
        """发送请求"""
        for retry in range(self.max_retries):
            try:
                # 1. 获取签名
                sign_headers = await self._get_sign(method, url, kwargs.get("params") or kwargs.get("json"))
                headers = kwargs.pop("headers", {})
                headers.update(sign_headers)
                kwargs["headers"] = headers
                
                print(f"[DEBUG] 发送请求: {method} {url}")
                print(f"[DEBUG] 请求参数: {kwargs.get('params')}")
                print(f"[DEBUG] 请求头: {headers}")
                
                # 2. 发送请求
                async with httpx.AsyncClient(
                    cookies=self.cookies,
                    follow_redirects=True,
                    timeout=20,
                    verify=False,
                    proxy=self.proxy if self.proxy else None
                ) as client:
                    response = await client.request(method, url, **kwargs)
                    print(f"[DEBUG] 响应状态码: {response.status_code}")
                    print(f"[DEBUG] 响应头: {dict(response.headers)}")
                    print(f"[DEBUG] 响应内容: {response.text[:1000]}")  # 只打印前1000个字符
                    
                    response.raise_for_status()
                    await self._sleep_random()
                    return response.json()
                
            except Exception as e:
                if retry == self.max_retries - 1:
                    print(f"[ERROR] 请求失败: {str(e)}")
                    print(f"[ERROR] 错误类型: {type(e)}")
                    import traceback
                    print(f"[ERROR] 详细错误信息:\n{traceback.format_exc()}")
                    return {}
                print(f"[WARN] 请求失败，正在重试({retry + 1}/{self.max_retries}): {str(e)}")
                await asyncio.sleep(self.retry_interval)

    async def _get_sign(self, method: str, url: str, data: dict = None) -> dict:
        """获取签名"""
        try:
            # 1. 获取当前时间戳
            x_t = str(int(time.time() * 1000))
            
            # 2. 处理URL，只保留路径部分
            path = url.replace("https://www.xiaohongshu.com", "")
            
            # 3. 构造签名数据
            sign_data = {
                "url": path,
                "method": method.upper(),
                "data": data if data else {},
                "headers": {
                    "x-t": x_t,
                }
            }
            
            # 4. 生成签名字符串
            sign_str = json.dumps(sign_data, separators=(',', ':'))
            sign_bytes = encodeUtf8(sign_str)
            x_s = b64Encode(sign_bytes)
            
            # 5. 获取其他必要参数
            a1 = self.cookies.get('a1', '')
            web_session = self.cookies.get('web_session', '')
            
            # 6. 生成x-s-common
            common = {
                "s0": 2,
                "s1": web_session,
                "x0": 1,
                "x1": "3.7.8",
                "x2": "Windows",
                "x3": "xhs-pc-web",
                "x4": "4.27.2",
                "x5": a1,
                "x6": x_t,
                "x7": x_s,
                "x8": "",
                "x9": mrc(x_t + x_s),
                "x10": 154
            }
            
            # 7. 编码x-s-common
            common_str = json.dumps(common, separators=(',', ':'))
            common_bytes = encodeUtf8(common_str)
            x_s_common = b64Encode(common_bytes)
            
            # 8. 生成trace_id
            x_b3_traceid = get_b3_trace_id()
            
            # 9. 返回完整签名
            return {
                "x-s": x_s,
                "x-t": x_t,
                "x-s-common": x_s_common,
                "x-b3-traceid": x_b3_traceid
            }
            
        except Exception as e:
            print(f"[ERROR] 生成签名失败: {str(e)}")
            return {
                "x-s": "",
                "x-t": x_t,
                "x-s-common": "",
                "x-b3-traceid": get_b3_trace_id()
            }

    async def search_notes(self, keyword: str):
        """搜索笔记"""
        url = 'https://edith.xiaohongshu.com/api/sns/web/v1/search/notes'
        page = 1
        has_more = True
        note_count = 0
        
        while has_more and note_count < 50:
            params = {
                'keyword': keyword,
                'page': page,
                'page_size': 20,
                'search_id': self.get_search_id(),
                'sort': 'general',
                'note_type': 0,
                'ext_flags': [],
                'image_formats': ['jpg', 'webp', 'avif']
            }
            
            try:
                print(f"\n[DEBUG] 开始搜索第 {page} 页 (已获取{note_count}条笔记)")
                data = await self.request('POST', url, json=params)
                
                if not data:
                    print("[ERROR] 请求返回空数据")
                    return
                
                if data.get('code') != 0:  # 修改：检查code而不是success
                    print(f"[ERROR] 搜索失败: {data.get('msg', '未知错误')}")
                    return
                    
                items = data.get('data', {}).get('items', [])
                valid_notes = [item for item in items if item.get('model_type') == 'note']
                print(f"[INFO] 获取到第 {page} 页，{len(valid_notes)} 条有效笔记")
                
                # 筛选热门笔记
                for item in valid_notes:
                    if note_count >= 50:
                        print("[INFO] 已达到50条笔记上限")
                        return
                        
                    note_card = item.get('note_card', {})
                    # 修改：将字符串转换为整数
                    like_count = int(note_card.get('interact_info', {}).get('liked_count', '0'))
                    
                    # 只返回点赞数超过1000的笔记
                    if like_count >= 1000:
                        note_count += 1
                        note_info = {
                            'id': item.get('id'),
                            'title': note_card.get('display_title'),
                            'like_count': like_count,
                            'user': note_card.get('user', {}).get('nickname'),
                            'user_id': note_card.get('user', {}).get('user_id'),
                            'cover_url': note_card.get('cover', {}).get('url_default'),
                            'type': note_card.get('type'),
                            'xsec_token': item.get('xsec_token')  # 可能需要用于后续请求
                        }
                        print(f"[INFO] 找到第{note_count}个热门笔记: {note_info['title']} (点赞数: {like_count})")
                        yield note_info
                
                has_more = data.get('data', {}).get('has_more', False)
                page += 1
                
                if has_more:
                    await asyncio.sleep(random.uniform(1, 2))
                    
            except Exception as e:
                print(f"[ERROR] 搜索笔记出错: {str(e)}")
                print(f"[ERROR] 错误类型: {type(e)}")
                import traceback
                print(f"[ERROR] 详细错误信息:\n{traceback.format_exc()}")
                return

    def get_search_id(self) -> str:
        """生成搜索ID"""
        e = int(time.time() * 1000) << 64
        t = int(uniform(0, 2147483646))
        return self._base36encode((e + t))

    def _base36encode(self, number: int) -> str:
        """将整数转换为base36字符串"""
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        base36 = ''
        while number:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36
        return base36 or alphabet[0]

    async def get_note_comments(self, note_id: str, xsec_token: str):
        """获取笔记评论"""
        url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page'
        cursor = ''
        has_more = True
        api_call_count = 0
        MAX_API_CALLS = 10  # 最多调用10次接口
        
        # 记录频率限制次数
        rate_limit_count = 0
        MAX_RATE_LIMITS = 3  # 最多允许3次频率限制
        
        while has_more and api_call_count < MAX_API_CALLS:
            try:
                params = {
                    'note_id': note_id,
                    'cursor': cursor,
                    'top_comment_id': '',
                    'image_formats': 'jpg,webp,avif',
                    'xsec_token': xsec_token
                }
                
                # 基础延迟：3-5秒
                base_delay = random.uniform(3, 5)
                # 随机增加0-2秒的额外延迟，模拟人类行为
                extra_delay = random.uniform(0, 2) if random.random() < 0.3 else 0
                await asyncio.sleep(base_delay + extra_delay)
                
                print(f"\n[DEBUG] 开始获取评论，第{api_call_count + 1}次调用，cursor: {cursor}")
                data = await self.request('GET', url, params=params)
                api_call_count += 1
                
                if not data:
                    print("[ERROR] 请求返回空数据")
                    continue
                    
                if data.get('code') == 300013:  # 访问频率异常
                    rate_limit_count += 1
                    if rate_limit_count >= MAX_RATE_LIMITS:
                        print("[ERROR] 频繁访问受限，建议稍后再试")
                        return
                    
                    # 计算递增的等待时间：15-25秒，且每次触发都增加
                    wait_time = random.uniform(15, 25) * (1 + rate_limit_count * 0.5)
                    print(f"[WARN] 访问太快啦，休息一下... ({int(wait_time)}秒)")
                    await asyncio.sleep(wait_time)
                    continue
                    
                # 成功获取数据，重置频率限制计数
                rate_limit_count = 0
                
                if data.get('code') != 0:
                    print(f"[ERROR] 获取评论失败: {data.get('msg', '未知错误')}")
                    return
                
                comments = data.get('data', {}).get('comments', [])
                print(f"[INFO] 获取到 {len(comments)} 条评论")
                
                for comment in comments:
                    # 解析主评论数据
                    like_count = int(comment.get('like_count', '0'))
                    reply_count = int(comment.get('sub_comment_count', '0'))
                    
                    # 筛选高质量评论 - 满足任一条件即可
                    if like_count >= self.hot_comment_min_likes or reply_count >= self.min_reply_count:
                        comment_info = {
                            'id': comment.get('id'),
                            'content': comment.get('content', ''),
                            'like_count': like_count,
                            'reply_count': reply_count,
                            'create_time': comment.get('create_time', ''),
                            'status': comment.get('status'),
                            'show_tags': comment.get('show_tags', []),
                            'user_info': {
                                'user_id': comment.get('user_info', {}).get('user_id'),
                                'nickname': comment.get('user_info', {}).get('nickname'),
                                'image': comment.get('user_info', {}).get('image')
                            },
                            'pictures': [pic.get('url_default') for pic in comment.get('pictures', [])]
                        }
                        yield comment_info
                        
                        # 获取子评论中的高赞评论
                        for sub_comment in comment.get('sub_comments', []):
                            sub_like_count = int(sub_comment.get('like_count', '0'))
                            if sub_like_count >= self.hot_comment_min_likes:  # 子评论只看点赞数
                                sub_comment_info = {
                                    'id': sub_comment.get('id'),
                                    'content': sub_comment.get('content', ''),
                                    'like_count': sub_like_count,
                                    'create_time': sub_comment.get('create_time', ''),
                                    'status': sub_comment.get('status'),
                                    'show_tags': sub_comment.get('show_tags', []),
                                    'user_info': {
                                        'user_id': sub_comment.get('user_info', {}).get('user_id'),
                                        'nickname': sub_comment.get('user_info', {}).get('nickname'),
                                        'image': sub_comment.get('user_info', {}).get('image')
                                    },
                                    'pictures': [pic.get('url_default') for pic in sub_comment.get('pictures', [])],
                                    'parent_id': comment.get('id')
                                }
                                yield sub_comment_info
                
                cursor = data.get('data', {}).get('cursor', '')
                has_more = data.get('data', {}).get('has_more', False)
                
                if has_more:
                    # 页面间增加更自然的随机延迟：2-6秒
                    page_delay = random.uniform(2, 4)
                    # 30%概率增加额外延迟
                    if random.random() < 0.3:
                        page_delay += random.uniform(1, 2)
                    await asyncio.sleep(page_delay)
                    
            except Exception as e:
                print(f"[ERROR] 获取评论出错: {str(e)}")
                return  # 遇到其他错误直接返回，避免无效重试

    async def save_note_comments(self, keyword: str, note_id: str, note_title: str, comments: List[Dict]):
        """保存笔记评论到对应关键词的JSON文件"""
        if not comments:  # 如果没有高赞评论，直接返回
            return
            
        try:
            # 使用关键词作为文件名
            filename = f"{self.data_dir}/{keyword}.json"
            filename = "".join(x for x in filename if x.isalnum() or x in ('_', '-', '/', '.'))
            
            # 读取现有数据（如果文件存在）
            data = {}
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    print(f"[WARN] 文件 {filename} 格式错误，将重新创建")
            
            # 添加新的笔记数据
            data[note_id] = {
                'title': note_title,
                'crawl_time': datetime.now().strftime('%Y%m%d_%H%M%S'),
                'comments': comments
            }
            
            # 确保目录存在
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # 保存更新后的数据
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print(f"[INFO] 已更新关键词'{keyword}'的数据文件，添加笔记《{note_title[:20]}...》的{len(comments)}条评论")
        except Exception as e:
            print(f"[ERROR] 保存评论数据时出错: {str(e)}")

    async def collect_hot_comments(self, keywords_list: List[str]):
        """收集高赞评论主函数"""
        for keyword in keywords_list:
            note_count = 0
            print(f"\n处理关键词: {keyword}")
            
            try:
                async for note in self.search_notes(keyword):
                    if note_count >= self.max_notes:
                        break
                        
                    note_count += 1
                    print(f"\n[INFO] 正在处理第{note_count}个笔记: {note['title'][:30]}...")
                    
                    # 获取到笔记后，模拟人类阅读行为
                    read_time = random.uniform(8, 15)  # 模拟阅读笔记的时间：8-15秒
                    print(f"[INFO] 阅读笔记中... ({int(read_time)}秒)")
                    await asyncio.sleep(read_time)
                    
                    # 70%概率增加一个额外的停顿，模拟看图片或思考
                    if random.random() < 0.7:
                        extra_time = random.uniform(3, 7)
                        print(f"[INFO] 查看图片中... ({int(extra_time)}秒)")
                        await asyncio.sleep(extra_time)
                    
                    xsec_token = note.get('xsec_token')
                    if not xsec_token:
                        print(f"[WARN] 笔记缺少xsec_token，跳过")
                        continue
                    
                    # 收集单个笔记的评论
                    note_comments = []
                    comment_count = 0
                    
                    # 进入评论区前再等待一下
                    pre_comment_time = random.uniform(2, 5)
                    print(f"[INFO] 正在进入评论区... ({int(pre_comment_time)}秒)")
                    await asyncio.sleep(pre_comment_time)
                    
                    async for comment in self.get_note_comments(note['id'], xsec_token):
                        if comment_count >= self.max_comments_per_note:
                            print(f"[INFO] 已达到单个笔记评论收集上限({self.max_comments_per_note}条)")
                            break
                            
                        hot_comment = {
                            'comment_id': comment.get('id'),
                            'content': comment.get('content', ''),
                            'like_count': comment.get('like_count', 0),
                            'reply_count': comment.get('reply_count', 0),
                            'user_name': comment.get('user_info', {}).get('nickname', ''),
                            'create_time': comment.get('create_time', ''),
                            'pictures': comment.get('pictures', [])
                        }
                        note_comments.append(hot_comment)
                        comment_count += 1
                        print(f"[INFO] 找到第{comment_count}个热门评论: {hot_comment['content'][:30]}... (点赞: {hot_comment['like_count']})")
                    
                    # 每处理完一个笔记就更新数据文件
                    if note_comments:
                        await self.save_note_comments(keyword, note['id'], note['title'], note_comments)
                    else:
                        print(f"[INFO] 该笔记未找到符合条件的高赞评论")
                    
                    # 每处理完3-5个笔记后，模拟一个较长的休息
                    if note_count % random.randint(3, 5) == 0:
                        rest_time = random.uniform(20, 30)
                        print(f"[INFO] 休息一下... ({int(rest_time)}秒)")
                        await asyncio.sleep(rest_time)
                
            except Exception as e:
                print(f"[ERROR] 处理关键词 {keyword} 时发生错误: {str(e)}")
                await asyncio.sleep(15)  # 出错后等待15秒
                continue

    async def login(self):
        """登录并获取必要的cookie"""
        try:
            print("[INFO] 开始登录流程...")
            
            # 使用 playwright 打开浏览器
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)  # 设置为有头模式
                context = await browser.new_context()
                page = await context.new_page()
                
                # 访问搜索页面
                url = f"https://www.xiaohongshu.com/search_result?keyword=火锅"
                print(f"[INFO] 正在访问页面: {url}")
                await page.goto(url)
                
                # 等待用户手动处理验证码
                print("[INFO] 请在浏览器中完成验证...")
                await page.wait_for_selector('.feeds-container', timeout=60000)  # 等待搜索结果出现
                
                # 获取所有 cookies
                cookies = await context.cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                print("[DEBUG] 获取到的cookies:", cookie_dict)
                
                # 更新 cookies
                self.cookies.update(cookie_dict)
                
                # 关闭浏览器
                await browser.close()
                
                print("[INFO] 登录成功")
                return True
                
        except Exception as e:
            print(f"[ERROR] 登录过程出错: {str(e)}")
            print(f"[ERROR] 错误类型: {type(e)}")
            import traceback
            print(f"[ERROR] 详细错误信息:\n{traceback.format_exc()}")
            return False

    async def _refresh_cookies(self):
        """刷新cookie"""
        try:
            url = "https://www.xiaohongshu.com/web_api/sns/v1/system_service/config"
            data = await self.request("GET", url)
            
            if data.get("success"):
                print("[DEBUG] 成功刷新cookie")
                return True
            
        except Exception as e:
            print(f"[ERROR] 刷新cookie失败: {str(e)}")
            return False

async def extract_comments_to_txt():
    """从所有JSON文件中提取评论并保存为TXT"""
    data_dir = "hot_comments"
    try:
        # 获取hot_comments目录下的所有json文件
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        if not json_files:
            print("[INFO] 没有找到JSON文件")
            return
            
        # 创建输出文件
        output_file = "all_comments.txt"
        comment_count = 0
        all_comments = []  # 用于存储所有评论
        
        # 收集所有评论
        for json_file in json_files:
            file_path = os.path.join(data_dir, json_file)
            keyword = json_file.replace('.json', '')  # 获取关键词
            print(f"[INFO] 正在处理关键词'{keyword}'的文件")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
                    
                # 遍历每个笔记
                for note_id, note_data in data.items():
                    note_title = note_data.get('title', '未知标题')
                    comments = note_data.get('comments', [])
                    
                    # 遍历笔记中的评论
                    for comment in comments:
                        content = comment.get('content', '').strip()
                        if content:  # 只保存非空评论
                            like_count = comment.get('like_count', 0)
                            all_comments.append({
                                'content': content,
                                'like_count': like_count,
                                'keyword': keyword,
                                'note_title': note_title
                            })
                            
            except Exception as e:
                print(f"[ERROR] 处理文件 {json_file} 时出错: {str(e)}")
                continue
        
        # 按点赞数排序
        all_comments.sort(key=lambda x: x['like_count'], reverse=True)
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, comment in enumerate(all_comments, 1):
                f.write(f"{idx}. {comment['content']} (点赞数: {comment['like_count']}, 来自: {comment['keyword']}-{comment['note_title'][:20]}...)\n")
                comment_count += 1
        
        print(f"[SUCCESS] 已提取并排序 {comment_count} 条评论到 {output_file}")
        
    except Exception as e:
        print(f"[ERROR] 提取评论时出错: {str(e)}")

async def main():
    """主函数"""
    try:
        # 初始化浏览器
        async with async_playwright() as p:
            # 启动浏览器，设置为有头模式
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            print("[INFO] 正在访问小红书...")
            await page.goto("https://www.xiaohongshu.com")
            
            # 等待用户手动处理验证码和登录
            print("[INFO] 请在浏览器中完成验证码验证和登录...")
            print("[INFO] 登录完成后请按回车键继续...")
            
            # 等待用户输入
            await asyncio.get_event_loop().run_in_executor(None, input)
            
            try:
                print("[INFO] 正在获取cookies...")
                # 获取cookies
                cookies = await context.cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                print("[DEBUG] 获取到的cookies:", cookie_dict)
                
                # 初始化RedTalk
                red_talk = RedTalk(cookie=cookie_dict)
                
                # 开始搜索和收集评论
                keywords = ["怎么选", "避雷", "平替", "学生党", "职场通勤", "露营"]
                print("[INFO] 开始收集评论数据...")
                await red_talk.collect_hot_comments(keywords)
                print("[INFO] 数据收集完成")
                
            except Exception as e:
                print(f"[ERROR] 操作过程出错: {str(e)}")
                raise
            finally:
                # 完成后关闭浏览器
                print("[INFO] 正在关闭浏览器...")
                await browser.close()
            
    except Exception as e:
        print(f"[ERROR] 程序执行出错: {str(e)}")
        print(f"[ERROR] 错误类型: {type(e)}")
        import traceback
        print(f"[ERROR] 详细错误信息:\n{traceback.format_exc()}")

if __name__ == "__main__":
    # 确保安装了必要的依赖：pip install playwright
    # 安装浏览器驱动：playwright install chromium
    print("[INFO] 程序启动...")
    asyncio.run(main())
    print("[INFO] 程序结束")

    # 可以单独运行这个函数来提取评论
    # asyncio.run(extract_comments_to_txt()) 