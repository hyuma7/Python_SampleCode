import PySimpleGUI as sg
from joblib import dump,load
from hashlib import sha256
from os import makedirs
from os.path import isdir

# --- 定型変数を定義 ---
HIGHLOWLIST = ['HighLow', 'HighLowスプレッド']
OPETIONSLIST = ['Turbo', 'HighLow', 'Turboスプレッド', 'HighLowスプレッド']
HIGHLOW_TIME = ['短期', '中期', '長期', '1時間', '23時間']
TURBO_TIME = ['30秒', '1分', '3分', '5分']

#--- 初期設定 ---
split_index = 11
local_symbol_list = ['AUDJPY', 'AUDUSD', 'BTCJPY', 'BTCUSD', 'ETHJPY', 'ETHUSD', 'EURJPY', 'EURUSD', 'GBPJPY', 'NZDJPY', 'USDJPY',
                    'CADJPY', 'CHFJPY', 'EURAUD', 'EURGBP', 'GBPAUD', 'GBPUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'GOLD']
local_time_list = ['5分' if i < split_index  else '短期' for i,_ in enumerate(local_symbol_list)]
local_time_list[-1] = '23時間'
local_typename_list = ['Turbo' if i < split_index  else 'HighLow' for i,_ in enumerate(local_symbol_list)]
time_list = [TURBO_TIME if i < split_index else HIGHLOW_TIME for i,_ in enumerate(local_symbol_list)]
time_list[-1] = '23時間'
user_dist = {'flat_price': True,
    'entry_price':'1000',
    'coins_rate':'2',
    'input_code': '',
    'input_username': '',
    'input_password': '',
    'run_demo': True,
    'collect_code': None
    }
nowcoins = -1

# --- セーブデータ読み込み ---
SAVEFILE = 'savedata/'

try:
    local_time_list = load(SAVEFILE + 'local_time_list.pki')
    local_typename_list = load(SAVEFILE + 'local_typename_list.pki')
    user_dist = load(SAVEFILE + 'user_dist.pki')
except:
    print('セーブデータが見つかりませんでした')

# 通貨別設定 レイアウト
frame1 = [[sg.Text('通貨ペア   取引オプション ' + " "*10 + ' 時間 '+" "*5, background_color='#202020')]]
for i, s in enumerate(local_symbol_list):
    option = OPETIONSLIST
    if split_index <= i:
        option = HIGHLOWLIST
    if s == 'GOLD':
        option = ['HighLow']
        local_time_list[i] = '23時間'
    frame1.append([
    sg.Button(s,size = (7,0),key=s), # 通貨
    sg.Combo(option, default_value=local_typename_list[i], size=(17, 1), enable_events=True, key=s + '_OPTIONS'),
    sg.Combo(time_list[i], default_value=local_time_list[i], size=(6, 1), enable_events=True, key=s + '_TIMES'),
    ])

# エントリー設定 レイアウト
frame2 =[
        #=== スタート、停止ボタン、メッセージ
        [
            sg.Button('開始',enable_events=True, key='-START-'),
            sg.Button('停止',enable_events=True, key='-STOP-', disabled = True),
            sg.Text('停止中', key='-MESSAGE-')
        ],

    # === 口座設定 ===
        [
            sg.Text('口座設定'+' '*100, background_color='#202020')
        ],
        #=== 承認コード
        [
            sg.Text('承認コード',size=(9,0)),
            sg.Input(user_dist['input_code'], enable_events=True, key='-CODE-', size=(7,1))
        ],
        #=== ユーザーID
        [
            sg.Text('ユーザー',size=(9,0)),
            sg.Input(user_dist['input_username'], enable_events=True, key='-USERNAME-', size=(10,1)),
        ],
        #=== password
        [
            sg.Text('パスワード',size=(9,0)),
            sg.Input(user_dist['input_password'], enable_events=True, key='-PASSWORD-', size=(18,1), password_char="●"),
            sg.Checkbox("表示", enable_events=True, key="-toggle_password-"), 
        ],
        #=== 口座切り替え
        [
            sg.Text('口座'),
            sg.Radio('デモ口座', enable_events=True, key='-DEMO-', group_id='0', default=user_dist['run_demo']),
            sg.Radio('リアル口座', enable_events=True, key='-REAL-', group_id='0',default=not user_dist['run_demo'])
        ],
        #=== 口座残高
        [
            sg.Text('口座残高'),
            sg.Text('---', key='HIGHLOWCOINS')
        ],

    # === エントリー設定 ===
        [
            sg.Text('購入設定'+' '*100, background_color='#202020')
        ],
        #=== 定額設定
        [
            sg.Radio('定額購入', enable_events=True, key='FLATPRICECHECK', group_id='1', default=user_dist['flat_price']),
            sg.Input(user_dist['entry_price'], enable_events=True, key='FLATPRICE', size=(15,0), disabled= not user_dist['flat_price']),
            sg.Text('円')
        ],
        #=== 複利設定
        [
            sg.Radio('複利購入', enable_events=True, key='COMPOUNDCHECK', group_id='1',default= not user_dist['flat_price']),
            sg.Input(user_dist['coins_rate'], enable_events=True, key='COMPOUND', size=(7,0), disabled=user_dist['flat_price']),
            sg.Text('%'),
            sg.Text('---', key='-COMPOUNDPRICE-')
        ],
    ]

def get_symbol_time_list():
    """ 通貨ごとの時間設定の辞書を返す
    
    Return:
        timedict(dict):
    """
    timedict = dict(zip(local_symbol_list, local_time_list))
    return timedict

def get_symbol_type_list():
    """ 通貨ごとのオプション設定の辞書を返す
    
    Return:
        typedict(dict):
    """
    typedict = dict(zip(local_symbol_list, local_typename_list))
    return typedict

def get_user_dist():
    """ ユーザー情報を辞書型で返す
    
    Return:
        user_dist(dist):ユーザー情報の初期設定 ↓
            'flat_price': True,
            'entry_price':'1000',
            'coins_rate':'2',
            'input_code': '',
            'input_username': '',
            'input_password': '',
            'run_demo': True,
            'collect_code': None
    """
    return user_dist

exit_Flg = False
send_message = ''
def get_gui_signal():
    """ GUIからのメッセージを返す
    
    Return:
        message(str): メッセージ内容
    """
    global send_message
    
    if exit_Flg: return 'exit'
    if send_message == '': return

    # 送信したらsend_messageをクリア
    else:
        message = send_message
        send_message = ''
        return message

window=None
def change_nowcoins(coins):
    """ 残高を反映させる

    Args:
        coins:
    """
    global nowcoins
    nowcoins = int(coins)
    window['HIGHLOWCOINS'].update(nowcoins)
    window['-COMPOUNDPRICE-'].update((int(round((float(user_dist['coins_rate'])) * nowcoins * 0.01))))

def change_gui_message(mes):
    """ GUI上のメッセージを変更する

    Args:
        mes(str):メッセージ
    """
    window['-MESSAGE-'].update(mes)
    
def get_hash(formal: str):
    """ 文字列を編集してハッシュ化し、短くして返す
    Args:
        formal(str):ハッシュ化したい文字列

    Return:
        ハッシュ化した文字列
    """
    afterstring = formal + 'pAjenG93'
    s256 = sha256(afterstring.encode()).hexdigest()
    string = s256[2] + s256[4] + s256[15] + s256[25] + s256[8] + s256[12]
    return string

def save_data():
    """ GUIの内容をセーブする """

    if not isdir('savedata'): makedirs('savedata')
    dump(local_time_list, SAVEFILE + 'local_time_list.pki', compress=3) 
    dump(local_typename_list, SAVEFILE + 'local_typename_list.pki', compress=3)
    dump(user_dist, SAVEFILE + 'user_dist.pki', compress=3)

# 通貨移動のオーダーを出す
signal_info = {}
def get_signal_info():
    return signal_info
    

def GUI_start():
    """ GUIループを開始する """
    global exit_Flg
    global send_message
    global window

    # === レイアウト設定 ===
    layout = [[sg.Frame('',frame1, size=(300, 580)),sg.Frame('',frame2, size=(300, 580))]]
    window = sg.Window('HighLowAuto', layout, resizable=True, finalize=True)
    while True:
        event, values = window.read()
            
        # === 共通設定 ===
        for i, Pname in enumerate(local_symbol_list):
            Pnum = i
            Pname = local_symbol_list[Pnum]

            # --- オプション設定
            if event == Pname + '_OPTIONS':

                window[Pname + '_TIMES'].update(value='短期', values = HIGHLOW_TIME)
                local_typename_list[Pnum] = values[Pname + '_OPTIONS']
                local_time_list[Pnum] = '短期'
            
            # --- 通貨を移動
            if event == Pname:
                signal_info.update({'symbol': Pname, 'rate':'0', 'order_type':'MOVE'})
                send_message = 'signal'

        #=== 開始 ===
        if event == '-START-':
            window['-START-'].update(disabled=True)
            window['-STOP-'].update(disabled=False)
            send_message = 'start'
            window['-MESSAGE-'].update('起動中')
        #=== 停止 ===
        if event == '-STOP-':
            window['-START-'].update(disabled=False)
            window['-STOP-'].update(disabled=True)
            send_message = 'stop'
            window['-MESSAGE-'].update('停止中')

        # !=== アカウント情報 ===!
        #=== ユーザー ===
        elif event == '-USERNAME-':
            user_dist['input_username'] = values['-USERNAME-']
            user_dist['input_username'] = values['-USERNAME-']
            user_dist['collect_code'] = get_hash(user_dist['input_username'])

        #=== password ===
        elif event == '-PASSWORD-':
            user_dist['input_password'] = values['-PASSWORD-']

        #=== password 表示ボックス ===
        elif event == "-toggle_password-":
            if values["-toggle_password-"]:
                window["-PASSWORD-"].update(password_char="")
            else:
                window["-PASSWORD-"].update(password_char="●")

        #=== 承認コード ===
        if event == '-CODE-':
            user_dist['input_code'] = values['-CODE-']

        # !=== 口座切り替え ===!
        #--- デモ
        if event == '-DEMO-':
            user_dist['run_demo'] = True

        #--- リアル
        elif event == '-REAL-':
            user_dist['run_demo'] = False

        # === HighLow設定 ===
        for i, Pname in enumerate(local_symbol_list[11:]):

            Pnum = i + split_index
            Pname = local_symbol_list[Pnum]

            if Pname == 'GOLD':
                continue

            #--- オプションタイプ ---
            if event == Pname + '_OPTIONS':
                window[Pname + '_TIMES'].update(value='短期', values = HIGHLOW_TIME)
                local_typename_list[Pnum] = values[Pname + '_OPTIONS']
                local_time_list[Pnum] = '短期'

            #--- 時間 ---
            if event == Pname + '_TIMES':
                local_time_list[Pnum] = values[Pname + '_TIMES']

        # === turbo設定 ===
        for i, Pname in enumerate(local_symbol_list[:11]):

            Pnum = i
            Pname = local_symbol_list[Pnum]

            #--- オプションタイプ
            if event == Pname + '_OPTIONS':

                if values[Pname + '_OPTIONS'] == 'Turbo':
                    window[Pname + '_TIMES'].update(value='30秒', values = TURBO_TIME)
                    local_time_list[Pnum] = '30秒'

                elif values[Pname + '_OPTIONS'] == 'Turboスプレッド':
                    window[Pname + '_TIMES'].update(value='30秒', values = TURBO_TIME)
                    local_time_list[Pnum] = '30秒'

                elif values[Pname + '_OPTIONS'] == 'HighLow':
                    window[Pname + '_TIMES'].update(value='短期', values = HIGHLOW_TIME)
                    local_time_list[Pnum] = '短期'

                else:
                    window[Pname + '_TIMES'].update(value='短期', values = HIGHLOW_TIME)
                    local_time_list[Pnum] = '短期'

                local_typename_list[Pnum] = values[Pname + '_OPTIONS']

            #--- 時間 
            if event == Pname + '_TIMES':
                local_time_list[Pnum] = values[Pname + '_TIMES']

        #=== 定額購入 ===
        if event == 'FLATPRICE':
            try:
                entry_price = int(values['FLATPRICE'])
                entry_price = values['FLATPRICE']
                user_dist['entry_price'] = entry_price
            except:
                window['FLATPRICE'].update(value = '')

        #=== 定額ON ===
        if event == 'FLATPRICECHECK':
            window['FLATPRICE'].update(disabled=False)
            window['COMPOUND'].update(disabled=True)
            window['-COMPOUNDPRICE-'].update('')
            user_dist['flat_price'] = True

        #=== 複利ON ===
        if event == 'COMPOUNDCHECK':
            window['FLATPRICE'].update(disabled=True)
            window['COMPOUND'].update(disabled=False)

            #--- 複利金額を表示
            if nowcoins != -1: window['-COMPOUNDPRICE-'].update(int((round(float(user_dist['coins_rate']) * int(nowcoins) * 0.01))))
            else: window['-COMPOUNDPRICE-'].update('---')
            user_dist['flat_price'] = False

        #=== 複利設定 ===
        if event == 'COMPOUND':
            try:
                coins_rate = float(values['COMPOUND'])
                user_dist['coins_rate'] = coins_rate
                #--- 複利金額を表示
                if nowcoins != -1:
                    window['-COMPOUNDPRICE-'].update(int((round(float(user_dist['coins_rate']) * int(nowcoins) * 0.01))))
                else:
                    window['-COMPOUNDPRICE-'].update('計算中')
            except:
                window['COMPOUND'].update(value = '')

        # === 終了処理 ===
        if event is None:
            exit_Flg = True
            save_data()
            break

if __name__ == '__main__':
    GUI_start()