import os
import time
import pandas as pd
from email_handler import connect_to_outlook, fetch_attachments
from file_classifier import classify_and_move_file
from organizer import create_folder, move_file

INTERVAL = 10 * 60  


def load_email_list(excel_file):
    
    df = pd.read_excel(excel_file)
    email_list = df['H'].dropna().tolist()  
    return email_list

# メールアドレスが名簿にあるか確認する関数
def is_valid_sender(sender_email, email_list):
    return sender_email in email_list

def process_email_attachments():
    # 一時ディレクトリの作成
    if not os.path.exists("temp/"):
        os.makedirs("temp/")

    print("Outlook と接続しています")
    mail = connect_to_outlook()

    print("添付ファイルを取得しています")
    attachments = fetch_attachments(mail)

    if not attachments:
        print("何もありませんでした")
        return

    print(f"{len(attachments)} を見つけました")

    # 名簿のメールアドレスを読み込む
    excel_file = "名簿.xlsx"  # 名簿のエクセルファイル
    email_list = load_email_list(excel_file)

    # 各ファイルの処理
    for file, sender in attachments:
        file_path = os.path.join("temp/", file)


        print(f"{sender}さんのメール読み込み中")
        if not is_valid_sender(sender, email_list):
            print(f"{sender}は名簿に存在しません。")
            continue  

        # ファイルの分類
        print(f"Classifying file: {file}")
        classification = classify_and_move_file(file_path)

        # ファイルの整理
        print(f"Organizing file: {file}")
        destination = create_folder(sender, classification)  # senderをperson_nameとして利用
        move_file(file_path, destination)

    print("Processing complete!")

def main():
    print("メール確認を開始します...")
    while True:
        try:
            print("メールを確認中...")
            process_email_attachments()
            print(f"次回の確認は{INTERVAL / 60}分後です...")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        
        # 次回の確認まで待機
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
