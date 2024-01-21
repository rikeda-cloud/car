# 学習
* [ cd training ; py main.py ]にて学習用プログラムディレクトリへ移動し、プログラムを起動
* joystickのLB入力でデータ取得開始
* joystickのRB入力でデータ取得終了
* joystickのLT入力で一つ前に取得したデータを削除
* joystickのBボタンでアクセル、Aボタンでブレーキ、左のスティックで方向を入力
* データを取り終えたら[ py json_buffer.py ]にてAWSへ取得したデータを送信
* joystickの仕様としてmodeが2種類あり、起動してスティックを動かしているのにミニカーが動かない場合、MODEボタンを数回押し、緑に光らないようにする

# ストリーミング配信
* [cd training/streaming ; py streaming.py ]にてストリーミング配信用プログラムディレクトリへ移動し、ストリーミングサーバを立ち上げるプログラムを起動
* Webブラウザで[http://{raspiのipアドレス}:5000]にてストリーミングサーバにアクセスしてカメラ映像を確認
* streaming.pyのHaarLikeCameraクラスをBinarizationCameraクラスに変更し、コンストラクタ引数を削除すると２値化した配信に変更可能(デフォルトのカメラはハールライク特徴量の抽出で特徴量を抽出し、白黒差の大きい部分に黒い横線を描画している)

# 本番
* [ cd perfomance ; py main.py ]にて本番用プログラムディレクトリに移動し、プログラムを起動
* main.pyの[ if __name__ == "__main__" ]以降の部分でMiniCarクラスのインスタンス作成時に機械学習モデルのモデル名(機械学習モデルはperfomance/modelsディレクトリ内にあり、拡張子'.pkl'を外したモデル名を指定する)を指定すると使用するモデルを切り替えて自動運転することができる。
* 機械学習モデルの"c_d4_model_v1"はセンサー数を4つに絞る関係上、ProcessUltraSonicクラスのコンストラクタ引数にecho_pinとtrig_pinの指定をしないとエラーとなるため注意。
ex) ultrasonic = ProcessUltraSonic(pool_size=2, timeout=0.035, echo_pin=[15, 21, 31, 33], trig_pin=[16, 22, 32, 35])
* 新たに機械学習モデルを追加する際はget_perfomance_data.py内のGetPerfomanceDataクラスにデータを取得して学習モデルに使うパラメータをlistとして返すメソッドを記述し、determine_get_perfomance_dataメソッド内の_func_dict_for_modelディクトに['モデル名': モデルに対応したデータ取得メソッド]の形式で追加する。
