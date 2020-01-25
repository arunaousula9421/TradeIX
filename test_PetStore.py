import json
import requests
import jsonpath


def test_pet_store():
    id = 0

    def test_add_new_pet():
        global id
        app_url = "https://petstore.swagger.io/v2/pet"
        header = {'content-type': 'application/json'}
        file = open('add_new_petstore.json', 'r')
        request_json = json.loads(file.read())
        response = requests.post(app_url, data=json.dumps(request_json), headers=header)
        id = jsonpath.jsonpath(response.json(), 'id')
        id = id[0]
        response_body = response.json()
        assert response.status_code == 200
        assert response_body['name'] == 'doggie'

    def test_update_pet_name():
        global id
        update_app_url = "https://petstore.swagger.io/v2/pet/" + str(id)
        header = {'accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded'}
        data = {'name': 'snoopies', 'status': 'available'}
        response = requests.post(update_app_url, data=data, headers=header)
        assert response.status_code == 200

    def test_get_verify_updated_pet_details():
        global id
        get_app_url = "https://petstore.swagger.io/v2/pet/" + str(id)
        header = {'accept': 'application/json'}
        response = requests.get(get_app_url, headers=header)
        response_body = response.json()
        assert response.status_code == 200
        assert response_body['name'] == 'snoopies'
        assert response_body['status'] == 'available'

    def test_delete_pet_details():
        global id
        get_app_url = "https://petstore.swagger.io/v2/pet/" + str(id)
        header = {'accept': 'application/json'}
        response = requests.delete(get_app_url, headers=header)
        assert response.status_code == 200

    def test_verify_deleted_pet_details():
        global id
        get_app_url = "https://petstore.swagger.io/v2/pet/" + str(id)
        header = {'accept': 'application/json'}
        response = requests.get(get_app_url, headers=header)
        assert response.status_code == 404

    test_add_new_pet()
    test_update_pet_name()
    test_get_verify_updated_pet_details()
    test_delete_pet_details()
    test_verify_deleted_pet_details()
