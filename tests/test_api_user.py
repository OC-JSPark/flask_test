def test_get_user(client):
    r = client.get(
        '/api/users',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert len(r.json) == 1 ## response의 길이르 보자. conftest에서 userModel을 1개 넣었으므로 len은 1이 나올것이다.

def test_get_user(client,user_data):
    ## dummy data를 가져와서 넣은데이터와 일치하는지 확인
    r = client.get(
        '/api/users/1',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert r.json.get('user_id') == user_data.get('user_id')
    assert r.json.get('user_name') == user_data.get('user_name')

## 생성하는것.
def test_post_user(client,user_data):
    r = client.post(
        '/api/users',
        data=user_data
    )
    assert r.status_code == 409 ## user_id는 unique해야하니깐 장애가 나야한다.
    new_user_data = user_data.copy()
    new_user_data['user_id'] = 'tester2'

    r=client.post(
        '/api/users',
        data=new_user_data
    )
    assert r.status_code ==201