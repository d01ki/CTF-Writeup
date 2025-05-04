import socket

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('ecbpp.kctf-453514-codelab.kctf.cloud', 1337))
    return s

def send_message(s, message):
    s.sendall(message.encode() + b'\n')
    return s.recv(2048)

def get_encrypted_message(s, message):
    s.recv(2048)  # 初期のWelcomeメッセージを受け取る
    send_message(s, 'Y')  # 暗号化する準備を整える
    send_message(s, message)
    response = s.recv(2048)  # 暗号化されたメッセージを受け取る
    return response.decode()

def main():
    s = connect_to_server()

    # 1. 最初に空のメッセージを送って、フラグの暗号化された部分を取得します
    message = "A" * 16  # 初回は適当なメッセージを送る
    encrypted_message = get_encrypted_message(s, message)
    print("Encrypted message:", encrypted_message)

    # 2. 次にメッセージの後ろにフラグが加わるので、フラグ部分の暗号化を観察します
    # 追加で送信してフラグの暗号化された部分を観察
    message2 = "A" * 15  # 1バイト短くして
    encrypted_message2 = get_encrypted_message(s, message2)
    print("Encrypted message2:", encrypted_message2)

    # 3. encrypted_messageとencrypted_message2を比較して、フラグ部分のパターンを確認します

    # ここからはECBモードの性質を利用して、フラグを特定していきます

    s.close()

if __name__ == "__main__":
    main()
