# KeycloakとGrowiの連携を自動化

## 要約
DockerでKeycloakとGrowiを立ち上げ、SAML認証のお互いの設定をスクリプトで行う。


## KeycloakとGrowiの初期設定


`paramas.json`に初期設定を書き込んでください。

`python-app/`にある`setjson.py`を実行することでgrowi, keycloakの初期設定やSAML設定に関する情報をjsonファイルに自動的に書き込んでくれます。
```params.json
{
    "realmName": "test04",
    "keycloakUsername": "ssouser",
    "keycloakPassword": "ssopass",
    "keycloakUrl": "https://keycloak_mima.com",
    "growiUrl": "https://growimima.com",
    "growiUsername": "username",
    "growiName": "name",
    "growiEmail": "email@gmail.com",
    "growiPassword": "password"
}
```
### keycloakに関する設定 ###
* realmName

にkeycloakに作成するRealmの名前を設定してください。
* keycloakUsername
* keucloakPassword

にそれぞれSAML認証のためのusernameとpasswordをそれぞれ設定してください。
* keycloakUrl

にkeycloakのurlを設定してください。


### growiに関する設定 ###
* growiUrl

にgrowiのurlを設定してください。
* growiUsername
* growiName
* growiEmail
* growiPassword

ではgrowiのアカウントのusername, name, emailアドレス, passwordをそれぞれ設定してください。


## pythonの設定
pythonはDockerの公式イメージのpython3を使用しました。

`python-app/`の`Dockerfile`でpython3をコンテナ内で立ち上げ、`requirements.txt`で必要ないくつかのpythonのライブラリをインストールしています。

ターミナルでコンテナを立ち上げて、pythonが立ち上がっているコンテナ(ここではpython-app)へ`docker-compose exec python-app bash`で入って以下のようにpythonを実行してください。
```bash
docker-compose up -d
docker-compose exec python-app bash

python setjson.py
python setKeycloak.py 
python setGrowi.py
```
### 注意
GrowiでSAMLの設定をする際に、Keycloakのrealmに関するX.509証明書が必要になるので先に、KeycloakのSAML設定を行ってください。(python setKeycloak.pyをおこなってから、python setGrowi.pyをおこなってください。)

### setKeycloak.py

* `setKeycloak.py`のkeycloak_urlはdocker-compose.ymlでkeycloakを立ち上げているサービス名、ポート番号で設定してください。(ここでは、サービス名は'keyclaok', ポート番号は'8080')
* `create_realm()`, `create_client()`, `create_users()`関数でrealm, client, userを設定しています。
また、`get_cert()`, `write_realm_to_growijson(realmName)`でGrowiのSAML認証の設定に必要な設定を`growi/`下のjsonファイルに書き込むので、先にこちらを実行してください。


### setGrowi.py
* `setGrowi.py`でも同じように、以下のurlはdocker-compose.ymlでgrowiを立ち上げているサービス名、ポート番号で設定してください(ここでは、サービス名は'app', ポート番号は'3000')
* 初めて`setGrowi.py`を実行する際にはログインをする`set_login()`を実行する必要はありません。`set_install()`で初期設定が行われます。2回目からは`set_install()`ではなく`set_login()`でログインしてください。


# 参考

KeycloakとGrowiの設定は次の記事を参考にさせていただきました。[シングルサインオンサービスKeycloakとWikiシステムGrowiを連携する](https://qiita.com/myoshimi/items/f26cf3f179602a12a5ac)

ありがとうございます。




