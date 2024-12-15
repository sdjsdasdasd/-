import pandas as pd

# 读取Excel文件
file_path = 'OriginalData.xlsx'  # 请替换为你的文件路径
xls = pd.ExcelFile(file_path)

# 遍历每个工作表并处理
with pd.ExcelWriter('cleaned_data.xlsx') as writer:  # 新文件保存为 'cleaned_data.xlsx'
    for sheet_name in xls.sheet_names:
        # 读取工作表数据
        sheet_df = pd.read_excel(xls, sheet_name=sheet_name)

        # 检查是否包含 '充电前SOC' 列
        if '充电前SOC' in sheet_df.columns:
            # 删除充电前SOC大于0.95的行
            sheet_df = sheet_df[sheet_df['充电前SOC'] <= 0.95]

        # 将处理后的数据写入新的Excel文件
        sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

print("已删除充电前SOC大于0.95的行，并保存为 'cleaned_dataxlsx'.")
