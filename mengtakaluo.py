import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import gaussian_kde

# 设置字体为支持中文的字体
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 1. 从Excel加载所有工作表数据
file_path = 'OriginalData.xlsx'  # 请替换为你的实际文件路径
xls = pd.ExcelFile(file_path)

# 初始化一个空的DataFrame用于合并所有工作表的数据
total_df = pd.DataFrame()

# 2. 遍历所有工作表并提取“判定品牌”和“充电前SOC”列
for sheet_name in xls.sheet_names:
    sheet_df = pd.read_excel(xls, sheet_name=sheet_name)

    # 检查是否包含必要的列
    if '判定品牌' in sheet_df.columns and '充电前SOC' in sheet_df.columns:
        # 提取所需列并添加到总数据框中
        sheet_df = sheet_df[['判定品牌', '充电前SOC']]
        total_df = pd.concat([total_df, sheet_df], ignore_index=True)

# 3. 将数据根据品牌分组
brand_groups = total_df.groupby('判定品牌')['充电前SOC']

# 4. 使用核密度估计（KDE）进行蒙特卡洛抽样
n_samples = 1000  # 设置蒙特卡洛抽样的样本数量

# 存储每个品牌的样本数据
sampled_data = []

for brand, group in brand_groups:
    # 使用Gaussian KDE拟合SOC数据
    kde = gaussian_kde(group)

    # 从KDE分布中抽取样本
    samples = kde.resample(n_samples)[0]

    # 将抽取的样本数据存储到列表中，添加品牌信息
    brand_samples = pd.DataFrame({
        '判定品牌': [brand] * n_samples,
        '充电前SOC': samples
    })
    sampled_data.append(brand_samples)

    # 绘制每个品牌的SOC分布与抽样结果
    plt.figure(figsize=(10, 6))
    sns.kdeplot(group, label=f'原始数据 ({brand})', fill=True, alpha=0.5)
    plt.hist(samples, bins=30, density=True, alpha=0.6, label=f'蒙特卡洛抽样结果 ({brand})')
    plt.title(f'{brand} 核密度估计与蒙特卡洛抽样', fontsize=16)
    plt.xlabel('充电前SOC', fontsize=12)
    plt.ylabel('概率密度', fontsize=12)
    plt.legend()
    plt.show()

# 将抽样数据合并成一个DataFrame
sampled_df = pd.concat(sampled_data, ignore_index=True)

# 输出抽样结果到Excel
output_file = 'sampled_data_output.xlsx'  # 设置输出文件路径
sampled_df.to_excel(output_file, index=False)

print(f"蒙特卡洛抽样结果已成功输出到 {output_file}")
