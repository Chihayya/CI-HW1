# 以 Q-Learning 模擬自走車

# 程式環境

Python 3.x 以上 / Numpy / Pygame 2.6.x 以上

# 使用方式

axis.py -> 描述二維運動
car.py -> 描述自走車在二維座標上的運動
playground.py -> 搭設自走車運行環境
q_learning.py -> 模型訓練
gui.py -> GUI 顯示模型動作

先在 軌道座標點.txt 輸入好座標後，運行 q_learning.py 得到訓練結果 q_table.pkl
運行 gui.py 觀察模型動作，決定要不要把 q_table.pkl 再訓練

# 執行檔說明

進入 /dist/gui.exe 執行前須注意該路徑下是否存在 已訓練後的 q_table.pkl 及 定義好的軌道座標點 
