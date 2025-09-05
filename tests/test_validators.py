from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.html import avoid_wrapping

from upload_to.validators import MaxSizeValidator, MinSizeValidator


class MaxFileSizeValidatorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.validator = MaxSizeValidator(limit_value=1024)  # 1KB limit

    def test_valid_file_size(self):
        content = b"small file content"  # Less than 1KB
        uploaded_file = SimpleUploadedFile("test.txt", content)
        try:
            self.validator(uploaded_file)
        except ValidationError:
            self.fail("MaxFileSizeValidator raised ValidationError for valid file size")

    def test_invalid_file_size(self):
        content = b"x" * 2048  # 2KB, larger than 1KB limit
        uploaded_file = SimpleUploadedFile("test.txt", content)

        with self.assertRaises(ValidationError) as context:
            self.validator(uploaded_file)

        exception = context.exception
        code = exception.code
        message = str(exception.messages[0])
        self.assertEqual(code, "max_file_size")
        self.assertIn("less than", message)
        self.assertIn(avoid_wrapping("1.0 KB"), message)
        self.assertIn(avoid_wrapping("2.0 KB"), message)

    def test_exact_limit_size(self):
        content = b"x" * 1024  # Exactly 1KB
        uploaded_file = SimpleUploadedFile("test.txt", content)
        try:
            self.validator(uploaded_file)
        except ValidationError:
            self.fail(
                "MaxFileSizeValidator raised ValidationError for file at exact limit"
            )

    def test_callable_limit_value(self):
        validator = MaxSizeValidator(limit_value=lambda: 512)
        content = b"x" * 1024  # 1KB, larger than 512B limit
        uploaded_file = SimpleUploadedFile("test.txt", content)

        with self.assertRaises(ValidationError) as context:
            validator(uploaded_file)

        exception = context.exception
        code = exception.code
        message = str(exception.messages[0])
        self.assertEqual(code, "max_file_size")
        self.assertIn("less than", message)
        self.assertIn(avoid_wrapping("512 bytes"), message)
        self.assertIn(avoid_wrapping("1.0 KB"), message)


class MinFileSizeValidatorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.validator = MinSizeValidator(limit_value=100)  # 100 bytes minimum

    def test_valid_file_size(self):
        content = b"x" * 200  # 200 bytes, larger than 100 bytes limit
        uploaded_file = SimpleUploadedFile("test.txt", content)
        try:
            self.validator(uploaded_file)
        except ValidationError:
            self.fail("MinFileSizeValidator raised ValidationError for valid file size")

    def test_invalid_file_size(self):
        content = b"small"  # 5 bytes, smaller than 100 bytes limit
        uploaded_file = SimpleUploadedFile("test.txt", content)

        with self.assertRaises(ValidationError) as context:
            self.validator(uploaded_file)

        exception = context.exception
        code = exception.code
        message = str(exception.messages[0])
        self.assertEqual(code, "min_file_size")
        self.assertIn("greater than", message)
        self.assertIn(avoid_wrapping("100 bytes"), message)
        self.assertIn(avoid_wrapping("5 bytes"), message)

    def test_exact_limit_size(self):
        content = b"x" * 100  # Exactly 100 bytes
        uploaded_file = SimpleUploadedFile("test.txt", content)

        try:
            self.validator(uploaded_file)
        except ValidationError:
            self.fail(
                "MinFileSizeValidator raised ValidationError for file at exact limit"
            )

    def test_callable_limit_value(self):
        validator = MinSizeValidator(limit_value=lambda: 200)
        content = b"small"  # 5 bytes, smaller than 200 bytes limit
        uploaded_file = SimpleUploadedFile("test.txt", content)

        with self.assertRaises(ValidationError) as context:
            validator(uploaded_file)

        exception = context.exception
        code = exception.code
        message = str(exception.messages[0])
        self.assertEqual(code, "min_file_size")
        self.assertIn("greater than", message)
        self.assertIn(avoid_wrapping("200 bytes"), message)
        self.assertIn(avoid_wrapping("5 bytes"), message)

    def test_empty_file(self):
        uploaded_file = SimpleUploadedFile("test.txt", b"")

        with self.assertRaises(ValidationError) as context:
            self.validator(uploaded_file)

        exception = context.exception
        code = exception.code
        message = str(exception.messages[0])
        self.assertEqual(code, "min_file_size")
        self.assertIn("greater than", message)
        self.assertIn(avoid_wrapping("100 bytes"), message)
        self.assertIn(avoid_wrapping("0 bytes"), message)
