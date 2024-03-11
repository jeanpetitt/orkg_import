from tsotsa import _ORKG
import argparse
from dotenv import load_dotenv
import os


def argsparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contribution", type=bool,
                        help="Create contributin", default=False)
    parser.add_argument("--contribution_and_comparison", type=bool,
                        help="Create contributin", default=True)
    parser.add_argument("--comparison", type=bool,
                        default=False, help="create comparison")
    parser.add_argument(
        '--json_path_contribution', type=str, help="Json template which help to create a contribution")
    parser.add_argument(
        '--paper_id', type=str, help="ORKG paper id")
    parser.add_argument(
        '--comparison_folder_path', type=str, help="Folder path that contain a list of json file form for the comparison")
    parser.add_argument(
        '--platform', type=str, help="platform name")
    args = parser.parse_args()
    return args


def set_api(args, orkg):
    if args.platform == "incubating":
        orkg.set_api("https://incubating.orkg.org/api")
    elif args.platform == "sandbox":
        orkg.set_api("https://sandbox.orkg.org/api")
    elif args.platform == "orkg":
        orkg.set_api("https://orkg.org/api")
    else:
        orkg.set_api("https://incubating.orkg.org/api")


if __name__ == '__main__':
    load_dotenv()
    token = os.environ["TOKEN"]
    args = argsparser()
    orkg = _ORKG()
    set_api(args=args, orkg=orkg)

    if args.contribution == True:
        args.comparison = False
        orkg.create_contribution(
            paper_id=args.paper_id, token=token, json_template=args.json_path_contribution)
    elif args.comparison == True:
        args.contribution = False
        orkg.create_dataframe_comparison(
            token=token, comparison_folder_path=args.comparison_folder_path)
    elif args.contribution_and_comparison == True:
        args.contribution = False
        args.comparison = False
        orkg._create_dataframe_comparison(
            token=token,
            paper_id=args.paper_id,
            comparison_folder_path=args.comparison_folder_path,
            template_contribution=args.json_path_contribution
        )

    else:
        print("No Process running")
