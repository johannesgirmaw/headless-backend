"""
File storage service for handling file uploads and management.
"""

import os
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class FileStorageService:
    """
    Service for handling file uploads and storage operations.
    """

    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt', '.rtf']
    ALLOWED_ARCHIVE_EXTENSIONS = ['.zip', '.rar', '.7z', '.tar', '.gz']

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5MB

    @classmethod
    def validate_file(cls, file, file_type='document'):
        """
        Validate uploaded file.

        Args:
            file: Django UploadedFile object
            file_type: Type of file ('image', 'document', 'archive')

        Returns:
            bool: True if valid, False otherwise

        Raises:
            ValidationError: If file is invalid
        """
        # Check file size
        if file.size > cls.MAX_FILE_SIZE:
            raise ValidationError(
                f"File size exceeds maximum allowed size of {cls.MAX_FILE_SIZE / (1024*1024):.1f}MB")

        # Check file extension
        file_extension = os.path.splitext(file.name)[1].lower()

        if file_type == 'image':
            if file_extension not in cls.ALLOWED_IMAGE_EXTENSIONS:
                raise ValidationError(
                    f"Invalid image format. Allowed formats: {', '.join(cls.ALLOWED_IMAGE_EXTENSIONS)}")

            # Additional validation for images
            if file.size > cls.MAX_IMAGE_SIZE:
                raise ValidationError(
                    f"Image size exceeds maximum allowed size of {cls.MAX_IMAGE_SIZE / (1024*1024):.1f}MB")

        elif file_type == 'document':
            if file_extension not in cls.ALLOWED_DOCUMENT_EXTENSIONS:
                raise ValidationError(
                    f"Invalid document format. Allowed formats: {', '.join(cls.ALLOWED_DOCUMENT_EXTENSIONS)}")

        elif file_type == 'archive':
            if file_extension not in cls.ALLOWED_ARCHIVE_EXTENSIONS:
                raise ValidationError(
                    f"Invalid archive format. Allowed formats: {', '.join(cls.ALLOWED_ARCHIVE_EXTENSIONS)}")

        return True

    @classmethod
    def generate_unique_filename(cls, original_filename):
        """
        Generate a unique filename for the uploaded file.

        Args:
            original_filename: Original filename

        Returns:
            str: Unique filename
        """
        file_extension = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_extension}"

    @classmethod
    def upload_file(cls, file, folder_path='uploads', file_type='document'):
        """
        Upload file to storage.

        Args:
            file: Django UploadedFile object
            folder_path: Folder path in storage
            file_type: Type of file ('image', 'document', 'archive')

        Returns:
            dict: Upload result with file info
        """
        try:
            # Validate file
            cls.validate_file(file, file_type)

            # Generate unique filename
            unique_filename = cls.generate_unique_filename(file.name)

            # Create full path
            full_path = os.path.join(folder_path, unique_filename)

            # Save file
            saved_path = default_storage.save(full_path, file)

            # Get file URL
            file_url = default_storage.url(saved_path)

            # Get file info
            file_info = {
                'original_name': file.name,
                'stored_name': unique_filename,
                'path': saved_path,
                'url': file_url,
                'size': file.size,
                'content_type': file.content_type,
                'file_type': file_type,
            }

            logger.info(f"File uploaded successfully: {saved_path}")
            return file_info

        except Exception as e:
            logger.error(f"Failed to upload file: {str(e)}")
            raise ValidationError(f"Failed to upload file: {str(e)}")

    @classmethod
    def upload_image(cls, file, folder_path='images', resize=True, max_size=(800, 600)):
        """
        Upload and process image file.

        Args:
            file: Django UploadedFile object
            folder_path: Folder path in storage
            resize: Whether to resize image
            max_size: Maximum size for resizing (width, height)

        Returns:
            dict: Upload result with file info
        """
        try:
            # Validate as image
            cls.validate_file(file, 'image')

            # Generate unique filename
            unique_filename = cls.generate_unique_filename(file.name)

            # Create full path
            full_path = os.path.join(folder_path, unique_filename)

            if resize:
                # Process image
                image = Image.open(file)

                # Convert to RGB if necessary
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')

                # Resize if needed
                if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Save processed image
                from io import BytesIO
                output = BytesIO()
                image.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)

                # Create ContentFile from processed image
                processed_file = ContentFile(output.getvalue())
                processed_file.name = unique_filename

                saved_path = default_storage.save(full_path, processed_file)
            else:
                saved_path = default_storage.save(full_path, file)

            # Get file URL
            file_url = default_storage.url(saved_path)

            # Get file info
            file_info = {
                'original_name': file.name,
                'stored_name': unique_filename,
                'path': saved_path,
                'url': file_url,
                'size': file.size,
                'content_type': file.content_type,
                'file_type': 'image',
                'resized': resize,
            }

            logger.info(f"Image uploaded successfully: {saved_path}")
            return file_info

        except Exception as e:
            logger.error(f"Failed to upload image: {str(e)}")
            raise ValidationError(f"Failed to upload image: {str(e)}")

    @classmethod
    def delete_file(cls, file_path):
        """
        Delete file from storage.

        Args:
            file_path: Path to file in storage

        Returns:
            bool: True if deleted successfully
        """
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                logger.info(f"File deleted successfully: {file_path}")
                return True
            else:
                logger.warning(f"File not found: {file_path}")
                return False

        except Exception as e:
            logger.error(f"Failed to delete file: {str(e)}")
            return False

    @classmethod
    def get_file_info(cls, file_path):
        """
        Get file information.

        Args:
            file_path: Path to file in storage

        Returns:
            dict: File information
        """
        try:
            if not default_storage.exists(file_path):
                return None

            file_info = {
                'path': file_path,
                'url': default_storage.url(file_path),
                'size': default_storage.size(file_path),
                'exists': True,
            }

            return file_info

        except Exception as e:
            logger.error(f"Failed to get file info: {str(e)}")
            return None

    @classmethod
    def list_files(cls, folder_path=''):
        """
        List files in a folder.

        Args:
            folder_path: Folder path in storage

        Returns:
            list: List of file paths
        """
        try:
            files = default_storage.listdir(folder_path)[1]  # Get files only
            return files

        except Exception as e:
            logger.error(f"Failed to list files: {str(e)}")
            return []

    @classmethod
    def create_folder(cls, folder_path):
        """
        Create a folder in storage.

        Args:
            folder_path: Folder path to create

        Returns:
            bool: True if created successfully
        """
        try:
            # Create a dummy file to create the folder
            dummy_file = ContentFile(b'')
            dummy_path = os.path.join(folder_path, '.keep')
            default_storage.save(dummy_path, dummy_file)

            logger.info(f"Folder created successfully: {folder_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to create folder: {str(e)}")
            return False
