from typing import Optional


class Storage:
	async def query(self, key: int) -> Optional[dict]:
		pass

	async def insert(self, key: int, content: dict) -> bool:
		pass

	async def update(self, key: int, content: dict) -> Optional[dict]:
		pass


class InMemoryStore(Storage):

	storage: dict = {}

	async def query(self, key: int) -> Optional[dict]:
		if key in self.storage:
			return self.storage[key]
		else:
			return None

	async def insert(self, key: int, content: dict) -> bool:
		if key in self.storage:
			return False
		else:
			self.storage[key] = content
			return True

	async def update(self, key: int, content: dict) -> Optional[dict]:
		if key not in self.storage:
			return None
		self.storage[key].update(content)
		return self.storage[key]
