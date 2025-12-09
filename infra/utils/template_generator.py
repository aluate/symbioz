"""
Template generator for Otto.
Generates project specs from templates.
"""

import re
from pathlib import Path
from typing import Any, Dict, Optional


def load_template(template_name: str) -> Dict[str, Any]:
    """Load a template by name."""
    template_dir = Path(__file__).parent.parent / "templates" / template_name
    
    if not template_dir.exists():
        raise ValueError(f"Template '{template_name}' not found in {template_dir.parent}")
    
    template_yaml_path = template_dir / "template.yaml"
    if not template_yaml_path.exists():
        raise ValueError(f"Template '{template_name}' missing template.yaml")
    
    import yaml
    with open(template_yaml_path, "r", encoding="utf-8") as f:
        template_meta = yaml.safe_load(f)
    
    project_spec_path = template_dir / "project-spec.yaml"
    if not project_spec_path.exists():
        raise ValueError(f"Template '{template_name}' missing project-spec.yaml")
    
    with open(project_spec_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    return {
        "metadata": template_meta,
        "content": template_content,
    }


def list_templates() -> list[Dict[str, Any]]:
    """List all available templates."""
    templates_dir = Path(__file__).parent.parent / "templates"
    
    if not templates_dir.exists():
        return []
    
    templates = []
    for template_dir in templates_dir.iterdir():
        if not template_dir.is_dir():
            continue
        
        if template_dir.name.startswith("."):
            continue
        
        template_yaml = template_dir / "template.yaml"
        if not template_yaml.exists():
            continue
        
        import yaml
        with open(template_yaml, "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        
        templates.append({
            "name": meta.get("name", template_dir.name),
            "description": meta.get("description", ""),
            "version": meta.get("version", "1.0.0"),
        })
    
    return templates


def render_template(template_content: str, variables: Dict[str, str]) -> str:
    """
    Render template content with variables.
    
    Supports simple {{variable}} substitution.
    Also handles {{#if variable}}...{{/if}} conditionals.
    """
    result = template_content
    
    # Handle conditionals first
    conditional_pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'
    
    def replace_conditional(match):
        var_name = match.group(1)
        content = match.group(2)
        if variables.get(var_name):
            # Render nested variables in conditional content
            return render_template(content, variables)
        return ""
    
    result = re.sub(conditional_pattern, replace_conditional, result, flags=re.DOTALL)
    
    # Replace variables
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, str(value))
    
    return result


def generate_project_spec(
    template_name: str,
    variables: Dict[str, str],
    output_path: Optional[Path] = None
) -> str:
    """
    Generate a project spec from a template.
    
    Args:
        template_name: Name of the template to use
        variables: Dictionary of variable values
        output_path: Optional path to save the generated spec
    
    Returns:
        Generated project spec content as string
    """
    template = load_template(template_name)
    
    # Validate required variables
    required_vars = template["metadata"].get("variables", [])
    for var_def in required_vars:
        if var_def.get("required", False):
            var_name = var_def["name"]
            if var_name not in variables or not variables[var_name]:
                raise ValueError(
                    f"Required variable '{var_name}' not provided. "
                    f"Description: {var_def.get('description', '')}"
                )
    
    # Render template
    generated = render_template(template["content"], variables)
    
    # Save if output path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(generated)
    
    return generated

