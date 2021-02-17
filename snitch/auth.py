
import argparse

from google_auth_oauthlib.flow import InstalledAppFlow


SCOPE = "https://www.googleapis.com/auth/adwords"


def main(client_secrets_path, scopes):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_path, scopes=scopes
    )

    flow.run_local_server()

    print("Access token: %s" % flow.credentials.token)
    print("Refresh token: %s" % flow.credentials.refresh_token)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates OAuth 2.0 credentials with the specified "
        "client secrets file."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "--client_secrets_path",
        required=True,
        help=(
            "Path to the client secrets JSON file from the "
            "Google Developers Console that contains your "
            "client ID and client secret."
        ),
    )
    parser.add_argument(
        "--additional_scopes",
        default=None,
        help=(
            "Additional scopes to apply when generating the "
            "refresh token. Each scope should be separated "
            "by a comma."
        ),
    )
    args = parser.parse_args()

    configured_scopes = [SCOPE]

    if args.additional_scopes:
        configured_scopes.extend(
            args.additional_scopes.replace(" ", "").split(",")
        )

    main(args.client_secrets_path, configured_scopes)
