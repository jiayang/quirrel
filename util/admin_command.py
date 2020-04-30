DEV_IDS = [184002906981269505,178663053171228674]

def admin_only(func):
    async def inner(self, ctx, *args, **kwargs):
        if ctx.author.id not in DEV_IDS:
            return
        await func(self,ctx, *args, **kwargs)
        return
    return inner
