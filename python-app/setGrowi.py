import requests
import json

insUrl = 'http://app:3000/_api/v3/installer'
regUrl = 'http://app:3000/_api/v3/register'
logUrl = 'http://app:3000/_api/v3/login'
# siteUrl設定データ
site_url = 'http://app:3000/_api/v3/app-settings/site-url-setting'
# SAML設定データ
saml_url = 'http://app:3000/_api/v3/security-setting/saml'
samlEn_url = 'http://app:3000/_api/v3/security-setting/authentication/enabled'

# ログインリクエストを送信し、セッションを確立
session = requests.session()

def set_install():
    # install用のjsonファイルを読み込む
    with open('growiinsData.json', 'r') as file:   
        install_data = json.load(file)
    # grwoiの初期設定
    install_response = session.post(url=insUrl, json=install_data)
    print(install_response.status_code)
    print(install_response.json())

def set_register():
    # register用のjsonファイルを読み込む
    with open('growiregData.json', 'r') as file:
        register_data = json.load(file)
    # growiへregister
    register_response = session.post(url=regUrl, json=register_data)
    print(register_response.status_code)
    print(register_response.json())

def set_login():
    # login用のjsonファイルを読み込む
    with open('growilogData.json', 'r') as file:
        login_data = json.load(file)
        # growiへlogin
    login_response = session.post(url=logUrl, json=login_data)
    print(login_response.status_code)
    print(login_response.json())

def set_siteUrl():
    # growiのcallback_urlを設定するためのjsonファイルの読み込み
    with open('growisiteUrl.json', 'r') as file:
        data_to_url = json.load(file)

    # siteUrl 設定
    res_url = session.put(site_url, json=data_to_url)
    print(res_url.status_code)
    print(res_url.json())

def set_samlEn():
    # growiのsamlをenabledにするためのjsonファイルの読み込み
    with open('growiSamlEnabled.json', 'r') as file:
        data_to_samlen = json.load(file)
    # saml_enabled 設定
    res_en = session.put(samlEn_url, json=data_to_samlen)
    print(res_en.status_code)
    print(res_en.json())

def set_saml():
    # growiのsamlの各種設定のjsonファイルの読み込み
    with open('growiSaml.json', 'r') as file:
        data_to_saml = json.load(file)
    # saml 設定
    res_sc = session.put(saml_url, json=data_to_saml)
    print(res_sc.status_code)
    print(res_sc.json())

# set_install()
# set_register()
set_login()

set_siteUrl()
set_samlEn()
set_saml()
