from fastapi import HTTPException
from typing import Type, Dict

from app.rest.assemblers.credential_assembler import CredentialAssembler


class AssemblerRegistry:
    _assemblers: Dict[str, Type[CredentialAssembler]] = {}

    @classmethod
    def register(cls, credential_type: str):
        def decorator(assembler_class: Type[CredentialAssembler]):
            cls._assemblers[credential_type] = assembler_class
            return assembler_class
        return decorator

    def get_assembler(self, credential_type: str) -> CredentialAssembler:
        assembler_class = self._assemblers.get(credential_type)
        if not assembler_class:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported credential type: {credential_type}"
            )
        return assembler_class()