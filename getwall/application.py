"""Application module."""
import logging
from typing import List

import httpx
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, FastAPI, HTTPException

from .containers import Container
from .models import Comment, CommentList, Post, PostAndComments
from .services import Service

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

POSTS_API_URL = "https://jsonplaceholder.typicode.com/posts"
COMMENTS_API_URL = "https://jsonplaceholder.typicode.com/comments"

app = FastAPI()


@app.api_route("/post_with_comments/{post_id}")
@inject
async def get_post_with_comments(
    post_id: int, cache: Service = Depends(Provide[Container.service])
):
    key = f"post_with_comments:{post_id}"
    post_with_comments_from_cache = await cache.get(key)
    if not post_with_comments_from_cache:
        post_with_comments = await fetch_post_with_comments(post_id)
        await cache.set(key, post_with_comments.json())
        log.info("update the key in cache: %s", key)
        return post_with_comments
    return PostAndComments.parse_raw(post_with_comments_from_cache)


async def fetch_post_with_comments(post_id: int) -> PostAndComments:
    post = await get_post(post_id)
    comments = await get_post_comments(post_id)
    return PostAndComments(post=post, comments=comments)


async def get_post(post_id: int) -> Post:
    async with httpx.AsyncClient() as client:
        raw_post = await client.get(f"{POSTS_API_URL}/{post_id}")
        if raw_post.json():
            return Post.parse_obj(raw_post.json())
        raise HTTPException(status_code=404, detail="Post not found")


async def get_post_comments(post_id: int) -> List[Comment]:
    # NOTE: can we get all comments partially?.. No, cause we have a regular endpoint for comments
    async with httpx.AsyncClient() as client:
        raw_comments = await client.get(COMMENTS_API_URL)
        if raw_comments.json():
            comments = CommentList.parse_obj(raw_comments.json())
            return [
                comment for comment in comments.__root__ if comment.postId == post_id
            ]
        return []


# NOTE: Add an endpoint to
# get all posts and comments, and in this case update values for each post in a cache

container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost")
container.config.redis_password.from_env("REDIS_PASSWORD", "password")
container.wire(modules=[__name__])
