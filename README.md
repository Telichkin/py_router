# py_router

**py_router** is small and fast URL router for WSGI applications. 
It's small in both lines of code and features. 
All functionality and API presented below:

```python
import py_router

router = py_router.create(
    ('/users', 'handle_users'),
    ('/users/:user_id', 'handle_user'),
    ('/users/:user_id/posts', 'handle_user_posts'),
    ('/users/:user_id/posts/:post_id', 'handle_user_post'))


assert router('/users') == ('handle_users', {})
assert router('/users/42') == ('handle_user', {'user_id': '42'})
assert router('/users/84/posts') == ('handle_user_posts', {'user_id': '84'})
assert router('/users/168/posts/336') == ('handle_user_post', {'user_id': '168', 'post_id': '336'})

```


