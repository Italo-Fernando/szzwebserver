from dataclasses import dataclass, field

@dataclass
class ApiResponse:
    szz_variant: str
    repository_url: str
    status: str = "WAITING"
    result: list = field(default_factory=list)
