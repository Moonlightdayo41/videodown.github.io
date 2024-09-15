from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__, static_folder='.', static_url_path='')

DOWNLOAD_DIR = 'C:/Users/ユーザー/Documents/NetDLSite/downloads/'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URLが提供されていません'}), 400

    try:
        ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),  # ダウンロード先のディレクトリとファイル名
    'format': 'bestaudio/best',  # 音声と動画の最適なフォーマットを選択
}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            
            # ファイルのフルパスを取得
            downloaded_file = os.path.join(DOWNLOAD_DIR, filename)
            
            # ファイルを送信
            response = send_file(downloaded_file, as_attachment=True)
            
            # ファイルを削除
            try:
                os.remove(downloaded_file)
            except Exception as e:
                app.logger.error(f'ファイルの削除中にエラーが発生しました: {str(e)}')
            
            return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

