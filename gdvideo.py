import requests
import urllib3
import time
import hashlib

# 禁用 HTTPS 证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 全局基础配置
HOST = "https://gdypt.rf.hangzhou.gov.cn:9443"
BASE_URL = f"{HOST}/ginkgo/system-api/system/videoStudy/data"
LOGIN_URL = f"{HOST}/ginkgo/system-api/system/auth/passwd-login"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
}

def login(username, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    payload = {
        "username": username,
        "password": hashed_password,
        "type": "mobile"
    }
    
    login_headers = HEADERS.copy()
    
    try:
        r = requests.post(LOGIN_URL, headers=login_headers, json=payload, verify=False, timeout=10)
        res_json = r.json()
        
        if res_json.get("success"):
            access_token = res_json.get("data", {}).get("accessToken")
            print(f"登录成功！(*ﾟ∀ﾟ*)")
            return access_token
        else:
            print(f"登录失败: {res_json.get('message')}")
            return None
    except Exception as e:
        print(f"登录请求异常: {e}")
        return None

def hack_video(video_id, auth_token):
    action_headers = HEADERS.copy()
    action_headers["Content-Type"] = "application/x-www-form-urlencoded"
    action_headers["Authorization"] = f"Bearer {auth_token}"

    try:
        watch_data = {"id": str(video_id)}
        r1 = requests.post(f"{BASE_URL}/watchVideo", headers=action_headers, data=watch_data, verify=False, timeout=10)
        
        res_json = r1.json()
        if not res_json.get("success"):
            print(f"视频 {video_id} watchVideo 请求失败: {res_json.get('message')}")
            return False
        
        record_id = res_json.get("data") 
        
        finish_data = {"id": str(record_id)}
        r2 = requests.post(f"{BASE_URL}/finishStudy", headers=action_headers, data=finish_data, verify=False, timeout=10)
        
        finish_json = r2.json()
        if finish_json.get("success"):
            return True
        else:
            print(f"[-] 视频 {video_id} finishStudy 失败: {finish_json.get('message')}")
            return False
            
    except Exception as e:
        print(f"[-] 视频 {video_id} 请求异常: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("让我们开始刷课吧,Ciallo~(∠・ω )⌒☆")
    print("="*50)
    
    # 账号配置
    USERNAME = input("请输入账号(´・ω・`):")
    PASSWORD = input("请输入密码(つω⊂):")
    
    # 执行登录
    token = login(USERNAME, PASSWORD)
    
    if not token:
        print("未能获取 Token,程序退出。")
        exit()
        
    try:
        start_id = input("请输入开始id (默认为6): ")
        start_id = int(start_id) if start_id != "" else 6
        
        count = input("请输入想刷课的数量 (默认为100): ")
        count = int(count) if count != "" else 100
        end_id = start_id + count
    except ValueError:
        print("输入错误：请输入数字")
        exit()
    
    success_count = 0
    
    # 执行刷课
    for vid in range(start_id, end_id + 1):
        print(f"\r正在处理视频 ID: {vid} (进度: {success_count + 1}/{count})", end="", flush=True)
        
        if hack_video(vid, token):
            success_count += 1
            
        # 防封禁延迟
        time.sleep(0.5) 
        
    print("\n")
    print(f"刷课完成！共成功刷完 {success_count}/{count} 个视频(∩^o^)⊃━☆ﾟ.*･｡")