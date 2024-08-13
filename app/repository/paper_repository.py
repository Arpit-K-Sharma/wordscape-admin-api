from typing import List, Dict
from bson import ObjectId
from app.config.db_config import database_erp

class PaperRepository:
    def __init__(self):
        self.collection = database_erp["paper"]

    async def find_all_papers(self) -> List[Dict]:
        papers = await self.collection.find().to_list(length=None)
        return papers

    async def create_paper(self, paper_dict: Dict) -> str:
        result = await self.collection.insert_one(paper_dict)
        return str(result.inserted_id)

    async def update_paper(self, paper_id: str, paper_update: Dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(paper_id)},
            {"$set": paper_update}
        )
        return result.modified_count > 0

    async def delete_paper(self, paper_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(paper_id)})
        return result.deleted_count > 0

    async def find_paper_by_id(self, paper_id: str) -> Dict:
        paper = await self.collection.find_one({"_id": ObjectId(paper_id)})
        return paper
