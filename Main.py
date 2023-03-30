from threading import Thread
from time import sleep
import MT4Pipe
import Controll_highlow as ch
import GUI
import traceback

def change_symbol_name(symbol):
    """通貨名をハイローオーストラリアと同じになるように合わせる

    Args:
        symbol(str): MT4から取得した通貨名
    Return:
        result_symbol(str): 変更後の通貨名
    """

    if symbol != 'XAUUSD':
        result_symbol = symbol[:3] + '/'+ symbol[3:]
    else:
        result_symbol = 'GOLD'
    return result_symbol

class main_flow():

    def move_highlow(self,symbol):
        """辞書を参照し、指定された通貨に移動する
        Args:
            symbol(str): 移動する通貨名(MT4型で指定)
        """
        timedict = GUI.get_symbol_time_list()
        typedict = GUI.get_symbol_type_list()
        highlow_symbol = change_symbol_name(symbol)
        time_ = timedict[symbol]
        type_ = typedict[symbol]
        try:
            self.highlow.select_type(type_)
            self.highlow.move_symbol(highlow_symbol)
            self.highlow.select_time(time_,symbol)
        except:
            print('通貨に移動できませんでした')
        
    def entry_highlow(self,direction):
        """現在の通貨でエントリー
        
        Args:
            direction(str): エントリーする方向指定HIGH、LOW
        """
        userlist = GUI.get_user_dist()
    
        # --- 定額購入
        if userlist['flat_price']: inputprice = userlist['entry_price']

        # --- 複利購入
        else: inputprice = int(round(float(userlist['coins_rate']) * self.highlow.get_coins() *0.01))

        try:
            self.highlow.send_price(inputprice)
            self.highlow.entry(direction)
        except:
            print('エントリーできませんでした')

    def mql_to_action_loop(self):
        """MQL4のパイプを監視する
        """

        while self.obverb_mql_flag:
            mqlinfo = MT4Pipe.Get_MQL4_info()
            if not self.obverb_mql_flag: return
            if mqlinfo == None: continue
            try:GUI.change_nowcoins(self.highlow.get_coins())
            except:traceback.print_exc()
            
            if mqlinfo['order_type'] == 'MOVE':
                self.move_highlow(mqlinfo['symbol'])

            if mqlinfo['order_type'] == 'HIGH':
                self.move_highlow(mqlinfo['symbol'])
                self.entry_highlow('HIGH')
                
            if mqlinfo['order_type'] == 'LOW':
                self.move_highlow(mqlinfo['symbol'])
                self.entry_highlow('LOW')
            sleep(0.1)
        
    def gui_to_action_loop(self):
        """GUIをからのシグナルを監視する
        """

        while True:
            sleep(0.1)
            # 終了時処理    
            gui_mes = GUI.get_gui_signal()
            if gui_mes == 'exit': break
            if gui_mes == None: continue

            userlist = GUI.get_user_dist()

            # 通貨ボタン
            if gui_mes == 'signal':
                self.move_highlow(GUI.get_signal_info()['symbol'])

            # 開始ボタン
            if gui_mes == 'start':

                self.highlow = ch.highlow_controler()

                # --- デモの時 ---
                if userlist['run_demo']:

                    if self.highlow.start_demo() != 'seccess': continue
                    GUI.change_gui_message('稼働中')
                    self.obverb_mql_flag = True
                    Thread(target = self.mql_to_action_loop, daemon=True).start()

                    self.obverb_mql_flag = True

                # --- リアルの時 ---
                else: 
                    login = self.highlow.login_to_start(password=userlist['input_password'], code=userlist['input_code'], username=userlist['input_username'], collect_code=userlist['collect_code'])
                    if login == 'password_error': GUI.change_gui_message('パスワードが無効です')
                    elif login == 'code_error': GUI.change_gui_message('承認コードが違います')
                    elif login == 'seccess':
                        self.obverb_mql_flag = True
                        GUI.change_gui_message('稼働中')
                        Thread(target = self.mql_to_action_loop, daemon=True).start()
            # 停止ボタン
            if gui_mes == 'stop':
                self.obverb_mql_flag = False
                self.highlow.stop()

            

        # 強制終了したときにブラウザを閉じる
        try: self.highlow.stop()
        except: pass

if __name__ == '__main__':
    Thread(target = GUI.GUI_start, daemon=True).start()
    main = main_flow()
    main.gui_to_action_loop()