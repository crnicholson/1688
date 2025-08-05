#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Very simple server with one endpoint:
POST /search - accepts image URL and prints search r    app.run(host='127.0.0.1', port=5001, debug=True)sults
"""

import os
import sys
import tempfile
import requests
from flask import Flask, request, jsonify

# Add the lib directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.ali1688 import ali1688

app = Flask(__name__)


def download_image(image_url):
    """Download image from URL to temporary file"""
    try:
        print(f"📥 Downloading image from: {image_url}")
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()

        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_file.write(response.content)
        temp_file.close()

        print(f"✅ Image downloaded to: {temp_file.name}")
        return temp_file.name

    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return None


def search_1688(image_path):
    """Upload image to 1688 and get search URL"""
    try:
        # Upload image and get image ID
        print("🔄 Uploading image to 1688...")
        upload = ali1688.Ali1688Upload()
        response = upload.upload(filename=image_path)

        # Extract image ID from response
        response_data = response.json()
        image_id = response_data.get("data", {}).get("imageId", "")

        if not image_id:
            print("❌ Failed to get image ID")
            return None

        print(f"✅ Image uploaded successfully! Image ID: {image_id}")

        # Generate search URL
        # search_url = f"https://s.1688.com/youyuan/index.htm?tab=imageSearch&imageId={image_id}&imageIdList={image_id}"

        search_url = (
            f"https://acbuy.com/search-list?searchType=picture&imageId={image_id}"
        )

        print("=" * 80)
        print("🎯 SEARCH RESULTS:")
        print(f"Search URL: {search_url}")
        print("=" * 80)

        return search_url

    except Exception as e:
        print(f"❌ Error searching on 1688: {e}")
        return None


@app.route("/search", methods=["POST"])
def search():
    """
    Simple endpoint that accepts an image URL and prints search results

    Request: POST /search
    Body: {"image_url": "https://example.com/image.jpg"}
    """
    try:
        # Get image URL from request
        data = request.get_json()
        if not data or "image_url" not in data:
            return jsonify({"error": "Missing image_url in request body"}), 400

        image_url = data["image_url"]
        print(f"\n🚀 Starting search for image: {image_url}")

        # Download image
        temp_image_path = download_image(image_url)
        if not temp_image_path:
            return jsonify({"error": "Failed to download image"}), 400

        try:
            # Search on 1688
            search_url = search_1688(temp_image_path)

            # Clean up temporary file
            os.unlink(temp_image_path)
            print("🗑️ Cleaned up temporary file")

            if search_url:
                return jsonify(
                    {
                        "success": True,
                        "search_url": search_url,
                        "message": "Search completed successfully!",
                    }
                )
            else:
                return jsonify({"error": "Failed to search on 1688"}), 500

        except Exception as e:
            # Make sure to clean up temp file even if search fails
            if os.path.exists(temp_image_path):
                os.unlink(temp_image_path)
            raise e

    except Exception as e:
        print(f"❌ Server error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Simple 1688 search server is running"})


if __name__ == "__main__":
    print("🚀 Starting simple 1688 search server...")
    print("📋 Usage:")
    print("  POST /search")
    print('  Body: {"image_url": "https://example.com/image.jpg"}')
    print("  GET /health - Health check")
    print("\n💡 The search results will be printed in the terminal!")
    print("=" * 80)

    app.run(host="127.0.0.1", port=5001, debug=True)
