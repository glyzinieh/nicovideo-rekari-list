import os

from flask import Flask, redirect, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont

from .gspread import get_id_list, get_rekari_list, get_video_info, record_post


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        videos = get_rekari_list()
        return render_template("index.html", videos=videos)

    @app.route("/policy/")
    def policy():
        return redirect("https://www.wisteriatp.work/privacy-policy")

    @app.route("/search/")
    def search():
        return render_template("search.html")

    @app.route("/watch_tmp/<string:id>")
    def watch(id):
        video = get_video_info(id)
        url = f"https://www.nicovideo.jp/watch_tmp/{id}"
        return render_template("watch_tmp.html", video=video, url=url)

    @app.route("/post/", methods=["GET", "POST"])
    def post():
        match request.method:
            case "GET":
                return render_template("post.html")

            case "POST":
                id = request.form["id"]
                title = request.form["title"]

                if not id or not title:
                    msg = "ID、タイトルは必須です"
                elif id in get_id_list():
                    msg = "この動画はすでに登録されています"
                else:
                    record_post(id, title)
                    msg = "登録が完了しました"

                return render_template("post.html", msg=msg)

    @app.route("/api/thumbnail/<string:id>")
    def thumbnail(id):
        video = get_video_info(id)

        title = video["タイトル"]

        # 画像のサイズを指定
        width, height = 1200, 630
        # 新しい画像を作成
        image = Image.new("RGB", (width, height), color=(73, 109, 137))

        # フォントを指定（ここではデフォルトのフォントを使用）
        # 実際には必要なフォントファイルを指定することを推奨
        font_path = "NOTOSANSJP-REGULAR.OTF"  # 例
        font_size = 50
        font = ImageFont.truetype(font_path, font_size)

        # ImageDrawオブジェクトを作成
        d = ImageDraw.Draw(image)
        # テキストの位置を計算
        text_bbox = d.textbbox((0, 0), title, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        # テキストを描画
        d.text((x, y), title, fill=(255, 255, 255), font=font)

        # 出力ディレクトリを作成
        output_dir = "temp"
        os.makedirs(output_dir, exist_ok=True)

        # 画像を保存
        output_path = os.path.abspath(os.path.join("temp", f"{id}.png"))
        image.save(output_path)

        return send_file(output_path, mimetype="image/png")

    return app
