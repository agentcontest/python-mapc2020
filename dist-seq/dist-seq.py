import aiohttp.web
import itertools
import urllib.parse

from tinyhtml import h, frag

routes = aiohttp.web.RouteTableDef()

class Group:
    def __init__(self):
        self.assigned = {}

    def assign(self, uuid):
        if uuid not in self.assigned:
            used = set(self.assigned.values())
            for i in itertools.count(1):
                if i not in used:
                    break
            self.assigned[uuid] = i
        return self.assigned[uuid]

    def unassign(self, uuid):
        self.assigned.pop(uuid, None)

groups = {}

@routes.post("/dist-seq/{group}/{uuid}")
async def assign(req):
    group = req.match_info["group"]
    uuid = req.match_info["uuid"]
    if group not in groups:
        groups[group] = Group()
    return aiohttp.web.Response(text=str(groups[group].assign(uuid)))

@routes.get("/dist-seq/{group}")
async def view(req):
    try:
        group = groups[req.match_info["group"]]
    except KeyError:
        raise aiohttp.web.HTTPNotFound()

    return aiohttp.web.Response(content_type="text/html", text=frag(
        h("table", border="1")(
            h("tr")(
                h("td")(key),
                h("td")(val),
                h("td")(
                    h("form", method="POST")(
                        h("input", type="hidden", name="unassign", value=key),
                        h("input", type="submit", value="unassign"),
                    ),
                ),
            ) for key, val in sorted(group.assigned.items(), key=lambda item: item[1])
        ),
        h("a", href="/dist-seq/")("list groups"),
    ).render())

@routes.post("/dist-seq/{group}")
async def delete(req):
    try:
        group = groups[req.match_info["group"]]
    except KeyError:
        raise aiohttp.web.HTTPNotFound()

    body = await req.post()
    if "unassign" in body:
        group.unassign(body["unassign"])

    return await view(req)

@routes.get("/dist-seq/")
async def list(req):
    return aiohttp.web.Response(content_type="text/html", text=frag(
        h("ul")(
            h("li")(
                h("a", href=f"/dist-seq/{urllib.parse.quote(group, safe='')}")(group)
            ) for group in groups
        ),
        h("form", method="POST")(
            h("input", type="hidden", name="reset", value="1"),
            h("input", type="submit", value="reset all")
        ),
    ).render())

@routes.post("/dist-seq/")
async def reset(req):
    body = await req.post()
    if "reset" in body:
        groups.clear()

    return await list(req)

if __name__ == "__main__":
    app = aiohttp.web.Application()
    app.router.add_routes(routes)
    aiohttp.web.run_app(app, host="127.0.0.1", port=12301)
