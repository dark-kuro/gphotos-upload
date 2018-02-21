import logging
import os
import io

class Service:
    def __init__(self, http, logger):
        self.http = http
        self.logger = logger.getChild('service')

        self.photos_already_online = None

        # make "requests" log the same as our logger
        requests_log = logging.getLogger('requests')
        requests_log.setLevel(self.logger.level)
        for handler in self.logger.handlers:
            requests_log.addHandler(handler)

    def ensure_file_uploaded(self, path, full_quality = False):
        if not self.file_is_uploaded(path):
            self.upload_file_with_quality(path, full_quality)

    def upload_file_with_quality(self, path, full_quality):
        if full_quality:
            # self.upload_file_full_quality(path)
            print('Not implemenrted')
        else:
            self.upload_file_high_quality(path)


    def upload_file_high_quality(self, path):
        with open(path, 'rb') as f:
            self.upload_file_data(path, f)

    def upload_file_data(self, path, data):
        slug = os.path.basename(path)
        n_bytes = data.seek(-1, io.SEEK_END)
        data.seek(0)
        print('Uploading %s' % slug)

        self.logger.info('Uploading %s' % slug)
        response = self.http.post(
            'https://picasaweb.google.com/data/feed/api/user/default/albumid/default',
            headers = {
                'Slug': str(slug),
                'Content-Type': 'image/jpeg',
                'Content-Length': str(n_bytes),
            },
            data = data
        )
        if response.status_code != 201:
            print(response.text)
            response.raise_for_status()


    def file_is_uploaded(self, path):
        if not self.photos_already_online:
            self.photos_already_online = self.load_photos_already_online()

        key = self.unique_key_for_path(path)
        exists = key in self.photos_already_online
        exists_words = 'is already'
        if not exists:
            exists_words = 'is not yet'
        self.logger.info('%s %s online, last we checked' % (key, exists_words))

        return exists


    def load_photos_already_online(self):
        self.logger.info('Loading existing-photo list from Google Photos (to make sure we do not upload duplicates)')
        response = self.http.get('https://picasaweb.google.com/data/feed/api/user/default', params = {
            'kind': 'photo',
            'alt': 'json',
            'fields': 'entry(title)',
            'max-results': '999999999'
        })

        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()

        json = response.json()

        return set([ e['title']['$t'] for e in json['feed']['entry'] ])

    def unique_key_for_path(self, path):
        basename = os.path.basename(path)
        return basename