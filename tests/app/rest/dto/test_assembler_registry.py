import pytest
from datetime import datetime, UTC
from fastapi import HTTPException
from app.rest.assemblers.assembler_registry import AssemblerRegistry
from app.rest.assemblers.credential_assembler import CredentialAssembler
from app.domain.models.credential import Credential
from app.rest.dto.credential_dto import CredentialDTO


class MockCredential(Credential):
    def _validate_issuer_id(self, holder_id: str) -> None:
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
            valid_until="2024-12-31T23:59:59Z",
            issuing_country="CA"
        )

    def to_domain(self, credential_dto: dict) -> Credential:
        return MockCredential(
            issuer_id="test_issuer",
            holder_id="test_holder",
            valid_from=datetime(2024, 1, 1, tzinfo=UTC),
            valid_until=datetime(2024, 12, 31, tzinfo=UTC),
            issuing_country="CA"
        )


def test_given_assembler_class_when_registering_then_adds_to_registry():
    registry = AssemblerRegistry()

    @registry.register("test_credential")
    class TestAssembler(MockAssembler):
        pass

    assert "test_credential" in registry._assemblers
    assert registry._assemblers["test_credential"] == TestAssembler


def test_given_registered_credential_type_when_getting_assembler_then_returns_correct_assembler():
    registry = AssemblerRegistry()

    @registry.register("test_credential")
    class TestAssembler(MockAssembler):
        pass

    assembler = registry.get_assembler("test_credential")
    assert isinstance(assembler, TestAssembler)


def test_given_unregistered_credential_type_when_getting_assembler_then_raises_exception():
    registry = AssemblerRegistry()

    with pytest.raises(HTTPException) as exc_info:
        registry.get_assembler("nonexistent_credential")

    assert exc_info.value.status_code == 400
    assert "Unsupported credential type" in exc_info.value.detail


def test_given_multiple_assemblers_when_registering_then_all_are_accessible():
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


def test_given_existing_credential_type_when_registering_new_assembler_then_overwrites_previous():
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