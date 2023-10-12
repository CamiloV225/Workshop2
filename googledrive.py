from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

""" google_credentials= 'dssds.json'

def auth():
    
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(google_credentials)


    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(google_credentials)
    else:
        gauth.Authorize()

    credentials = GoogleDrive(gauth)
    return credentials

def upload_file(path, id_folder):
    credentials=auth()
    archivo= credentials.CreateFile({'parents':[{'kind': 'drive#fileLink', 'id': id_folder}]})
    archivo['title']= path.split('/')[-1]
    archivo.SetContentFile(path)
    archivo.Upload()

if __name__ == "__main__":
    auth()
    upload_file() """