from nose.tools import *
from unittest import TestCase
from unittest.mock import patch
from factom_sdk.utils.key_util import KeyUtil


class TestKeyUtil(TestCase):
    def test_create_key_pair(self):
        """Check create key pair"""
        key_pair = KeyUtil.create_key_pair()
        assert_true('private_key' in key_pair)
        assert_true('public_key' in key_pair)

    def test_validate_checksum(self):
        """Check validate checksum"""
        key_passing = KeyUtil.validate_check_sum()
        assert_false(key_passing)
        key_bytes_length_match = KeyUtil.validate_check_sum({'signer_key': 'idpub2'})
        assert_false(key_bytes_length_match)
        key_valid = KeyUtil.validate_check_sum(
            {'signer_key': 'idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zH12'})
        assert_false(key_valid)
        key_valid = KeyUtil.validate_check_sum(
            {'signer_key': 'idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9'})
        assert_true(key_valid)

    def test_get_invalid_keys(self):
        """Check get invalid keys"""
        missing_key = KeyUtil.get_invalid_keys()
        assert_equal(missing_key, [])
        errors = [
            {
                'key': '123',
                'error': 'key is invalid',
            },
            {
                'key': '123',
                'error': 'key is invalid',
            },
        ]
        errors_key = KeyUtil.get_invalid_keys({'signer_keys': ['123', '123']})
        assert_equal(errors_key, errors)
        errors_key = KeyUtil.get_invalid_keys(
            {'signer_keys':
                ['idpub2FEZg6PwVuDXfsxEMinnqVfgjuNS2GzMSQwJgTdmUFQaoYpTnv',
                 'idpub1tkTRwxonwCfsvTkk5enWzbZgQSRpWDYtdzPUnq83AgQtecSgc']
             })
        assert_equal(errors_key, [])

    def test_get_duplicate_keys(self):
        """Check get duplicate keys"""
        missing_keys = KeyUtil.get_duplicate_keys();
        assert_equal(missing_keys,[])
        errors = [
            {
                'key': '123',
                'error': 'key is duplicated, keys must be unique.',
            },
        ]
        key_errors = KeyUtil.get_duplicate_keys({'signer_keys': ['123', '123']})
        assert_equal(errors, key_errors)

    def test_get_key_bytes_from_key(self):
        """Check get key bytes from key"""
        with assert_raises(Exception) as cm:
            KeyUtil.get_key_bytes_from_key({'signer_key': ''})
            assert_true('key is invalid.' in str(cm.exception))
        valid_key_bytes = KeyUtil.get_key_bytes_from_key(
            {'signer_key': 'idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9'})
        assert_true(isinstance(valid_key_bytes, bytes))

    def test_get_public_key_from_private_key(self):
        """Check get public key from private key"""
        with assert_raises(Exception) as cm:
            KeyUtil.get_public_key_from_private_key({'signer_private_key': 'idsec2'})
            assert_true('signer_private_key is invalid.' in str(cm.exception))
        public_key = KeyUtil.get_public_key_from_private_key(
            {'signer_private_key': 'idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6'})
        assert_equal(public_key, b'idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9')

    def test_sign_content(self):
        """Check sign content"""
        with assert_raises(Exception) as cm:
            KeyUtil.sign_content()
            assert_true('signer_private_key is required.' in str(cm.exception))
        with assert_raises(Exception) as cm:
            KeyUtil.sign_content({'signer_private_key': 'idsec2'})
            assert_true('signer_private_key is invalid.' in str(cm.exception))
        with assert_raises(Exception) as cm:
            KeyUtil.sign_content(
                {'signer_private_key': 'idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6'})
            assert_true('message is required.' in str(cm.exception))
        signature = KeyUtil.sign_content(
                {'signer_private_key': 'idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6',
                 'message': 'Abc'})
        assert_equal(signature,
                     b'Z4qvla16B9+gW/IFyng+5Q0njgwT2aRr5kmYMARRbT8+nivUiQO74O/y3MOH42R9cqTdkXkETLDitUO48DviBw==')

    def test_validate_signature(self):
        """Check validate signature"""
        with assert_raises(Exception) as cm:
            KeyUtil.validate_signature()
            assert_true('signer_public_key is required.' in str(cm.exception))
        with assert_raises(Exception) as cm:
            KeyUtil.validate_signature({'signer_public_key': 'idpub2'})
            assert_true('signer_public_key is invalid.' in str(cm.exception))
        with assert_raises(Exception) as cm:
            KeyUtil.validate_signature(
                {'signer_public_key': 'idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9'})
            assert_true('signature is required.' in str(cm.exception))
        with assert_raises(Exception) as cm:
            KeyUtil.validate_signature(
                {'signer_public_key': 'idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9',
                 'signature': 'D+lzNLb88IKXQk2BglvP7o6yK/DNAsO1B9qXdqArvrotTqSCI4Y4d8J8bwbfAyCvJT9tLYj9Ll7grCnyDWVtCg=='
                 })
            assert_true('message is required.' in str(cm.exception))
        valid_signature = KeyUtil.validate_signature(
                {'signer_public_key': 'idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9',
                 'signature': 'Z4qvla16B9+gW/IFyng+5Q0njgwT2aRr5kmYMARRbT8+nivUiQO74O/y3MOH42R9cqTdkXkETLDitUO48DviBw==',
                 'message': 'Abc'
                 })
        assert_true(valid_signature)
        invalid_signature = KeyUtil.validate_signature(
            {'signer_public_key': 'idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9',
             'signature': 'Z4qvla16B9+gW/IFyng+5Q0njgwT2aRr5kmYMARRbT8+nivUiQO74O/y3MOH42R9cqTdkXkETLDitUO48DviBw==',
             'message': 'Abcd'
             })
        assert_false(invalid_signature)




