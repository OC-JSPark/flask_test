def test_auth(client):
    r= client.get(
        '/auth/register',
        follow_redirects=True   ## 페이지가 redirection 될때 그걸 따라가겠다. 그리고 따라간 page의 response 값을 가져오겠다는 의미. get에 대한 response는 302가 떨어지는 경우도 많다. 그래서 그걸 이용하지 말고 최종적으로 도달한 request의 return값을 이용하기 위해서이다.

    )
    ## 검증할때는 assert 라고 붙이면 좋다.
    assert r.status_code == 200

    r = client.get(
        '/auth/login',
        follow_redirects= True
    )
    assert r.status_code == 200

    r = client.get(
        '/auth/logout',
        follow_redirects= True
    )
    assert r.status_code == 200

    r = client.get(
        '/auth',
        follow_redirects= True
    )
    assert r.status_code == 200

## index page도 만들어보자.
def test_base(client):
    r = client.get(
        '/',
        follow_redirects=True
    )
    assert r.status_code == 200