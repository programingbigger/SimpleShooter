import arcade

# 初期変数
SCREEN_WIDTH = 800

# 弾丸用のスプライト
class Bullet(arcade.Sprite):
    def update(self):
        """
        画面外に出たら削除
        """
        super().update()
        if self.left > SCREEN_WIDTH:
            self.remove_from_sprite_lists()

# 敵や雲などの設定をするスプライト
class FlyingSprite(arcade.Sprite):
    def update(self):
        """スプライトの位置を更新する
        画面外に移動したら削除する
        """
        # Move the sprite
        super().update()
        # 画面外を外れたら、spliteのリストから削除する。これをすることによって、メモリを削減できる
        if self.right < 0:
            self.remove_from_sprite_lists()