# pandas-re
Qiitaの記事用のソース置き場

# データの状態を確認する（行数列数カウント・データの選択的表示・重複の有無など）

df.shape()
df.index
df.columns
df.dtypes
df.loc[]
df.iloc[]
df.query()
df.unique()
df.drop_duplicates()
df.describe()

# データの整形（データ型変更、列名変更、並び替えなど）

df.set_index()
df.rename()
df.sort_values()
df.to_datetime()
df.sort_index()
df.resample()
df.apply()
pd.cut()

# データの欠損状態の確認

df.isnull()
df.any()

# 値（欠損）の置き換えや削除

df.fillna()
df.dropna()
df.replace()
df.mask()
df.drop()

# 集計

df.value_counts()
df.groupby()
df.diff()
df.rolling()
df.pct_change()

# 可視化

df.plot()
df.corr()
df.pivot()

# 変数の前処理
pd.get_dummies()
df.to_csv()
