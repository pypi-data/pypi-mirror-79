from wedge.tests.mixins.testcase_mixin import TestCaseMixin


class TestGoogleRecaptchaService(TestCaseMixin):
    """
    verify_token
    """

    # TODO : need to merge w lib for mock_request

    # def test_verify_token_with_bad_token_raise_runtime_error(self):
    #     """ Ensure method raise RuntimeError """
    #     response = {
    #         "json_file": self.get_datasets_dir("recaptcha/bad_token.json"),
    #     }
    #
    #     match = "Failed to create procedure .*"
    #     with request_test_helper.mock_request(response, method="post"):
    #         with pytest.raises(RuntimeError, match=match):
    #             GoogleRecaptchaService.verify_token("bad_token")
