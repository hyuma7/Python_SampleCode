from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

def get_time_to_highlow(cell):
    """
    Args:
        cell(WebElement):通貨ボックス

    Return:
        変換後の時間(str)
    """
    if len(cell.find_elements(By.CLASS_NAME, 'OptionItem_timeLeft__lhemy')) == 0:
        return cell.find_element(By.CLASS_NAME, 'OptionItem_duration__GpnIU').text

    elemtime = cell.find_element(By.CLASS_NAME, 'OptionItem_timeLeft__lhemy').find_element(By.TAG_NAME, 'span')
    highlow_time = elemtime.text
    highlow_time = highlow_time.replace(':', '')
    if highlow_time == '': return
    inttime = int(highlow_time)
    if cell.find_element(By.CLASS_NAME, 'OptionItem_duration__GpnIU').text == '1時間': return '1時間'
    elif inttime < 103 and inttime >= 0: return '中期'
    elif inttime < 500 and inttime >= 103: return '短期'
    elif inttime < 1000 and inttime >= 500: return '中期'
    elif inttime < 1440 and inttime >= 1000: return '長期'
    else: 
        if cell.find_element(By.CLASS_NAME, 'OptionItem_duration__GpnIU').text == '22時間': return '23時間'
        return cell.find_element(By.CLASS_NAME, 'OptionItem_duration__GpnIU').text

