import os
import subprocess
import sys
import ctypes
import urllib.request
import requests

# 配置项
ARIA2_PATH = "files/aria2c.exe"
A7Z_PATH = "files/7zr.exe"
UUP_CONV_PATH = "files/uup-converter-wimlib.7z"
ARIA2_SCRIPT_PATH = "files/aria2_script.txt"
DEST_DIR = "UUPs"
CONVERT_UUP_CMD = "convert-UUP.cmd"

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding='utf-8')

def check_admin():
    """检查是否具有管理员权限"""
    if os.name == 'nt':  # Windows
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception as e:
            print(f"检查管理员权限时发生错误: {e}")
            sys.exit(1)
        
        if not is_admin:
            print("此脚本需要以管理员身份运行。")
            sys.exit(1)
    else:
        print("仅支持 Windows 系统。")
        sys.exit(1)

def run_command(command, check=True):
    """运行命令并检查结果"""
    try:
        subprocess.run(command, check=check, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"命令失败：{e}")
        sys.exit(1)

def download_file(url, dest):
    """下载文件"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 使用 urlopen 发起请求
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            # 打开目标文件并写入响应内容
            with open(dest, 'wb') as f:
                f.write(response.read())
        print(f"文件下载成功：{dest}")
    except Exception as e:
        print(f"下载文件失败：{e}")
        sys.exit(1)

def extract_uup_converter():
    """提取UUP转换器"""
    if not os.path.exists(UUP_CONV_PATH):
        print(f"未找到文件 {UUP_CONV_PATH}")
        sys.exit(1)
    
    run_command(f'"{A7Z_PATH}" x -y "{UUP_CONV_PATH}"', check=True)

def get_latest_uuid():
    """获取最新的 UUID"""
    url = "https://api.uupdump.net/listid.php?search=26100&sortByDate=1"
    
    try:
        # 发起 GET 请求获取 JSON 数据
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，会抛出异常
        
        # 解析返回的 JSON 数据
        data = response.json()
        
        # 获取第一个最新的 build 信息
        builds = data.get("response", {}).get("builds", {})
        
        if builds:
            # 获取最新的 uuid
            latest_uuid = next(iter(builds.values())).get("uuid")
            return latest_uuid
        else:
            print("未找到最新的构建版本。")
            return None
    except requests.RequestException as e:
        print(f"获取数据时发生错误：{e}")
        return None

def download_aria2_script(url):
    """下载aria2脚本"""
    print("下载aria2脚本...")
    download_file(url, ARIA2_SCRIPT_PATH)
    print("下载完成")

def download_uup_set(uuid):
    """下载UUP文件集"""
    url = f"https://uupdump.net/get.php?id={uuid}&pack=zh-cn&edition=professional&aria2=2"
    download_aria2_script(url)
    
    print("下载UUP集...")
    run_command(f'"{ARIA2_PATH}" --no-conf --async-dns=false --console-log-level=warn --log-level=info --log="aria2_download.log" -x16 -s16 -j5 -c -R -d"{DEST_DIR}" -i"{ARIA2_SCRIPT_PATH}"')
    print("下载UUP集完成")

def download_apps(uuid):
    """下载Microsoft Store应用"""
    url = f"https://uupdump.net/get.php?id={uuid}&pack=neutral&edition=app&aria2=2"
    download_aria2_script(url)
    
    print("下载Microsoft Store应用...")
    run_command(f'"{ARIA2_PATH}" --no-conf --async-dns=false --console-log-level=warn --log-level=info --log="aria2_download.log" -x16 -s16 -j25 -c -R -d"{DEST_DIR}" -i"{ARIA2_SCRIPT_PATH}"')
    print("下载应用完成")

def convert_uup():
    """执行UUP转换"""
    if os.path.exists(CONVERT_UUP_CMD):
        print(f"执行 UUP 转换：{CONVERT_UUP_CMD}...")
        run_command(f'convert-UUP.cmd')
        print("UUP 转换完成！")
    else:
        print(f"未找到转换脚本 {CONVERT_UUP_CMD}，跳过转换步骤。")

def main():
    # 检查管理员权限
    check_admin()
    
    # 获取最新的UUID
    uuid = get_latest_uuid()
    if uuid:
        print(f"最新的 UUID 是: {uuid}")
    else:
        print("未能获取到 UUID，脚本将退出。")
        sys.exit(1)

    # 下载UUP转换器
    print("下载UUP转换器...")
    download_file("https://uupdump.net/misc/aria2c.exe", ARIA2_PATH)
    download_file("https://uupdump.net/misc/7zr.exe", A7Z_PATH)
    download_file("https://uupdump.net/misc/uup-converter-wimlib.7z", UUP_CONV_PATH)
    extract_uup_converter()

    # 下载UUP和Microsoft Store应用
    download_apps(uuid)
    download_uup_set(uuid)

    # 执行UUP转换
    convert_uup()

    print("所有操作完成！")

if __name__ == "__main__":
    main()
