from asyncio import gather
from notion_client import AsyncClient
from utils import get_env


API_KEY: str = get_env("NOTION_API_TOKEN")
DATABASE_ID: str = get_env("NOTION_DATABASE_ID")


class Notion:
    """Notion Integration Class
    """

    def __init__(self) -> None:
        self.async_client = AsyncClient(auth=API_KEY)

    async def get_notion_database_page_ids(self, query: dict = None):
        """Get filtered pages ID from tasks database.
        """

        all_responses = []
        params = {"database_id": DATABASE_ID, "filter": query} if query else {"database_id": DATABASE_ID}

        try:
            query_response = await self.async_client.databases.query(**params)
            all_responses.append(query_response)

            while query_response.get("has_more", False):
                query_response = await self.async_client.databases.query(
                    **params, start_cursor=query_response["next_cursor"]
                )
                all_responses.append(query_response)

        except Exception as e:
            raise RuntimeError(f"Erro ao buscar páginas do Notion: {str(e)}")

        return [page["id"] for response in all_responses for page in response.get("results", [])]


    async def delete_pages(self, query: dict = None) -> None:
        """Archive pages of a database
        """

        page_ids = await self.get_notion_database_page_ids(query)
        if not page_ids:
            return 

        async def archive_page(page_id: str):
            try:
                await self.async_client.pages.update(page_id, archived=True)
            except Exception as e:
                print(f"Erro ao arquivar a página {page_id}: {str(e)}")

        await gather(*(archive_page(page_id) for page_id in page_ids))