class highlow_controler():
    """HIGHLOWのサイトを操作するクラス
    """

    def login_to_start(self,code,username,password,collect_code):
        """ハイローを本講座で開始
        Args:
            code(str)
            username(str)
            password(str)

        return: condition(str): アクセス結果を表示
        """
        if collect_code != code: return 'code_error'
        options = webdriver.ChromeOptions()
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptInsecureCerts'] = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options, desired_capabilities=capabilities)
        self.driver.set_window_size(1200,800)
        self.driver.get("https://app.highlow.com/login")
        [self.driver.find_element(By.ID, "login-username").send_keys(s) for s in username] 
        [self.driver.find_element(By.ID, "login-password").send_keys(s) for s in password] 
        sleep(3.1)
        self.driver.find_element(By.XPATH, '//*[@id="login-submit-button"]').click()
        sleep(5)
        #--- passwordが違う場合
        if len(self.driver.find_elements(By.CLASS_NAME, 'FormMessage_message__1BGW5')) != 0:
            if self.driver.find_element(By.CLASS_NAME, 'FormMessage_message__1BGW5').text == 'ユーザー名またはパスワードが無効です。':
                return 'password_error'
        sleep(5)
        try:
            self.setting_start()
            self.save_element()
        except:
            print('サイトの取得に失敗')
            return 'wait'
        return 'seccess'

    def start_demo(self):
        """ハイローをデモバージョンで開始"""
        options = webdriver.ChromeOptions()
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptInsecureCerts'] = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options, desired_capabilities=capabilities)
        self.driver.set_window_size(1200,800)
        self.driver.get("https://app.highlow.com/quick-demo?source=header-quick-demo-cta")
        sleep(5)
        try:
            self.setting_start()
            self.save_element()
        except:
            print('サイトの取得に失敗')
            self.stop()
            return 'wait'
        return 'seccess'

    def setting_start(self):
        #---新しい順に並び替え
        self.open_left_bar()
        sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, '#App_sideContainer__132qg').find_element(By.CSS_SELECTOR, '#App_sideContainerContent__3UncR > div > div.OpenTrades_configs__15_w_ > div.OpenTradesCombinedDropdown_container__3NQ4S.OpenTrades_minimizedFiltersToggleContainer__3PK8l').click()
        sleep(0.2)
        leftchild = self.driver.find_element(By.CSS_SELECTOR, '#App_sideContainerContent__3UncR > div > div.OpenTrades_configs__15_w_ > div.OpenTradesCombinedDropdown_container__3NQ4S.OpenTradesCombinedDropdown_active__2cMTi.OpenTrades_minimizedFiltersToggleContainer__3PK8l > div.OpenTradesCombinedDropdown_collapseTransform__mfroh.OpenTradesCombinedDropdown_right__3IEaM > div > div')
        leftchild.find_element(By.CLASS_NAME, 'ScrollPanel_container__1ckhL').find_element(By.ID,'combinedOptionId2').click()
        sleep(0.3)
        #--- 終了時間順に並び替え
        leftbox = self.driver.find_element(By.CSS_SELECTOR,'#App_sideContainerContent__3UncR > div')
        leftbox.find_element(By.CSS_SELECTOR,'#TOOLTIP_ANCHOR_ID_TRADE_ACTIVITY_MODAL > div.ClickBounce_container__301Kv.OpenTrades_openFullOpenTradesScreenButton__3SoWr > div').click()
        self.driver.find_element(By.CSS_SELECTOR, '#root > div > div.takeOverModal_container__3Q2sx.takeOverModal_show__1_XV9 > div.takeOverModal_content__1jzs0 > div.takeOverModal_body__5UGc6.OpenTradesModal_body__6GZz7 > div.OpenTradesModal_controls__1_ViY > div.OpenTradesModal_filters__11zBL > div.OpenTradesModal_sortDropdown__Zvu0p.Dropdown_container__Oet-c.Dropdown_noGrowOnXL__2aaNw > div.ClickBounce_container__301Kv > div > div').click()
        sleep(0.5)
        Dropdown_right = self.driver.find_element(By.CSS_SELECTOR, '#root > div > div.takeOverModal_container__3Q2sx.takeOverModal_show__1_XV9 > div.takeOverModal_content__1jzs0 > div.takeOverModal_body__5UGc6.OpenTradesModal_body__6GZz7 > div.OpenTradesModal_controls__1_ViY > div.OpenTradesModal_filters__11zBL > div.OpenTradesModal_sortDropdown__Zvu0p.Dropdown_container__Oet-c.Dropdown_noGrowOnXL__2aaNw.Dropdown_active__1_BFI > div.Dropdown_collapseTransform__ASuTX.Dropdown_right__2K4Jn > div > div')
        Dropdown_right.find_element(By.CSS_SELECTOR,'#expirationTime').click()
        sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR,'#root > div > div.takeOverModal_container__3Q2sx.takeOverModal_show__1_XV9 > div.takeOverModal_content__1jzs0 > div.takeOverModal_header__Ht3GR > div > div').click()

    def save_element(self):
        self.allbox = self.driver.find_element(By.CSS_SELECTOR, '#root > div > div.App_tradingInterface__Kc3Cj')
        self.upperbox = self.allbox.find_element(By.CLASS_NAME, 'OptionBrowser_optionFilters__1n27n')
        self.upper = self.driver.find_element(By.CSS_SELECTOR, '#root > div > div.NavigationBar_container__2dta2.App_nav__2LqfW')
        self.pege_num = 0
        self.info_list_idx = 0
        self.sub_elem_num = 0

    def send_price(self,price):
        """値段を変える
        Args:
            price(str): 値段
        """
        
        input_price = self.allbox.find_element(By.CSS_SELECTOR, '#scroll_panel_1_content > div.App_tradeArea__1rrhJ > div > div.App_tradeForm__3vFhv > div > div.TradePanel_main__Ik28z > div.TradePanel_amountArea__3FGk0 > div:nth-child(2) > div > input')
        input_price.send_keys(price)

    def oneclick_on(self):
        oneclickcondition = self.allbox.find_element(By.CSS_SELECTOR, '#scroll_panel_1_content > div.App_tradeArea__1rrhJ > div > div.App_tradeForm__3vFhv > div > div.TradePanel_footer__37dl2 > div.TradePanel_label__2ivNV > div').get_attribute('data-test')
        if oneclickcondition == 'oneclick_24Px-icon':
            self.driver.execute_script('document.querySelector("#scroll_panel_1_content > div.App_tradeArea__1rrhJ > div > div.App_tradeForm__3vFhv > div > div.TradePanel_footer__37dl2 > div.Switch_switch__1MnTD")'+ '.click();')

    def select_type(self,option):
        """指定のオプションを合わせます

        Args:
            option(str): オプション名(Turbo,HighLow,Turboスプレッド,HighLowスプレッド)
        """
        

        now_option = self.upperbox.find_element(By.CLASS_NAME, 'Tabs_active__37GLw').text
        if now_option == option: return

        if option == 'Turbo': self.upperbox.find_element(By.ID, 'ChangingStrikeOOD0').click()
        elif option == 'HighLow': self.upperbox.find_element(By.ID, 'ChangingStrike0').click()
        elif option == 'Turboスプレッド': self.upperbox.find_element(By.ID, 'FixedPayoutHLOOD0').click()
        elif option == 'HighLowスプレッド': self.upperbox.find_element(By.ID, 'FixedPayoutHL0').click()
        sleep(0.8)

    def move_symbol(self,symbol):
        """指定の通貨に切り替えます

        Args:
            symbol(str): 通貨名、例(AUD/JPY)、(GOLD)
        """
        
        if self.upperbox.find_element(By.CLASS_NAME,'Dropdown_input__22IkL').find_element(By.TAG_NAME,'input').get_attribute('value') == symbol: return
        pulldown_button = self.upperbox.find_element(By.CLASS_NAME, 'OptionBrowser_assetFilter__26N3g')
        pulldown_button.click()
        self.upperbox.find_element(By.CLASS_NAME,'Dropdown_input__22IkL').find_element(By.TAG_NAME,'input').send_keys(Keys.CONTROL + "a")
        self.upperbox.find_element(By.CLASS_NAME,'Dropdown_input__22IkL').find_element(By.TAG_NAME,'input').send_keys(Keys.DELETE)
        self.upperbox.find_element(By.CLASS_NAME,'Dropdown_input__22IkL').find_element(By.TAG_NAME,'input').send_keys(symbol)
        self.upperbox.find_element(By.ID,symbol).click()
        sleep(0.5)

    def select_time(self,time,symbol):
        """選択したセルを返す
        Args:
            time(str): moveしたいtime
            symbol(str): moveしたいsymbol
        return:
            cell(WebElement): moveしたelement
        """
        nowtime = self.allbox.find_element(By.CLASS_NAME, 'ChartInfo_optionInfoValue__1mxxO').text
        nowtime = str(nowtime).split('• ')[-1]
        timecells = self.allbox.find_elements(By.CLASS_NAME, 'OptionItem_container__3xNYD')
        #---通貨が切り替わるのが確認できるまでトライする
        for _ in range(3):
            for cell in timecells:
                if get_time_to_highlow(cell) == time:
                    cell.click()
                    break
            sleep(0.2)
            if symbol.replace('/','') == self.get_active_cell()[0].replace(' ','').replace('/','') and time.replace('/','') == self.get_active_cell()[1].replace(' ','').replace('/',''):
                return cell
        return 'can not move cell'

    def Get_Spread(self,elem,option):
        """highlowのスプレッドを取得
        Turboスプレッド HighLowスプレッドは0.7秒ラグが発生します
        Args:
            elem(Webelement): 調べたいエレメント
            option(str): Turbo HighLow Turboスプレッド HighLowスプレッド

        Return:
            spreadgap(float): 現在のスプレッドを返します
        """
        spreadgap = 0.0
        try:
            if option == 'Turbo': return spreadgap
            elif option == 'HighLow':
                child_spread = float(elem.find_element(By.CLASS_NAME,'PriceDisplay_container__1Xcb3').text.replace('.',''))
                main_spread = float(self.allbox.find_element(By.CLASS_NAME,'PriceDisplay_container__1Xcb3').text.replace('.',''))
                spreadgap = abs((child_spread - main_spread))
            elif option == 'Turboスプレッド' or option == 'HighLowスプレッド':
                sleep(0.8)
                centerbox = self.allbox.find_element(By.CSS_SELECTOR, '#scroll_panel_1_content')
                if len(centerbox.find_elements(By.CLASS_NAME, 'ChartInfo_chartLabel__1xt4H')) == 0: return 0
                tradeupper = centerbox.find_elements(By.CLASS_NAME, 'ChartInfo_chartLabel__1xt4H')[-1]
                if 'スプレッド' == tradeupper.find_element(By.CLASS_NAME, 'ChartInfo_optionInfoLabel__2rAyk').text: # スプレッド
                    nowspread = tradeupper.find_element(By.CLASS_NAME, 'ChartInfo_optionInfoValue__1mxxO').text
                    spreadgap = float(nowspread)*10
        except:
            print('スプレッドの取得に失敗')
            return spreadgap
        return spreadgap

    def entry(self,direction):
        """ワンクリックをオンにして、エントリーします。
        
        Args:
            direction(str): HIGHかLOWを入力
        """
        self.oneclick_on()
        if direction == 'HIGH': self.allbox.find_element(By.CSS_SELECTOR,'#TradePanel_oneClickHighButton__3OAFf > div').click()
        if direction == 'LOW': self.allbox.find_element(By.CSS_SELECTOR,'#TradePanel_oneClickLowButton__3Oq9p > div').click()
        self.direction = direction

    def get_coins(self):
        """現在の口座残高を取得します

        return:
            nowcois(int) 口座の残高
        """
        
        nowcoins = self.upper.find_element(By.ID,"balanceValue").text
        nowcoins = ''.join(filter(str.isalnum, nowcoins))
        nowcoins = int(nowcoins)
        return nowcoins

    def stop(self):
        """HighLowを終了する
        """
        try: self.driver.quit()
        except:pass

    def start_position(self):
        try: self.close_left_bar()
        except: pass
        try:
            self.driver.find_element(By.CSS_SELECTOR,'#root > div > div.takeOverModal_container__3Q2sx.takeOverModal_show__1_XV9 > div.takeOverModal_content__1jzs0 > div.takeOverModal_header__Ht3GR > div > div').click()
        except: pass

    def open_left_bar(self):
        if len(self.driver.find_elements(By.CSS_SELECTOR,'#root > div > div.SecondaryBanner_container__1dK5N.GuidedTourInvitationBanner_readyToTradeBanner__Zx9Vd.SecondaryBanner_enter__1PYvo > div > div.SecondaryBanner_closeButton__1iz3l > svg')) == 1:
            self.driver.find_element(By.CSS_SELECTOR,'#root > div > div.SecondaryBanner_container__1dK5N.GuidedTourInvitationBanner_readyToTradeBanner__Zx9Vd.SecondaryBanner_enter__1PYvo > div > div.SecondaryBanner_closeButton__1iz3l > svg').click()
        if len(self.driver.find_elements(By.CLASS_NAME, 'App_collapsed__3fuRa')) == 1:
            self.driver.find_element(By.CSS_SELECTOR,'#root > div > div.NavigationBar_container__2dta2.App_nav__2LqfW').find_element(By.CSS_SELECTOR,'#TOOLTIP_ANCHOR_ID_OPEN_TRADES_TOGGLE').click()
    
    def close_left_bar(self):
        if len(self.driver.find_elements(By.CLASS_NAME, 'App_collapsed__3fuRa')) == 0:
            self.driver.find_element(By.CSS_SELECTOR,'#root > div > div.NavigationBar_container__2dta2.App_nav__2LqfW').find_element(By.CSS_SELECTOR,'#TOOLTIP_ANCHOR_ID_OPEN_TRADES_TOGGLE').click()

    def get_active_cell(self):
        """減算選択されているセルの詳細情報を返します
        
        return:
            active_cell_list(list)
                symbol(str): 通貨ペア
                time(str): 時間
        """
        symbol_group_element = self.allbox.find_element(By.CSS_SELECTOR,'#scroll_panel_1_content > div.App_optionBrowser__2Pqv1')
        symbol_group_element = symbol_group_element.find_element(By.CSS_SELECTOR,'#container_1')
        symbol_group_element = symbol_group_element.find_element(By.CSS_SELECTOR,'#scrollContainer_1')
        symbol_group_element = symbol_group_element.find_element(By.CSS_SELECTOR,'#content_1')
        active_cell_element = symbol_group_element.find_element(By.CLASS_NAME,'RecentlyOpenOptions_active__2rxVz')
        return active_cell_element.text.split('•')

if __name__ == '__main__':
    
    collect_code = ''
    input_code = ''
    input_username = ''
    input_password = ''
    web = highlow_controler()
    web.start_demo()
    web.select_type('Turbo')
    web.move_symbol('AUD/JPY')
    cell = web.select_time('30秒','AUD/JPY')
    spread = web.Get_Spread(cell,'HighLow')
    web.entry('HIGH')
    info = web.get_entry_data()
    web.update_waiting_list(info)
    #coins = web.get_coins()