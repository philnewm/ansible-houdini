import click
import json
import os
import sidefx


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("client_id", type=click.STRING, default=os.environ.get("SIDEFX_CLIENT_ID"))
@click.argument("client_secret_key", type=click.STRING, default=os.environ.get("SIDEFX_CLIENT_SECRET_KEY"))
@click.argument("product", type=click.STRING, default="houdini")
@click.argument("version", type=click.STRING, default="21.0")
@click.argument("platform", type=click.STRING, default="linux")
@click.argument("production_only", type=click.BOOL, default=True)
@click.argument("build_number", type=click.STRING, default="")
def get_build_url(
    client_id: str,
    client_secret_key: str,
    product: str = "houdini",
    version: str = "21.0",
    platform: str = "linux",
    production_only: bool = True,
    build_number: str = "",
    ) -> dict[str, str] | None:

    service = sidefx.service(
        client_id=client_id,
        client_secret_key=client_secret_key,
    )

    if not build_number:
        build_list: list[dict[str, str]] = service.download.get_daily_builds_list(
            product=product,
            version=version,
            platform=platform,
            only_production=production_only,
            )

        if not build_list:
            click.echo(f"No results found for version {version}")
            exit(1)

        build_number = build_list[0]["build"]

    result: dict[str, str] =  service.download.get_daily_build_download(
        product=product,
        version=version,
        build=build_number,
        platform=platform,
        )
    click.echo(json.dumps(result))
    return result


@cli.command()
@click.argument("client_id", type=click.STRING, default=os.environ.get("SIDEFX_CLIENT_ID"))
@click.argument("client_secret_key", type=click.STRING, default=os.environ.get("SIDEFX_CLIENT_SECRET_KEY"))
@click.argument("server_name", type=click.STRING, default="")
@click.argument("server_code", type=click.STRING, default="")
@click.argument("version", type=click.STRING, default="")
@click.argument("products", type=click.STRING, default="HOUDINI-NC;RENDER-NC")
def get_non_commercial_license_key(
        client_id: str,
        client_secret_key: str,
        server_name: str = "",
        server_code: str = "",
        version: str = "",
        products: str = "HOUDINI-NC;RENDER-NC",
    ) -> None:

    service = sidefx.service(
        client_id=client_id,
        client_secret_key=client_secret_key,
    )

    license_strings = service.license.get_non_commercial_license(
        server_name=server_name,
        server_code=server_code,
        version=version,
        products=products,
    )

    click.echo(json.dumps(license_strings["license_keys"]))

if __name__ == "__main__":
    cli()
