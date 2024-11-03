import arcade
import random
import arcade.key
from game.components import FlyingSprite
from game.components import Bullet
from utils.config import config

# 初期変数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "SimpoleShooter"
SCALING = 0.1
FONT_ENGLISH = config["font_name"]["en"]
FONT_JAPANESE = config["font_name"]["ja"]

class StartView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Shooters"
                        , SCREEN_WIDTH / 2
                        , SCREEN_HEIGHT / 2 + 100
                        ,arcade.color.BLACK
                        , font_size=50
                        , anchor_x="center"
                        , font_name = FONT_ENGLISH)
# 説明文を描画 (複数行対応)
        instructions = [
            "Q: ゲームを終了します",
            "P: ゲームを一時停止/一時停止解除します",
            "I/J/K/L または 矢印キー: 上、左、下、右に移動します",
            "SPACE: 弾丸を発射します",
            "クリックしてゲーム開始"
        ]
        y_position = SCREEN_HEIGHT / 2 - 30
        for line in instructions:
            arcade.draw_text(line
                            , SCREEN_WIDTH / 2
                            , y_position
                            , arcade.color.BLACK
                            , font_size=15
                            , anchor_x="center"
                            , font_name=FONT_JAPANESE)
            y_position -= 30

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Shooter()
        game_view.setup()
        self.window.show_view(game_view)

class Shooter(arcade.View):
    """
    横スクロール型のスペースシューターゲーム

    プレイヤーは左側に開始位置があり、敵は右側から出現します。
    プレイヤーは画面外に出ない限り、自由に移動できます。
    敵は様々な速度で左へ飛行します。
    衝突するとゲームオーバーになります。
    """
    def __init__(self, height=SCREEN_HEIGHT, width=SCREEN_WIDTH):
        super().__init__()
        self.enemies_list = arcade.SpriteList()  # 敵のスプライトリスト
        self.clouds_list = arcade.SpriteList()  # 雲のスプライトリスト
        self.all_sprites = arcade.SpriteList()  # 全てのスプライトリスト
        self.bullets_list = arcade.SpriteList() # 弾丸リストの作成
        self.paused = False
        
        self.height = height
        self.width = width
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        self.player = arcade.Sprite("images/airplane.png", SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10 # スプライトの左端をウィンドウの左端から数ピクセル離して配置することで、スプライトの x 位置を設定
        self.all_sprites.append(self.player)
        
        # スプライトが出てくるスパン
        arcade.schedule(self.add_enemy, 0.25)
        arcade.schedule(self.add_cloud, 0.5)
    
    # 敵ユニットの作成
    def add_enemy(self, delta_time: float):
        enemy = FlyingSprite("images/enemy.png", SCALING*2)

        # 位置をランダムな高さに設定し、画面右外へ
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)
        enemy.velocity = (random.randint(-7, -3), random.randint(-1, 1)) # 敵の速度
        
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)
    
    # 雲の作成
    def add_cloud(self, delta_time: float):
        # cloudの定義
        cloud = FlyingSprite("images/cloud.png", SCALING*2.3)
        cloud.center_x = random.randint(80, self.width)
        cloud.center_y = random.randint(self.height-500, self.height)
        cloud.velocity = (random.randint(-3, -2), 0)
        
        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)
    
    # 弾丸の作成
    def shoot_bullet(self):
        """弾丸を発射する"""
        bullet = Bullet("images/bullet.png", SCALING)
        bullet.center_y = self.player.center_y # playerのY座標の位置から射出される
        bullet.velocity = (10, 0)
        
        # add list
        self.bullets_list.append(bullet)
        self.all_sprites.append(bullet)
    
    def on_key_press(self, symbol:int, modifiers:int):
        """
        Q: ゲームを終了します
        P: ゲームを一時停止/一時停止解除します
        I/J/K/L: 上、左、下、右に移動します
        矢印キー: 上、左、下、右に移動します
        SPACE: 弾丸を発射します

        引数:
            symbol {int} -- どのキーが押されたか
            modifiers {int} -- どの修飾キーが押されたか
        """
        
        if symbol == arcade.key.Q:
            print("predd Q key")
            arcade.close_window()
        
        if symbol == arcade.key.P:
            self.paused = not self.paused
        
        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = 5

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -5

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 5
        
        if symbol == arcade.key.SPACE:
            self.shoot_bullet()
    
    def on_key_release(self, symbol:int, modifiers:int):
        """
        移動キーが離されたときに移動ベクトルを元に戻します
        引数:
            symbol {int} -- どのキーが押されたか
            modifiers {int} -- どの修飾キーが押されたか
        """
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0
        
        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0
        
    def on_update(self, delta_time):
        """
        Spliteオブジェクトを更新する
        ただし、一時停止している場合は、何もしない
        引数:
            delta_time {float} -- 最後の更新からの経過時間
        """
        
        # もし、pausedがTrueだったら、ゲームをアップデートしない
        if self.paused:
            return
        
        # 敵と衝突したら、ゲームオーバー画面に移動
        if self.player.collides_with_list(self.enemies_list):
            print("敵と衝突しました。")
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)
        
        # bulletで敵を倒したら、敵とbulletが消える
        for bullet in self.bullets_list:
            # spriteとspritelistが同じ座標に来たかどうかを判定する
            hit_enemies = arcade.check_for_collision_with_list(bullet, self.enemies_list)
            for enemy in hit_enemies:
                bullet.remove_from_sprite_lists()
                enemy.remove_from_sprite_lists()
        
        self.all_sprites.update()
        
        # プレイヤーが画面外から出ないようにする設定
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0
    
    def on_draw(self):
        """ゲーム画面を描画する"""
        arcade.start_render()  # 描画を開始
        self.all_sprites.draw()  # 全てのスプライトを描画

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
    
    def on_draw(self):
        self.clear()
        """
        "Game over"を画面に描画します。
        """
        arcade.draw_text("Game Over"
                , SCREEN_WIDTH / 2
                , SCREEN_HEIGHT / 2 + 100
                ,arcade.color.BLACK
                , font_size=50
                , anchor_x="center"
                , font_name = FONT_ENGLISH)
        
        instructions = [
            "R/rキーを押してゲームを再開します",
            "Q/qキーを押してゲームを終了します",
        ]
        y_position = SCREEN_HEIGHT / 2 - 50
        for line in instructions:
            arcade.draw_text(line
                            , SCREEN_WIDTH / 2
                            , y_position
                            , arcade.color.WHITE
                            , 24
                            , anchor_x="center"
                            , font_name=FONT_JAPANESE)
            y_position -= 40

    def on_key_release(self, symbol:int, modifiers:int):
        """
        R/rキーを押すとゲーム再開
        Q/qキーを押すと画面が閉じる
        """
        if symbol == arcade.key.Q:
            print("predd Q key")
            print("ゲーム終了")
            arcade.exit()

        if symbol == arcade.key.R:
            print("press R key")
            print("ゲーム再開")
            game_view = Shooter()
            game_view.setup()
            self.window.show_view(game_view)

def main():
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
