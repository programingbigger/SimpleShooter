import json
import arcade

config = {
    "font_name": {
        "ja": "Hiragino Sans" # 日本語フォント
        , "en": "Kenney Pixel Square"   # 英語フォント
    }
    , "texts": {  # texts キーに変更
        "start_screen": {
            "title": "Shooters"
            , "instructions": [
                "Q: ゲームを終了します"
                , "P: ゲームを一時停止/一時停止解除します"
                , "I/J/K/L または 矢印キー: 上、左、下、右に移動します"
                , "SPACE: 弾丸を発射します"
                , "クリックしてゲーム開始"
            ]
            , "color" : arcade.color.WHITE
        },
        "game_over_screen": {
            "title": "Game Over"
            ,"instructions": [
                "R/rキーを押してゲームを再開します"
                ,"Q/qキーを押してゲームを終了します"
            ]
            , "color": arcade.color.WHITE
            
        }
    }
}
