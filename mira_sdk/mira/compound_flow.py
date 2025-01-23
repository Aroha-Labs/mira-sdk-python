from .exceptions import LoadError, ValidationError
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .models.input import Input
from .models.metadata import Metadata
from .utils.yaml import load_yaml
import semantic_version

class CompoundFlow:
    def __init__(
            self,
            source: Optional[Union[str, Dict[str, Any], Path]] = None
        ):
        self._load_from_source(source)

    def _load_from_source(self, source: Union[str, Dict[str, Any], Path]) -> None:
        """
        Load compound flow configuration from source.

        Args:
            source: File path, dictionary, or Path object

        Raises:
            LoadError: If source cannot be loaded or is invalid
        """
        try:
            # Load config first
            if isinstance(source, (str, Path)):
                self.config = load_yaml(Path(source))
            else:
                self.config = source

            # Load version
            self.version = self.config.get('version', '0.1.0')

            # Load metadata
            meta = self.config.get('metadata', {})
            if not meta:
                raise ValueError("Metadata configuration is required")
            if meta.get('flow_type') != 'compound':
                raise ValueError("Invalid metadata or flow_type is not 'compound'")

            self.metadata = Metadata(
                name=meta.get('name', ''),
                description=meta.get('description', ''),
                author=meta.get('author', ''),
                private=meta.get('private', False),
                tags=meta.get('tags', []),
                flow_type=meta.get('flow_type')
            )

            # Load inputs
            self.inputs = {
                name: Input(**spec)
                for name, spec in self.config.get('inputs', {}).items()
            }

            # Load workflow
            workflow = self.config.get('workflow')
            if not workflow:
                raise ValueError("Workflow configuration is required for compound flows")
            self.workflow = workflow

            # Load output configuration
            self.output = self.config.get('output', {})

            # Load readme
            self.readme = self.config.get('readme', '')

            # Move validation to the end after all attributes are set
            if not self.validate():
                raise ValueError("Invalid compound flow configuration")

        except Exception as e:
            raise LoadError(f"Failed to load compound flow configuration: {str(e)}")


    def validate(self) -> bool:
        """
        Validate the flow configuration.

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validation fails
        """

        try:
            # Validate required fields
            if not self.metadata.name:
                raise ValidationError("Flow name is required")

            if not self.metadata.author:
                raise ValidationError("Flow author is required")

            if not self.metadata.description:
                raise ValidationError("Flow description is required")

            if not self.metadata.flow_type or self.metadata.flow_type != "compound":
                raise ValidationError("Flow type must be 'compound'")

            # Validate version if present
            if hasattr(self, 'version'):
                if not isinstance(self.version, str):
                    raise ValidationError("Version must be a semantic version string (e.g., '0.1.0')")
                try:
                    semantic_version.Version(self.version)
                except ValueError:
                    raise ValidationError("Version must be a semantic version string (e.g., '0.1.0')")

            # Validate workflow
            if not self.workflow:
                raise ValidationError("Workflow configuration is required")

            # Validate each workflow step
            for step_name, step in self.workflow.items():
                if 'type' not in step:
                    raise ValidationError(f"Step '{step_name}' missing required 'type' field")

                if 'inputs' not in step:
                    raise ValidationError(f"Step '{step_name}' missing required 'inputs' field")

                if 'model' not in step:
                    raise ValidationError(f"Step '{step_name}' missing required 'model' field")

                # Validate model configuration
                model = step['model']
                if not model.get('provider'):
                    raise ValidationError(f"Model provider is required for step '{step_name}'")
                if not model.get('name'):
                    raise ValidationError(f"Model name is required for step '{step_name}'")

                # Validate dependencies
                if 'depends_on' in step:
                    deps = step['depends_on']
                    if not isinstance(deps, list):
                        raise ValidationError(f"'depends_on' must be a list in step '{step_name}'")
                    for dep in deps:
                        if dep not in self.workflow:
                            raise ValidationError(f"Step '{step_name}' depends on non-existent step '{dep}'")

            # Validate output configuration exists
            if not self.output:
                raise ValidationError("Output configuration is required")

        except Exception as e:
            raise ValidationError(f"Flow validation failed: {str(e)}")

        return True
