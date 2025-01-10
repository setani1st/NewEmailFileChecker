import os
import win32com.client
from email.header import decode_header

TEMP_FOLDER = "temp/"  # 添付ファイルを保存する一時フォルダ

# Outlookのアプリケーションを起動
def connect_to_outlook():
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    return namespace

# メールから添付ファイルを抽出して保存する関数
def fetch_attachments(namespace, folder="INBOX"):
    # 受信トレイの指定
    inbox = namespace.GetDefaultFolder(6)  # 6は受信トレイ
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)  # 受信時刻でソート（降順）

    # 未読のメールを処理
    for message in messages:
        if message.UnRead:  # 未読のメールのみ処理
            print(f"処理中: {message.Subject}")
            # メールの添付ファイルを保存
            for attachment in message.Attachments:
                filename = attachment.FileName
                if filename:
                    filepath = os.path.join(TEMP_FOLDER, filename)
                    attachment.SaveAsFile(filepath)
                    print(f"保存: {filepath}")
            # メールを既読にする
            message.UnRead = False

    return os.listdir(TEMP_FOLDER)  # 保存したファイルのリストを返す

# メールの送信者を取得する関数
def get_sender_email(message):
    sender = message.Sender
    return sender.Address if sender else None

# メールを処理する関数
def process_email():
    # Outlookに接続
    namespace = connect_to_outlook()

    # 添付ファイルを取得
    files = fetch_attachments(namespace)

    return files
