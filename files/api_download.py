import click
import hashlib
import json
import os
import requests
import shutil
import sidefx


ACCESS_TOKEN_URL = "https://www.sidefx.com/oauth2/application_token"
ENDPOINT_URL = "https://www.sidefx.com/api/"
PRODUCTS_TO_INSTALL = "HOUDINI-NC;RENDER-NC"


@click.group()
def cli() -> None:
    pass

@cli.command()
@click.argument("client_id", type=click.STRING)
@click.argument("client_secret_key", type=click.STRING)
@click.argument("version", type=click.STRING)
@click.argument("production_only", type=click.BOOL)
def get_package_name(
    client_id: str,
    client_secret_key: str,
    version: str,
    production_only: bool,
    ) -> None:

    service = sidefx.service(
        access_token_url=ACCESS_TOKEN_URL,
        client_id=client_id,
        client_secret_key=client_secret_key,
        endpoint_url=ENDPOINT_URL,
    )

    releases_list = service.download.get_daily_builds_list(
        product='houdini',
        version=version,
        platform='linux',
        only_production=production_only,
        )

    latest_release: dict[str, str] = releases_list[0]
    h_version: str = latest_release['version']
    h_build: str = latest_release["build"]
    h_platform: str = latest_release["platform"]

    click.echo(f"houdini-{h_version}.{h_build}-{h_platform}.tar.gz")


@cli.command()
@click.argument("client_id", type=click.STRING)
@click.argument("client_secret_key", type=click.STRING)
@click.argument("version", type=click.STRING)
@click.argument("build_number", type=click.STRING)
@click.argument("package_dir", type=click.STRING)
def get_setup(
    client_id: str,
    client_secret_key: str,
    version: str,
    build_number: str,
    package_dir: str
    ) -> None:

    service = sidefx.service(
        access_token_url=ACCESS_TOKEN_URL,
        client_id=client_id,
        client_secret_key=client_secret_key,
        endpoint_url=ENDPOINT_URL,
    )

    latest_release = service.download.get_daily_build_download(
        product='houdini',
        version=version,
        build=build_number,
        platform='linux',
        )

    local_filename = latest_release['filename']
    result = requests.get(latest_release['download_url'], stream=True)
    downloads_dir = package_dir
    download_path = os.path.join(downloads_dir, local_filename)

    if result.status_code == 200:
        with open(download_path, 'wb') as file:
            result.raw.decode_content = True
            shutil.copyfileobj(result.raw, file)

    else:
        raise Exception('Error downloading file!')

    # Verify the file checksum is matching
    file_hash = hashlib.md5()
    with open(download_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            file_hash.update(chunk)

    if file_hash.hexdigest() != latest_release['hash']:
        raise Exception('Checksum does not match!')

    click.echo(download_path)


@cli.command()
@click.argument("client_id", type=click.STRING)
@click.argument("client_secret_key", type=click.STRING)
@click.argument("server_name", type=click.STRING)
@click.argument("server_code", type=click.STRING)
@click.argument("version", type=click.STRING)
def get_non_commercial_license_key(
        client_id: str,
        client_secret_key: str,
        server_name: str,
        server_code: str,
        version: str
    ) -> None:

    service = sidefx.service(
        access_token_url=ACCESS_TOKEN_URL,
        client_id=client_id,
        client_secret_key=client_secret_key,
        endpoint_url=ENDPOINT_URL,
    )

    license_strings = service.license.get_non_commercial_license(
        server_name=server_name,
        server_code=server_code,
        version=version,
        products=PRODUCTS_TO_INSTALL,
    )

    click.echo(json.dumps(license_strings["license_keys"], indent=2))

if __name__ == "__main__":
    cli()
