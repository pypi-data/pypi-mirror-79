from typing import Dict, Any, List, IO, Optional, Union

from .utils.service_utils import create_body_list, path_exists, regenerate_credentials
from .utils.export_utils import Export

from datetime import datetime


class SearchAnalytics:
    def __init__(self, service, credentials) -> None:
        self.service = service
        self.credentials = credentials
        self.data = {}
        self.body = {
            "startRow": 0,
            "rowLimit": 25000,
        }

    def update_body(self, body) -> None:
        """
        Updates the body, that we are going to use in the query
        """

        self.body.update({k: v for k, v in body.items()})

    @regenerate_credentials
    def query(self, url: str) -> None:
        """
        Just a simplified wrapper to the searchanalytics
        """

        self.data.update(
            self.service.searchanalytics().query(siteUrl=url, body=self.body).execute()
        )

    def date(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
        days: Optional[int] = None,
    ) -> None:
        pass

    def dimensions(self, *dimensions: List[str]) -> None:
        pass

    def search_type(self, search_type: str) -> None:
        pass

    def row_limit(self, limit: int) -> None:
        pass

    def start_row(self, start_row: int) -> None:
        pass

    def filters(
        self,
        dimension: List[str],
        expression: List[str],
        operator: Optional[List[str]] = None,
    ):
        pass

    def concurrent_query_asyncio(self, url: str):
        """
        Run queries concurrently.
        """

        import asyncio

        bodies = create_body_list(self.body)

        async def con_query(body):
            self.data.update(
                self.service.searchanalytics().query(siteUrl=url, body=body).execute()
            )

        async def main():
            await asyncio.gather(*[con_query(body) for body in bodies])

        asyncio.run(main())

    def concurrent_query_threadpool(self, url: str) -> None:

        from concurrent.futures import ThreadPoolExecutor

        bodies = create_body_list(self.body)

        @timeit
        def send_request(body):
            self.data.update(
                self.service.searchanalytics().query(siteUrl=url, body=body).execute()
            )

        def run_io_tasks_in_parallel(tasks):
            with ThreadPoolExecutor(max_workers=4) as executor:
                running_tasks = [executor.submit(task) for task in tasks]

        run_io_tasks_in_parallel([send_request(body) for body in bodies])

    def sites(self, url: Union[None, str] = None):
        """
        List all the web sites associated with the account.

        Info: https://developers.google.com/resources/api-libraries/documentation/webmasters/v3/python/latest/webmasters_v3.sites.html
        """

        if url:
            self.data.update(self.service.sites().get(siteUrl=url).execute())

        else:
            self.data.update(self.service.sites().list().execute())

    def sitemaps(self, url: str, feedpath: Union[None, str] = None):
        """
        Lists the sitemaps-entries submitted for the given site.

        Info: https://developers.google.com/resources/api-libraries/documentation/webmasters/v3/python/latest/webmasters_v3.sitemaps.html
        """

        if url and feedpath:
            self.data.update(
                self.service.sitemaps().get(siteUrl=url, feedpath=feedpath).execute()
            )

        elif url:
            self.data.update(self.service.sitemaps().list(siteUrl=url).execute())

    def export(
        self,
        export_type: Union[None, str] = None,
        url: Union[None, str] = None,
        command: Union[None, str] = None,
    ) -> None:
        """
        Specify the export type.
        """

        export_data = Export(self.data)

        if export_type == "csv":
            export_data.export_to_csv(
                filename=self._create_filename(
                    url=url, command=command, filetype=export_type
                )
            )

        if export_type == "json":
            export_data.export_to_json(
                filename=self._create_filename(
                    url=url, command=command, filetype=export_type
                )
            )

        if export_type == "excel":
            export_data.export_to_excel(
                filename=self._create_filename(
                    url=url, command=command, filetype="xlsx"
                )
            )

        if export_type == "tsv":
            export_data.export_to_tsv(
                filename=self._create_filename(url=url, command=command, filetype="tsv")
            )

        if not export_type or export_type == "table":
            export_data.export_to_table()

    def _create_filename(self, url: str, command: str, filetype: str) -> str:
        """
        Creates a file name from timestamp, url and command.
        """

        from datetime import datetime

        def __clean_url(url: str) -> str:
            for t in (
                ("https", ""),
                ("http", ""),
                (":", ""),
                ("sc-domain", ""),
                ("//", ""),
                ("/", "-"),
                ("--", "-"),
                (".", "-"),
                (",", "-"),
            ):
                url = url.lower().replace(*t)

            return url

        def __create_name(file_exists: bool = False) -> str:
            from random import randint

            if not file_exists:
                return "-".join(
                    [
                        __clean_url(url) or "sites",
                        command,
                        datetime.now().strftime("%d-%B-%Y-%H-%M") + f".{filetype}",
                    ]
                )
            return "-".join(
                [
                    __clean_url(url) or "sites",
                    command,
                    f"report-{randint(1,10000)}",
                    datetime.now().strftime("%d-%B-%Y-%H-%M") + f".{filetype}",
                ]
            )

        return (
            __create_name()
            if not path_exists(__create_name())
            else __create_name(file_exists=True)
            if not path_exists(__create_name(file_exists=True))
            else __create_name(file_exists=True)
        )

