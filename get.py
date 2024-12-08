import requests
import os

def get_latest_uuid():
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
            print("No builds found.")
            return None
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_uuid_to_file(uuid):
    # 将 uuid 写入临时文件
    with open("uuid.txt", "w") as file:
        file.write(uuid)
    print(f"UUID saved to uuid.txt: {uuid}")

if __name__ == "__main__":
    uuid = get_latest_uuid()
    if uuid:
        print(f"The latest UUID is: {uuid}")
        save_uuid_to_file(uuid)
    else:
        print("Failed to retrieve the UUID.")
