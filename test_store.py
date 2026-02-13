from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
def test_patch_order_by_id():
    # Step 1: Create an order for an available pet (pet_id 2 - 'flippy')
    create_order_endpoint = "/store/order"
    order_data = {
        "pet_id": 2
    }

    create_response = api_helpers.post_api_data(create_order_endpoint, order_data)

    # Validate POST response code
    assert_that(create_response.status_code, is_(201))

    # Validate order creation response against schema
    created_order = create_response.json()
    validate(instance=created_order, schema=schemas.order)

    order_id = created_order['id']
    pet_id = created_order['pet_id']

    # Step 2: Update the order status to 'sold' using PATCH
    patch_order_endpoint = f"/store/order/{order_id}"
    update_data = {
        "status": "sold"
    }

    patch_response = api_helpers.patch_api_data(patch_order_endpoint, update_data)

    # Validate PATCH response code
    assert_that(patch_response.status_code, is_(200))

    # Validate the response message
    patch_result = patch_response.json()
    assert_that(patch_result['message'], is_("Order and pet status updated successfully"))

    # Step 3: Verify the pet's status was correctly updated
    get_pet_endpoint = f"/pets/{pet_id}"
    pet_response = api_helpers.get_api_data(get_pet_endpoint)

    assert_that(pet_response.status_code, is_(200))

    updated_pet = pet_response.json()
    assert_that(updated_pet['status'], is_("sold"))
