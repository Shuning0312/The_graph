import requests
import pandas as pd

# GraphQL 端点 URL
url = 'https://api.studio.thegraph.com/query/80234/mirror/v1'


# 定义 GraphQL 查询模板
query = """
query getTransfers($skip: Int!, $first: Int!) {
  transfers(skip: $skip, first: $first, orderBy: value, orderDirection: desc) {
    id
    from
    to
    value
    blockNumber
    blockTimestamp
    transactionHash
  }
}
"""

def fetch_transfers(skip, first):
    response = requests.post(
        url,
        json={'query': query, 'variables': {'skip': skip, 'first': first}}
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {response.text}")

# 设置分页参数
first = 1000
skip = 0
all_transfers = []

while True:
    # 获取数据
    data = fetch_transfers(skip, first)
    transfers = data['data']['transfers']
    
    # 如果获取的数据少于请求的数量，说明已经获取到所有数据
    if len(transfers) < 1000:
        all_transfers.extend(transfers)
        break

    # 将数据添加到总列表中
    all_transfers.extend(transfers)

    # 更新skip以获取下一页数据
    skip += first

# # 打印获取到的所有转账事件
# for transfer in all_transfers:
#     print(f"ID: {transfer['id']}")
#     print(f"From: {transfer['from']}")
#     print(f"To: {transfer['to']}")
#     print(f"Value: {transfer['value']}")
#     print(f"Block Number: {transfer['blockNumber']}")
#     print(f"Block Timestamp: {transfer['blockTimestamp']}")
#     print(f"Transaction Hash: {transfer['transactionHash']}")
#     print("------------")

print(f"Total transfers fetched: {len(all_transfers)}")