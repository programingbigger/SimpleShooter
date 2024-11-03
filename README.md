# SIMPLESHOOTER

シンプルな横スクロールシューティングゲームです。プレイヤー操作の飛行機で、右から出現する敵機を撃墜しましょう！敵機に衝突するとゲームオーバーです。スコアは生存時間と撃墜数で計算されます。

## デモ動画
![デモ動画](https://github.com/user-attachments/assets/55b53418-fbea-4c79-92ec-195e477add8f)



## 操作方法

* I/J/K/Lキーまたは矢印キー：上下左右移動
* スペースキー：弾丸発射
* Pキー：一時停止/再開
* Qキー：ゲーム終了
* ゲームオーバー画面：
    * Rキー：ゲーム再開
    * Qキー：ゲーム終了

## インストール方法

1. リポジトリのクローンと移動
   ```bash
   git clone https://github.com/programingbigger/SimpleShooter.git
   ```

   ```
   cd SIMPLESHOOTER
   ```

2. 仮想環境の作成
   ```bash
   python3 -m venv .venv
   . .venv/bin/activate  # (Linux/macOS)
   .venv\Scripts\activate  # (Windows)
   ```

3. 必要なライブラリのインストール
   ```bash
   pip install -r requirements.txt
   ```

4. ゲームの実行
   ```bash
   python3 main.py
   ```

## ファイル構成

```
SIMPLESHOOTER/
├── game/
│   ├── components.py
│   └── images/
│       ├── airplane.png
│       ├── bullet.png
│       ├── cloud.png
│       └── enemy.png
├── main.py
├── README.md
├── requirements.txt
└── utils/
    └── config.py
```

* `SIMPLESHOOTER/`: プロジェクトルートディレクトリ
* `game/`: ゲームロジック関連のファイル
    * `components.py`: ゲームコンポーネント (飛行機、敵、弾丸など) の定義
    * `images/`: ゲームで使用する画像ファイル
* `main.py`: ゲームのメイン実行ファイル
* `README.md`: このファイル
* `requirements.txt`: 必要なPythonライブラリ一覧
* `utils/`: ユーティリティ関連のファイル
    * `config.py`: ゲームの設定ファイル

## ゲームの仕組み

* `StartView`: ゲーム開始画面
* `Shooter`: ゲームプレイ画面
    * 敵機と雲は一定間隔でランダムに出現
    * プレイヤーの移動範囲は画面内に制限
    * 衝突判定：プレイヤーと敵機、弾丸と敵機
    * スコア計算
* `GameOverView`: ゲームオーバー画面

## カスタマイズ

* `utils/config.py` でフォントやテキストを変更可能
* `game/images/` 内の画像ファイルを変更することで、見た目を変更可能
* `game/components.py` で敵機や雲の出現頻度、速度などを変更可能
