import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from scipy.stats import gaussian_kde

# 设置字体为支持中文的字体
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 1. 从Excel加载所有工作表数据
file_path = 'classified.xlsx'  # 请替换为你的实际文件路径
xls = pd.ExcelFile(file_path)

# 初始化一个空的DataFrame用于合并所有工作表的数据`
total_df = pd.DataFrame()

# 2. 遍历所有工作表并提取“判定品牌”和“充电前SOC”列
for sheet_name in xls.sheet_names:
    sheet_df = pd.read_excel(xls, sheet_name=sheet_name)

    # 检查是否包含必要的列
    if '判定品牌' in sheet_df.columns and '充电前SOC' in sheet_df.columns:
        # 提取所需列并添加到总数据框中
        sheet_df = sheet_df[['判定品牌', '充电前SOC']]
        total_df = pd.concat([total_df, sheet_df], ignore_index=True)

# 3. 将品牌列转换为数字编码
total_df['品牌编码'] = total_df['判定品牌'].astype('category').cat.codes

# 4. 将数据根据品牌分组
brand_groups = total_df.groupby('判定品牌')['充电前SOC']

# 5. 绘制每种品牌的初始SOC的概率密度函数
plt.figure(figsize=(10, 6))

# 绘制每种品牌的KDE（核密度估计）图
for brand, group in brand_groups:
    sns.kdeplot(group, label=brand, fill=True, alpha=0.5)

# 添加标题和标签
plt.title('不同品牌初始SOC的概率密度函数', fontsize=16)
plt.xlabel('充电前SOC', fontsize=12)
plt.ylabel('概率密度', fontsize=12)

# 显示图例
plt.legend(title='品牌')

# 展示图表
plt.tight_layout()  # 自动调整布局
plt.show()

import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

# 初始化一个空的DataFrame用于保存所有品牌的密度信息
density_df = pd.DataFrame()

# 1. 遍历每个品牌
for brand, group in brand_groups:
    # 使用 gaussian_kde 进行核密度估计
    kde = gaussian_kde(group)

    # 创建一个范围用于计算密度
    x_range = np.linspace(group.min() - 1, group.max() + 1, 1000)  # 生成1000个点
    density_values = kde(x_range)  # 计算这些点的密度

    # 将结果添加到DataFrame
    brand_density_df = pd.DataFrame({
        '品牌': [brand] * len(x_range),
        'SOC': x_range,
        'Density': density_values
    })

    # 合并到总的密度表中
    density_df = pd.concat([density_df, brand_density_df], ignore_index=True)

