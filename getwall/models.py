from typing import List

from pydantic import BaseModel


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str


class CommentList(BaseModel):
    __root__: List[Comment]


class PostAndComments(BaseModel):
    post: Post
    comments: List[Comment]
