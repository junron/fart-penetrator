import dataclasses


@dataclasses.dataclass()
class AttackConfig:
    store_raw_response: bool
    store_timing: bool
    store_content_length: bool

    def table_headers(self):
        return ["Status Code"] + (["Timing"] if self.store_timing else []) + (
            ["Length"] if self.store_content_length else [])
