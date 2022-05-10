import pytest
import construct.dummy as dummy


# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_lock_poc/lambda_lock_poc_stack.py
@pytest.mark.unit
def test_sqs_queue_created():
    assert dummy.dummy(True) == 1
    assert dummy.dummy(False) == 2
