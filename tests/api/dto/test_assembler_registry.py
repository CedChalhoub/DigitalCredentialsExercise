import pytest
from fastapi import HTTPException
from app.api.dto.AssemblerRegistry import AssemblerRegistry
from app.api.dto.CredentialAssembler import CredentialAssembler
from app.domain.Credential import Credential
from app.api.dto.CredentialDTO import CredentialDTO


# Test fixtures
class MockCredential(Credential):
    def _validate_holder_id(self, holder_id: str) -> None:
        pass

    def get_credential_type(self):
        pass

    @property
    def authorized_issuers(self):
        return []


class MockAssembler(CredentialAssembler):
    def to_dto(self, credential: Credential) -> CredentialDTO:
        return CredentialDTO(
            issuer_id="test_issuer",
            holder_id="test_holder",
            valid_from="2024-01-01T00:00:00Z",
            valid_until="2024-12-31T23:59:59Z"
        )

    def to_domain(self, credential_dto: dict) -> Credential:
        return MockCredential(
            issuer_id="test_issuer",
            holder_id="test_holder",
            valid_from="2024-01-01T00:00:00Z",
            valid_until="2024-12-31T23:59:59Z"
        )


def test_register_assembler():
    registry = AssemblerRegistry()

    @registry.register("test_credential")
    class TestAssembler(MockAssembler):
        pass

    assert "test_credential" in registry._assemblers
    assert registry._assemblers["test_credential"] == TestAssembler


def test_get_assembler_success():
    registry = AssemblerRegistry()

    @registry.register("test_credential")
    class TestAssembler(MockAssembler):
        pass

    assembler = registry.get_assembler("test_credential")
    assert isinstance(assembler, TestAssembler)


def test_get_assembler_not_found():
    registry = AssemblerRegistry()

    with pytest.raises(HTTPException) as exc_info:
        registry.get_assembler("nonexistent_credential")

    assert exc_info.value.status_code == 400
    assert "Unsupported credential type" in exc_info.value.detail


def test_multiple_assemblers():
    registry = AssemblerRegistry()

    @registry.register("credential_1")
    class TestAssembler1(MockAssembler):
        pass

    @registry.register("credential_2")
    class TestAssembler2(MockAssembler):
        pass

    assert "credential_1" in registry._assemblers
    assert "credential_2" in registry._assemblers
    assert isinstance(registry.get_assembler("credential_1"), TestAssembler1)
    assert isinstance(registry.get_assembler("credential_2"), TestAssembler2)


def test_register_same_type_overwrites():
    registry = AssemblerRegistry()

    @registry.register("test_credential")
    class TestAssembler1(MockAssembler):
        pass

    @registry.register("test_credential")
    class TestAssembler2(MockAssembler):
        pass

    assembler = registry.get_assembler("test_credential")
    assert isinstance(assembler, TestAssembler2)
    assert registry._assemblers["test_credential"] == TestAssembler2