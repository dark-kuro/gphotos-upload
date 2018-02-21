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
    # # print(args)
    api = uphotos.login(args)
    while 1:
        try:
            inp = input('Enter dir: ')
            # inp = inp.strip()
            args.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), inp)
            if not os.path.isdir(args.path):
                print('Not dir')
                raise Exception
            # api = ''

            upload_media(args, api)
            print(args.path)
        except Exception as e:
            print('ERROR:', e)
            pass
        


if __name__ == '__main__':
    main()
