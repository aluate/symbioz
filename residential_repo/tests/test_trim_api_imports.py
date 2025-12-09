def test_import_fastapi_app():
    import apps.web.trim_api as trim_api
    assert hasattr(trim_api, "app")

