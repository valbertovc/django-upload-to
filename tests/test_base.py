from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

import upload_to as base

User = get_user_model()


class UUIDFileNameTestCase(TestCase):
    @mock.patch("upload_to.base.uuid4")
    def test_should_replace_filename_by_uuid(self, uuid4):
        uuid4.return_value.hex = "abcd123"
        filename = base.uuid_filename("test.pdf")
        self.assertIn("abcd123", filename)

    def test_should_keep_original_extension(self):
        filename = base.uuid_filename("test.pdf")
        self.assertIn(".pdf", filename)


class UploadToTestCase(TestCase):
    def test_should_join_path_with_file_name(self):
        upload_path = base.upload_to(["a", "b"], "test.pdf")
        self.assertIn("a/b/test.pdf", upload_path)

    def test_should_replace_timestamp_by_timezone_now_values(self):
        upload_path = base.upload_to(["a", "%Y"], "test.pdf")
        current_year = timezone.now().year
        self.assertIn(f"a/{current_year}/test.pdf", upload_path)


class NormalizeFileNameTestCase(TestCase):
    def test_should_replace_spaces_by_undersore(self):
        filename = base.normalize_filename("test file name.pdf")
        self.assertIn("test_file_name.pdf", filename)

    def test_should_transform_to_lower_case(self):
        filename = base.normalize_filename("Test.PDF")
        self.assertIn("test.pdf", filename)

    def test_should_remove_accent_signal(self):
        filename = base.normalize_filename("tést.pdf")
        self.assertIn("test.pdf", filename)


class OptionsFromInstanceTestCase(TestCase):
    def test_should_return_app_label(self):
        user = User()
        options = base.options_from_instance(user)
        self.assertIn(user._meta.app_label, options)  # pylint: disable=protected-access

    def test_should_return_model_name(self):
        user = User()
        options = base.options_from_instance(user)
        self.assertIn(
            user._meta.model_name, options  # pylint: disable=protected-access
        )


class UploadToClassTestCase(TestCase):
    def test_prefix_as_none_should_create_empty_folder_path(self):
        generator = base.UploadTo(prefix=None)
        self.assertEqual([], generator.prefix)

    def test_prefix_as_string_path_directory_should_create_list_of_subfolders(self):
        generator = base.UploadTo(prefix="a/b/c")
        self.assertEqual(["a", "b", "c"], generator.prefix)

    def test_get_dirname_should_be_equal_to_prefix(self):
        generator = base.UploadTo(prefix="a")
        self.assertEqual(generator.prefix, generator.get_dirname(mock.Mock()))

    def test_get_filename_shuld_return_a_normalized_name(self):
        generator = base.UploadTo()
        self.assertEqual("test.pdf", generator.get_filename("Tést.PdF"))

    def test_calling_with_string_prefix_should_build_a_full_file_name(self):
        generator = base.UploadTo("folder/subfolder")
        instance = mock.Mock()
        filename = "test.pdf"
        self.assertEqual("folder/subfolder/test.pdf", generator(instance, filename))

    def test_calling_with_list_prefix_should_generate_a_full_file_name(self):
        generator = base.UploadTo(["folder", "subfolder"])
        instance = mock.Mock()
        filename = "test.pdf"
        self.assertEqual("folder/subfolder/test.pdf", generator(instance, filename))

    def test_calling_with_strftime_format_should_generate_a_full_file_name_from_timezone(
        self,
    ):
        generator = base.UploadTo(["folder", "%Y"])
        instance = mock.Mock()
        filename = "test.pdf"
        current_year = timezone.now().year
        self.assertEqual(
            f"folder/{current_year}/test.pdf", generator(instance, filename)
        )


class UuidUploadToTestCase(TestCase):
    @mock.patch("upload_to.base.uuid4")
    def test_get_filename_should_generates_a_new_uuid_name(self, uuid4):
        uuid4.return_value.hex = "abcd123"
        generator = base.UuidUploadTo()
        self.assertIn("abcd123.pdf", generator.get_filename("test.pdf"))

    @mock.patch("upload_to.base.uuid4")
    def test_calling_should_generate_a_new_full_path_with_uuid_as_file_name(
        self, uuid4
    ):
        uuid4.return_value.hex = "abcd123"
        generator = base.UuidUploadTo("a_folder")
        instance = mock.Mock()
        filename = "test.pdf"
        self.assertIn("a_folder/abcd123.pdf", generator(instance, filename))


class AttrUploadToTestCase(TestCase):
    def test_attrs_as_string_should_create_list_of_attrs(self):
        generator = base.AttrUploadTo(attrs="username")
        instance = User(username="test")
        self.assertEqual(["test"], generator.get_attrs(instance))

    def test_attrs_as_list_should_create_list_of_attrs(self):
        generator = base.AttrUploadTo(attrs=["username", "first_name"])
        instance = User(username="test", first_name="other")
        self.assertEqual(["test", "other"], generator.get_attrs(instance))

    def test_calling_should_generate_a_full_file_name_from_attrs_and_prefix(self):
        generator = base.AttrUploadTo(prefix="a/b", attrs=["username", "first_name"])
        instance = User(username="test", first_name="other")
        filename = "test.pdf"
        self.assertEqual("a/b/test/other/test.pdf", generator(instance, filename))


class ModelUploadToTestCase(TestCase):
    def test_dir_name_sould_return_options_from_instance(self):
        generator = base.ModelUploadTo()
        instance = User()
        options = (
            User._meta.app_label,  # pylint: disable=protected-access
            User._meta.model_name,  # pylint: disable=protected-access
        )
        self.assertEqual(list(options), generator.get_dirname(instance))

    def test_attrs_as_string_should_create_list_of_attrs(self):
        generator = base.ModelUploadTo(attrs="username")
        instance = User(username="user_name_test")
        self.assertEqual(["user_name_test"], generator.get_attrs(instance))

    def test_attrs_as_list_should_create_list_of_attrs(self):
        generator = base.ModelUploadTo(attrs=["username", "first_name"])
        instance = User(username="user_name_test", first_name="first_name_test")
        self.assertEqual(
            ["user_name_test", "first_name_test"], generator.get_attrs(instance)
        )

    def test_calling_should_generate_a_full_file_name_from_attrs_and_prefix(self):
        generator = base.ModelUploadTo(
            prefix="prefixfolder", attrs=["username", "first_name"]
        )
        instance = User(username="user_name_test", first_name="first_name_test")
        filename = "test.pdf"
        folder = (
            f"prefixfolder/"
            f"{instance._meta.app_label}/{instance._meta.model_name}/"  # pylint: disable=protected-access
            "user_name_test/first_name_test/test.pdf"
        )
        self.assertEqual(folder, generator(instance, filename))
