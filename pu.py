import uphotos
# from pprint import pformat
import os
from googleapiclient.discovery import build
import google.oauth2.credentials

def upload_media(args, api, full_quality = False):
	for i in uphotos.walk(args.path):
		print(i)
		api.ensure_file_uploaded(i, full_quality = full_quality)

def main():
    parser = uphotos.parser()
    
    parser.add_argument('path', 
    	metavar='PATH', 
    	help='Path to directory containing Pictures files', 
    	nargs='?', 
    	default='.')
    args = parser.parse_args()
    # print(args)
    api = uphotos.login(args)
    # credentials = google.oauth2.credentials.Credentials(api.http)
    # print('credentials', vars(credentials))
    # drive = build('drive', 'v3', credentials=credentials)
    # upload_media(args, api)
    # c = api.http
    # print(dir(c))
    # print(dir(api.http))
    # api.http._client='jj'
    # credentials
    # print
    # print((api.http))
    # print((api.http._scopes))
    # print((api.http.refresh_token))
    # response = api.http.get()
    # .from_client_secrets_file()
    # print(vars(response))

    # rrr=response.oauth2session
    # rrr._client = response.client_config['client_id']
    api = api.http
    response = api.get('https://picasaweb.google.com/data/feed/api/user/default')
    print('response', vars(response))
    # print(vars(.get()))
    # response.authorized_session(client_id="")


if __name__ == '__main__':
    main()
