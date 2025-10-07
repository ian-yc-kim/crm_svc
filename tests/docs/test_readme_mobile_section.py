def test_readme_contains_mobile_section_and_refs():
    with open("README.md", "r", encoding="utf-8") as f:
        text = f.read()

    assert "Mobile-Friendly Responsive Design" in text
    assert "src/crm_svc/frontend/components/mobile_components.py" in text
    assert "src/crm_svc/frontend/utils/mobile_utils.py" in text
    # check for key helper function names used in codebase
    assert "inject_viewport_meta" in text
    assert "inject_mobile_base_css" in text
    assert "is_mobile_view" in text
