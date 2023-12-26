import json
import requests

with open('params.json') as f:
    j = json.load(f)
    realmName = j["realmName"]
    keycloakUsername = j["keycloakUsername"]
    keycloakPassword = j["keycloakPassword"]
    keycloakUrl = j["keycloakUrl"]
    growiUrl = j["growiUrl"]
    growiUsername = j["growiUsername"]
    growiName = j["growiName"]
    growiEmail = j["growiEmail"]
    growiPassword = j["growiPassword"]


# realm.jsonへ書き込む
def write_to_realm(realmName):
    with open("realm.json", "r") as json_file:
        data = json.load(json_file)

    data["id"] = realmName
    data["realm"] = realmName
  
    with open('realm.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)




# users.jsonへ書き込む
def write_to_users(keycloakUsername, keycloakPassword):
    with open("users.json", "r") as json_file:
        data = json.load(json_file)

    data["username"] = keycloakUsername
    
    if "credentials" in data and isinstance(data["credentials"], list):
        for credential in data["credentials"]:
            if credential.get("type") == "password":
                credential["value"] = keycloakPassword
  
    with open('users.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)





# createGrowiClient.jsonへ書き込む
def write_to_client(growiUrl):
    with open("createGrowiClient.json", "r") as json_file:
        data = json.load(json_file)

    data["rootUrl"] = growiUrl + "/"
    data["adminUrl"] = growiUrl + "/passport/saml/callback"

    if "redirectUris" in data and isinstance(data["redirectUris"], list):
        if len(data["redirectUris"]) > 0:
            data["redirectUris"][0] = growiUrl + "/*"
    
    data["attributes"]["saml_assertion_consumer_url_redirect"] = growiUrl + "/passport/saml/callback"
    data["attributes"]["saml_assertion_consumer_url_poset"] = growiUrl + "/"
    data["attributes"]["saml_single_logout_service_url_redirect"] = growiUrl + "/passport/saml/callback"
  
    with open('createGrowiClient.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)





# growiSaml.jsonへ書き込む
def write_to_growisaml(keycloakUrl):
    with open("growiSaml.json", "r") as json_file:
        data = json.load(json_file)

    data["entryPoint"] = keycloakUrl + "/auth/realms/" + realmName + "/protocol/saml"
  
    with open('growiSaml.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)



# growiSiteUrl.jsonへ書き込む
def write_to_growisite(growiUrl):
    with open("growisiteUrl.json", "r") as json_file:
        data = json.load(json_file)

    data["siteUrl"] = growiUrl
  
    with open('growsSiteUrl.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)



# growiinsData.jsonへ書き込む
def write_to_growiins(growiUsername, growiName, growiEmail, growiPassword):
    with open("growiinsData.json", "r") as json_file:
        data = json.load(json_file)

    data["registerForm"]["username"] = growiUsername
    data["registerForm"]["name"] = growiName
    data["registerForm"]["email"] = growiEmail
    data["registerForm"]["password"] = growiPassword
  
    with open('growiinsData.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


# growilogData.jsonへ書き込む
def write_to_growilog(growiUsername, growiPassword):
    with open("growilogData.json", "r") as json_file:
        data = json.load(json_file)

    data["loginForm"]["username"] = growiUsername
    data["loginForm"]["password"] = growiPassword
  
    with open('growilogData.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)







write_to_realm(realmName)
write_to_users(keycloakUsername, keycloakPassword)
write_to_client(growiUrl)
write_to_growisaml(keycloakUrl)
write_to_growisite(growiUrl)
write_to_growiins(growiUsername, growiName, growiEmail, growiPassword)
write_to_growilog(growiUsername, growiPassword)