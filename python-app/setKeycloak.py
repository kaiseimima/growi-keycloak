from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenID
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import os.path
import requests
import json


# keycloakのurlを設定
keycloak_url = 'http://keycloak:8080/auth'

# realmNameとしてrealm.jsonファイルから設定したrealmの名前を取得
with open('realm.json') as f:
    j = json.load(f)
    realmName = j["realm"]

# KeycloakのURLと認証情報を設定
keycloak_admin = KeycloakAdmin(
    server_url="http://keycloak:8080/auth/",
    username="admin",
    password="admin",
    realm_name = realmName,
    user_realm_name="master",
    verify=True,
)


# Realmの作成
def create_realm():
    with open("realm.json", "r") as file:
        realm_data = json.load(file)
        keycloak_admin.create_realm(payload=realm_data, skip_exists=True)
    print("Realm created successfully")


# クライアントの作成
def create_client():
    with open("createGrowiClient.json", "r") as file:
    # with open("cp_createGrowiClient.json", "r") as file:
        client_data = json.load(file)
        keycloak_admin.create_client(payload=client_data, skip_exists=True)
    print("Client created successfully")
            

# ユーザーの作成
def create_users():
    with open("users.json", "r") as file:
        users_data = json.load(file)
        keycloak_admin.create_user(payload=users_data, exist_ok=True)
        # keycloak_admin_dev2.create_user(users_data)
    print("Users created successfully")



# keycloakから証明書を取得する
def get_cert():
    # Keycloakにアクセスしてdescriptorページの内容を取得します
    descriptor_url = f'{keycloak_url}/realms/{realmName}/protocol/saml/descriptor'
    response = requests.get(descriptor_url)
    descriptor_content = response.text

    # BeautifulSoupを使用してXMLをパースします
    soup = BeautifulSoup(descriptor_content, 'xml')

    # dsig:X509Certificate要素を取得します
    x509_cert_element = soup.find('ds:X509Certificate')

    # 証明書の値を取得します
    x509_cert_value = x509_cert_element.text

    write_cert_to_growijson(x509_cert_value)
    
    print("cert uploaded to growi.json successfully")


# growiSaml.jsonに証明書を書き込む関数
def write_cert_to_growijson(cert_value):
    # growi.jsonファイルを読み込む
    with open("growiSaml.json", "r") as json_file:
        data = json.load(json_file)

    # "samlCert"の値を更新
    data["cert"] = "-----BEGIN CERTIFICATE-----\n" + cert_value + "\n-----END CERTIFICATE-----"

    # JSONファイルの書き込み
    with open('growiSaml.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


# 実行
create_realm()
create_client()
create_users()

# growiSaml.jsonに証明書のデータを書き込む。
get_cert()
