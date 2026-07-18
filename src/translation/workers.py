import asyncio


class TranslationWorker:
    def __init__(self, translator, provider, semaphore):
        self.translator = translator
        self.provider = provider
        self.semaphore = semaphore

    async def translate(self, batch):
        async with self.semaphore:
            return await asyncio.to_thread(self.translator._translate_batch, batch, self.provider)
