import arcade
import random

import arcade.key
import arcade.key

# 初期変数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Simpole game"
SCALING = 0.1

"""
オブジェクトを表示させたい場合は、splitelistを作成して、
on_updateとon_drawの関数を定義し、run関数で実行する
↓
on_update ⇨ on_drawが繰り返される
"""

class FlyingSprite(arcade.Sprite):
    """すべての飛行スプライトの基本クラス
    飛行スプライトには、敵と雲が含まれます
    """

    def update(self):
        """スプライトの位置を更新する
        画面外に移動したら削除する
        """

        # Move the sprite
        super().update()

        # 画面外を外れたら、spliteのリストから削除する。これをすることによって、メモリを削減できる
        if self.right < 0:
            self.remove_from_sprite_lists()
            


# 弾丸用のスプライト
class Bullet(arcade.Sprite):
    def update(self):
        """
        画面外に出たら削除
        """
        super().update()
        if self.left > SCREEN_WIDTH: # 画面のleft⇨x軸だから、bulletのx軸が一番端のスクリーンから出たら、そのスプライトを削除する
            self.remove_from_sprite_lists()

class SpaceShoter(arcade.Window):
    """
    横スクロール型のスペースシューターゲーム

    プレイヤーは左側に開始位置があり、敵は右側から出現します。
    プレイヤーは画面外に出ない限り、自由に移動できます。
    敵は様々な速度で左へ飛行します。
    衝突するとゲームオーバーになります。
    """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # 空のスプライトリストを初期化します
        """
        スプライト：画面上の特定の位置に描画される、定義されたサイズのゲーム オブジェクトの 2 次元画像
        本当はdraw_コマンドでも描画できるが、多くなるため、スプライトリストを使う
        
        アプデと更新は、.update() ⇨ .draw()
        
        enemies_list:敵の位置を更新し、衝突を確認するために使用します。
        clouds_listクラウドの位置を更新するために使用します。
        最後に、 all_spritesすべてを描きます。
        """
        self.enemies_list = arcade.SpriteList()  # 敵のスプライトリスト
        self.clouds_list = arcade.SpriteList()  # 雲のスプライトリスト
        self.all_sprites = arcade.SpriteList()  # 全てのスプライトリスト
        self.bullets_list = arcade.SpriteList() # 弾丸リストの作成
        self.paused = False

    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.player = arcade.Sprite("images/airplane.png", SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10 # スプライトの左端をウィンドウの左端から数ピクセル離して配置することで、スプライトの x 位置を設定
        self.all_sprites.append(self.player)
        
        # Spawn a new enemy every 0.25 seconds
        arcade.schedule(self.add_enemy, 0.25)
        # Spawn a new cloud every second
        arcade.schedule(self.add_cloud, 0.5)
    
    # 敵を表示
    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen
            Arguments:
                delta_time {float} -- How much time has passed since the last call
            
            左下が(x,y) = (0,0)であることを考慮
            
            機能）
            ウィンドウの右側のランダムな場所に表示されます。
            彼らは一直線に左へ移動します。
            画面から外れると消えてしまいます。
            
            このenemyを表示させるためには、updateを行う必要がある。
            
            enemy.pngが表示されない原因） 2024/10/22
            arcade.run() を呼び出すと、ゲームループが開始されます。
            このループは、描画 (on_draw()) と更新 (on_update()) を繰り返します。
            元のコードでは on_update() が定義されていなかったため、arcade.run() 内で on_draw() だけが繰り返し実行されていました。
            そのため、敵の update() メソッドが実行されず、敵が移動せず、画面に表示されなかったと考えられます。
        """
        # 敵ユニットの作成
        # enemy = arcade.Sprite("images/enemy.png", SCALING)
        enemy = FlyingSprite("images/enemy.png", SCALING*2)

        # 位置をランダムな高さに設定し、画面右外へ
        enemy.left = random.randint(self.width, self.width + 80) # enemy.center_xと同じ意味
        enemy.top = random.randint(10, self.height - 10) # enemy.center_yと同じ意味
        
        # speed
        # y座標は変えずにx座標を変えている。-20にしているのは右(X座標Max)から左(X座標Min)に流れるため
        # enemy.velocity = (random.randint(-20, -5), 0)
        
        # アレンジ
        enemy.velocity = (random.randint(-7, -3), random.randint(-1, 1)) 
        
        # Add it to the enemies list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)
    
    def add_cloud(self, delta_time: float):
        """
        add_enemyと同じ要領で作成
        """
        # cloudの定義
        cloud = FlyingSprite("images/cloud.png", SCALING*2)
        cloud.center_x = random.randint(self.width-80, self.width)
        cloud.center_y = random.randint(self.height-500, self.height)
        cloud.velocity = (random.randint(-3, -2), 0)
        
        # add list
        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)
    
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
        
        # 敵と衝突したら、ゲームを終了する
        if self.player.collides_with_list(self.enemies_list):
            print("敵と衝突しました。")
            arcade.close_window()
        
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

def main():
    ss = SpaceShoter(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
    ss.setup() # setupが実行されないと、オブジェクトも何も定義されない状態になるため、この処理は必要
    arcade.run() # on_draw()とon_update()を繰り返す関数。画面に表示されていなかったら、updateを疑う

if __name__ == "__main__":
    main()
