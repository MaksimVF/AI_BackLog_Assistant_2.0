





"""
Test S3 Integration for AI Backlog Assistant

This module tests the S3 file storage integration.
"""

import pytest
import tempfile
import os
from src.utils.s3_client import s3_client

@pytest.mark.skip(reason="S3 integration test - requires S3 credentials and bucket")
def test_s3_file_upload_download():
    """Test S3 file upload and download"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"Test content for S3 upload")
        tmp_path = tmp.name

    s3_key = "test/test_upload.txt"

    # Upload the file
    result = s3_client.upload_file(tmp_path, s3_key)
    assert result is True

    # Download the file
    download_path = tmp_path + "_downloaded"
    result = s3_client.download_file(s3_key, download_path)
    assert result is True

    # Verify content
    with open(download_path, 'rb') as f:
        content = f.read()
        assert content == b"Test content for S3 upload"

    # Clean up
    os.remove(tmp_path)
    os.remove(download_path)

@pytest.mark.skip(reason="S3 integration test - requires S3 credentials and bucket")
def test_s3_file_url():
    """Test S3 file URL generation"""
    s3_key = "test/test_file.txt"
    url = s3_client.get_file_url(s3_key)

    assert url.startswith("https://")
    assert s3_client.bucket_name in url
    assert s3_key in url

@pytest.mark.skip(reason="S3 integration test - requires S3 credentials and bucket")
def test_s3_file_listing():
    """Test S3 file listing"""
    # Upload a test file first
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"Test content for listing")
        tmp_path = tmp.name

    s3_key = "test/listing_test.txt"
    s3_client.upload_file(tmp_path, s3_key)

    # List files
    files = s3_client.list_files("test/")
    assert len(files) >= 1
    assert any(file['key'] == s3_key for file in files)

    # Clean up
    os.remove(tmp_path)
