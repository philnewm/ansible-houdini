import os
import sidefx
import requests
import hashlib
import shutil


if __name__ == '__main__':

    # This service object retrieve a token using your Application ID and secret
    service = sidefx.service(
        access_token_url="https://www.sidefx.com/oauth2/application_token",
        client_id='your OAuth application ID',
        client_secret_key='your OAuth application secret',
        endpoint_url="https://www.sidefx.com/api/",
    )

    # Retrieve the latest production build available
    latest_release = service.download.get_daily_build_download(
        product='houdini', version='20.5', build='production', platform='linux')

    # Download the file
    local_filename = latest_release['filename']
    r = requests.get(latest_release['download_url'], stream=True)
    downloads_dir = "../"
    download_path = os.path.join(downloads_dir, local_filename)

    if r.status_code == 200:
        with open(download_path, 'wb') as file:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, file)
    else:
        raise Exception('Error downloading file!')

    # Verify the file checksum is matching
    file_hash = hashlib.md5()
    with open(download_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            file_hash.update(chunk)
    if file_hash.hexdigest() != latest_release['hash']:
        raise Exception('Checksum does not match!')