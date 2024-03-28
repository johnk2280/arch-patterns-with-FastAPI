class FakeSession:
    committed: bool = False

    async def commit(self) -> None:
        self.committed = True
