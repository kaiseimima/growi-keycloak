# KeycloakとGrowiの連携を自動化

## 要約
DockerでKeycloakとGrowiを立ち上げ、SAML認証のお互いの設定をスクリプトで行う。


## Keycloakの設定
 SAML認証の設定のためにRealm, User, Growi用のClientを作成する必要があります。それぞれの設定したい情報は、`keycloak/`の
 * realm.json
 * users.json
 * createGrowiClient.json
 

 にjson形式で書かれています。
 `realm.json`ファイルではkeyclaokのrealm名をいかに記述してください。
 ```realm.json
 {
    "id": "dev",
    "realm": "dev",
    …
 }
 ```
`users.json`ファイルではSAML認証でGrowiへログインする際の"username"と"password"を設定してください。
 ```users.json
 {
    "username": "user",
    …
    "credentials": [
    {
      "type": "password",
      "value": "password",
      …
    }
    ],
    …
 }
 ```
`createGrowiClient.json`ファイルでは以下のurlが記述されている場所にGrowiのurlを記述してください。
 ```createGrowiClient.json
 {
    …
    "rootUrl": "https://growi.example.com/",
    "adminUrl": "https://growi.example.com/passport/saml/callback",
    …
    "redirectUris": [
        "https://growi.example.com/*"
    ],
    "attributes": {
        "saml_assertion_consumer_url_redirect": "https://growi.example.com/passport/saml/callback",
        …
        "saml_assertion_consumer_url_post": "https://growi.example.com/",
        …
        "saml_single_logout_service_url_redirect": "https://growi.example.com/passport/saml/callback",
    },
 }
 ```

## Growiの設定

### 初期設定

Growiでは初期設定、ログインもスクリプトで行うためそれぞれの設定を`growi/`の
 * growiinsData.json
 * growilogData.json
 
 で設定してください。

 growiinsData.jsonでは"username", "name", "email", "password"をそれぞれ以下で設定してください。
 ```growiinsData.json
 {
    "registerForm": {
        "username": "username",
        "name": "name",
        "email":"emailexample@gmail.com",
        "password": "password",
        "app:globalLang:": "ja_JP"
    }
}
 ```
 growilogData.jsonでは初期設定で設定した"username"と"password"を設定してください。
 ```growilogData.json
 {
    "loginForm": {
        "username": "username",
        "password": "password"
    }
}
 ```

### SAML設定
次に、`growi/`の
* growiSiteUrl.json
* growiSamleEnabeled.json
* growiSaml.json

でそれぞれ、Growiのurl、SAML設定をONにする、SAML認証のための各種設定を設定してください。

`growiSiteUrl.json`ではGrowiのurlを設定してください。
 ```growiSiteUrl.json
{
    "siteUrl": "https://growi.example.com"
}
 ```
 `growiSamlEnabled.json`では特に設定するものはありません。
 ```growiSamlEnabled.json
 {
    "isEnabled": true,
    "authId": "saml"
}
 ```
 `growiSaml.json`ではkeycloakで設定したRealmに対するSAMLエントリーポイントを設定してください。
 ここでは、keyclaokで`dev`というrealmを作成したと想定しています。
 ```growiSaml.json
 {
    …
    "entryPoint": "https://growi.example.com/auth/realms/dev/protocol/saml",
    …
}
 ```


## pythonの設定
pythonはDockerの公式イメージのpython3を使用しました。

`python-app/`の`Dockerfile`でpython3をコンテナ内で立ち上げ、`requirements.txt`で必要ないくつかのpythonのライブラリをインストールしています。

ターミナルでコンテナを立ち上げて、pythonが立ち上がっているコンテナ(ここではpython-app)へ`docker-compose exec python-app bash`で入って以下のようにpythonを実行してください。
```bash
docker-compose up -d
docker-compose exec python-app bash

python setKeycloak.py 
python setGrowi.py
```
### 注意
GrowiでSAMLの設定をする際に、Keycloakのrealmに関するX.509証明書が必要になるので先に、KeycloakのSAML設定を行ってください。(python setKeycloak.pyをおこなってから、python setGrowi.pyをおこなってください。)

### setKeycloak.py

* `setKeycloak.py`のkeycloak_urlはdocker-compose.ymlでkeycloakを立ち上げているサービス名、ポート番号で設定してください。(ここでは、サービス名は'keyclaok', ポート番号は'8080')
* `write_realm_to_growijson()`関数内のdata["entryPoint"]のurlはkeycloakのurlを設定してください。
* `create_realm()`, `create_client()`, `create_users()`関数でrealm, client, userを設定しています。
また、`get_cert()`, `write_realm_to_growijson(realmName)`でGrowiのSAML認証の設定に必要な設定を`growi/`下のjsonファイルに書き込むので、先にこちらを実行してください。
```setKeycloak.py
keycloak_url = 'http://keycloak:8080/auth'


def write_realm_to_growijson(realmName):
    …
    # "samlCert"の値を更新
    data["entryPoint"] = "https://sso.example.com/auth/realms/" + realmName + "/protocol/saml"
    …

sso.example.com

# 実行
create_realm()
create_client()
create_users()

# growiSaml.jsonに証明書のデータを書き込む。
get_cert()
# growiSaml.jdonにrealmのデータを書き込む。
write_realm_to_growijson(realmName)
```

### setGrowi.py
* `setGrowi.py`でも同じように、以下のurlはdocker-compose.ymlでgrowiを立ち上げているサービス名、ポート番号で設定してください(ここでは、サービス名は'app', ポート番号は'3000')
* 初めて`setGrowi.py`を実行する際にはログインをする`set_login()`を実行する必要はありません。`set_install()`で初期設定が行われます。2回目からは`set_install()`ではなく`set_login()`でログインしてください。
```setGrowi.py
insUrl = 'http://app:3000/_api/v3/installer'
…
samlEn_url = 'http://app:3000/_api/v3/security-setting/authentication/enabled'

set_install()
# set_login()
set_siteUrl()
set_samlEn()
set_saml()
```
# 参考

KeycloakとGrowiの設定は次の記事を参考にさせていただきました。[シングルサインオンサービスKeycloakとWikiシステムGrowiを連携する](https://qiita.com/myoshimi/items/f26cf3f179602a12a5ac)

ありがとうございます。




