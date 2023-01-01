import dataclasses


@dataclasses.dataclass()
class AttackConfig:
    store_raw_response: bool = True
    store_timing: bool = True
    store_content_length: bool = True
    terminate_attack_if: str = "stored_response.status_code > 499"
    store_response_if: str = "True"

    def table_headers(self):
        return ["Status Code"] + (["Timing"] if self.store_timing else []) + (
            ["Length"] if self.store_content_length else [])
