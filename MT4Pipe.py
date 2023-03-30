import win32pipe
import win32file
import win32api
from traceback import print_exc

# パイプ名
pipename = 'mt4_to_python_pipe'

def Get_MQL4_info():
    """ MQL4からのシグナルを辞書型で返す
    
    return: entry_dict(dict): MQLのエントリー情報(symbol, rate, order_type)
    """
    # パイプが開くまで待つ
    try:
        pipe = win32pipe.CreateNamedPipe(
                '\\\\.\\pipe\\' + pipename, 
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe. PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,
                1, 256, 256, 0, None)

        win32pipe.ConnectNamedPipe(pipe, None)
        buffer = b''
    except:
        pass

    while True:
        try:
            # パイプから1バイト読み取る (パイプが空の場合は、パイプから読めるまで待つ)
            hr, char = win32file.ReadFile(pipe, 4096)
        except:
            break
        
        buffer += char
    
        # 改行文字が出現したところで読むのをやめる
        if char == b'\n':
            break
    
    # データを編集して、形式に当てはまる場合 辞書型にして返す
    try:
        line = buffer.decode('utf-8').replace('\r\n', '')
        win32pipe.DisconnectNamedPipe(pipe)
        win32api.CloseHandle(pipe)

        # 辞書型に変換
        entry = line.split(',')
        entry_dict = {'symbol': entry[0],
            'rate': entry[1],
            'order_type': entry[2]}
        return entry_dict
    except:
        return