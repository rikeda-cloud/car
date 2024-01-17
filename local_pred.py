import time

def execution_speed(func):
    """
    実行速度計測用のデコレータ
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("実行時間" + str(run_time) + "秒")
    return wrapper

@execution_speed
def predict_lgm(model, df):
    #予測の実行と書き出し
    for i in range(0, 100):
        pred = model.predict(df)
        print(pred)


import pickle
import pandas as pd
# カレントディレクトリにあるモデルデータの読み込み
model = pickle.load(open('model.pkl', 'rb'))


# 予測
data_list =[531.0,522.0,513.0,509.0,513.0,495.0,495.0,490.0,486.0,486.0,477.0,468.0,468.0,472.0,454.0,450.0,450.0,440.0,440.0,427.0,422.0,422.0,413.0,413.0,404.0,404.0,395.0,404.0,390.0,377.0,377.0,368.0,390.0,359.0,359.0,372.0,390.0,363.0,336.0,331.0,734.0,2742.0,566.0,1272.0,892.0,785.0,4000.0,1128.0,723.0,508.0]
# print(len(data_list))
df = pd.DataFrame(data_list)
df = df.T
predict_lgm(model, df)
# print(df)
# df = pd.read_csv("train_split.csv", header=None, encoding="utf-8")
# df = df.drop(df.columns[[0]], axis=1)
# x = pd.read_csv('522.0,513.0,509.0,509.0,504.0,504.0,504.0,500.0,500.0,500.0,495.0,495.0,554.0,486.0,554.0,486.0,486.0,486.0,486.0,486.0,486.0,477.0,477.0,540.0,477.0,477.0,468.0,468.0,468.0,468.0,463.0,459.0,459.0,459.0,459.0,454.0,454.0,472.0,450.0,490.0,545.0,402.0,401.0,3282.0,743.0,773.0,4000.0,665.0,624.0,643.0')
# print(len(model.feature_importance()))

