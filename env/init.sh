# "chmod 777 init.sh ; source ./init.sh"で実行
# 終了時は"deactivete"コマンドで終了
python3 -m venv car_env
source car_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
