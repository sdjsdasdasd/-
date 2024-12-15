import pandas as pd
from datetime import datetime, timedelta

# 读取Excel文件
input_file = 'OriginalData.xlsx'  # 替换为您的文件名
output_file = '充电时段分组.xlsx'

# 假设工作表名称为 "Sheet1"，并且第一列是“充电开始时间”
df = pd.read_excel(input_file, sheet_name="Sheet1")

# 将“充电开始时间”转换为datetime格式
df['充电开始时间'] = pd.to_datetime(df['充电开始时间'])

# 添加新列，用于标记时间区间
df['区间日期'] = df['充电开始时间'].apply(
    lambda x: (
        x.date() if x.time() >= datetime.strptime("18:00:00", "%H:%M:%S").time() else x.date() - timedelta(days=1)
    )
)

# 按夜间区间日期分组
grouped = df.groupby('区间日期')

# 创建Excel文件并保存到各工作表
with pd.ExcelWriter(output_file) as writer:
    for date, group in grouped:
        group.sort_values("充电开始时间", inplace=True)  # 按时间排序
        group.to_excel(writer, sheet_name=str(date), index=False)

print(f"处理完成！已保存到文件：{output_file}")
