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
    while 1:
        try:
            inp = input('Enter dir: ')
            inp = inp.strip()
            args.path = inp
            upload_media(args, api)
        except:
            print('ERROR')
            pass
        


if __name__ == '__main__':
    main()
